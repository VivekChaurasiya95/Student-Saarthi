import os
import sys
import json
import time
import urllib.request
import urllib.error

# Ensure immediate line-buffered printing
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

def get_token():
    config_file = os.path.expanduser("~/.antideploy/config.json")
    if not os.path.exists(config_file):
        raise RuntimeError("No Antideploy token found in ~/.antideploy/config.json")
    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["token"]

def api_call(path, method="GET", body=None, headers=None):
    token = get_token()
    url = f"https://antideploy.com{path}" if path.startswith("/") else path
    req_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    if headers:
        req_headers.update(headers)
    
    data = None
    if body is not None:
        if isinstance(body, dict):
            data = json.dumps(body).encode("utf-8")
        elif isinstance(body, bytes):
            data = body
        else:
            data = str(body).encode("utf-8")
            
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode("utf-8")
                try:
                    return resp.status, json.loads(content)
                except Exception:
                    return resp.status, content
        except urllib.error.HTTPError as e:
            content = e.read().decode("utf-8")
            try:
                return e.code, json.loads(content)
            except Exception:
                return e.code, content
        except (urllib.error.URLError, ConnectionResetError) as e:
            if attempt < 4:
                time.sleep(2)
                continue
            return 500, {"error": str(e)}

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if action == "check_hostname":
        label = sys.argv[2]
        status, res = api_call(f"/api/v1/hostnames/check?label={label}")
        print(f"Status: {status}, Result: {res}")
        
    elif action == "list_applications":
        status, res = api_call("/api/v1/applications")
        print(f"Status: {status}, Applications: {res}")
        
    elif action == "create_application":
        name = sys.argv[2]
        subdomain = sys.argv[3] if len(sys.argv) > 3 else None
        body = {"name": name}
        if subdomain:
            body["subdomain"] = subdomain
        status, res = api_call("/api/v1/applications", method="POST", body=body)
        print(f"Status: {status}, Result: {res}")
        if status in (200, 201):
            with open(".antideploy.json", "w", encoding="utf-8") as f:
                json.dump({"applicationId": res.get("id") or res.get("applicationId")}, f, indent=2)
            print("Saved .antideploy.json successfully.")
        elif status == 409 and isinstance(res, dict) and res.get("applicationId"):
            with open(".antideploy.json", "w", encoding="utf-8") as f:
                json.dump({"applicationId": res.get("applicationId")}, f, indent=2)
            print(f"Application already existed, saved existing applicationId: {res.get('applicationId')}")
            
    elif action == "create_database":
        app_id = sys.argv[2]
        status, res = api_call(f"/api/v1/database?applicationId={app_id}", method="POST")
        print(f"Database Creation Status: {status}, Result: {res}")
        
    elif action == "redeploy":
        app_id = sys.argv[2] if len(sys.argv) > 2 else None
        if not app_id:
            with open(".antideploy.json", "r", encoding="utf-8") as f:
                app_id = json.load(f)["applicationId"]

        print(f"🔄 Requesting redeploy for {app_id}...")
        status, res = api_call("/api/v1/redeploy", method="POST", body={"applicationId": app_id})
        print(f"Redeploy response ({status}): {res}")
        if status in (200, 202) and isinstance(res, dict) and (res.get("taskId") or res.get("id")):
            task_id = res.get("taskId") or res.get("id")
            print(f"📋 Watching redeployment task {task_id}...")
            # Watch task
            watch_path = f"/api/v1/deployments/{task_id}"
            last_step = None
            while True:
                time.sleep(3)
                poll_status, poll_res = api_call(watch_path)
                if poll_status != 200 or not isinstance(poll_res, dict):
                    continue
                status = poll_res.get("status")
                step = poll_res.get("step") or poll_res.get("progress")
                if step != last_step:
                    print(f"⚙️ Step: {step or status}")
                    last_step = step
                if status == "succeeded":
                    print("\n🎉 REDEPLOY SUCCEEDED! All credentials applied.")
                    print(f"🌐 Summary: {poll_res.get('summary')}")
                    print(f"🔗 Live URL: {poll_res.get('url') or poll_res.get('address')}")
                    print(f"🔑 Credentials: {poll_res.get('credentials')}")
                    break
                elif status == "failed":
                    print("\n❌ Redeploy failed:", poll_res.get("error"))
                    break

    elif action in ("status", "watch"):
        import time
        task_id = sys.argv[2] if len(sys.argv) > 2 else "3bf3e602-f4b9-474e-9a60-c56767527584"
        watch_path = f"/api/v1/deployments/{task_id}"
        print(f"⏳ Checking deployment {task_id}...")
        last_step = None
        while True:
            poll_status, poll_res = api_call(watch_path)
            if poll_status != 200 or not isinstance(poll_res, dict):
                print(f"Status {poll_status}: {poll_res}")
                time.sleep(3)
                continue
                
            status = poll_res.get("status")
            step = poll_res.get("step") or poll_res.get("progress")
            if step != last_step:
                print(f"⚙️ Step: {step or status}")
                last_step = step

            if status == "succeeded":
                print("\n🎉 =================================================")
                print("🎉 DEPLOYMENT SUCCEEDED!")
                print("🎉 =================================================")
                print(f"🌐 Summary: {poll_res.get('summary')}")
                print(f"🔗 Live URL: {poll_res.get('url') or poll_res.get('address')}")
                acc = poll_res.get("account", {})
                print(f"👤 Account: {acc.get('label') or acc.get('email')}")
                sec = poll_res.get("security", {})
                issues = sec.get("issues", [])
                if issues:
                    print(f"⚠️ Security Issues ({len(issues)}):")
                    for iss in issues:
                        print(f"   - {iss.get('title')}: {iss.get('recommendation')}")
                else:
                    print("🛡️ Security Check: Passed cleanly with 0 issues.")
                break
            elif status == "failed":
                print("\n❌ =================================================")
                print("❌ DEPLOYMENT FAILED")
                print("❌ =================================================")
                print(f"Error: {poll_res.get('error')}")
                print(f"Failed Step: {poll_res.get('failedStep')}")
                deployment = poll_res.get("deployment", {})
                if deployment.get("buildLog"):
                    print("\n--- Build Log ---")
                    print(deployment["buildLog"][-2000:])
                if deployment.get("runtimeLog"):
                    print("\n--- Runtime Log ---")
                    print(deployment["runtimeLog"][-2000:])
                break
            time.sleep(3)
        
    elif action == "deploy":
        import io
        import tarfile
        import time

        app_id = sys.argv[2] if len(sys.argv) > 2 else None
        if not app_id:
            with open(".antideploy.json", "r", encoding="utf-8") as f:
                app_id = json.load(f)["applicationId"]

        print(f"📦 Packaging project for deployment (applicationId: {app_id})...")
        buf = io.BytesIO()
        exclude_dirs = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'instance'}
        exclude_files = {'.env', '.env.local'}

        file_count = 0
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            for root, dirs, files in os.walk('.'):
                dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('__pycache__')]
                for file in files:
                    if file in exclude_files or file.endswith('.pyc'):
                        continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, '.')
                    tar_name = rel_path.replace('\\', '/')
                    tar.add(full_path, arcname=tar_name)
                    file_count += 1

        archive_bytes = buf.getvalue()
        print(f"✅ Packaged {file_count} files ({len(archive_bytes)} bytes compressed).")

        token = get_token()
        boundary = "----AntideployBoundary" + str(int(time.time()))
        crlf = b"\r\n"
        body_bytes = (
            f"--{boundary}\r\n".encode("utf-8") +
            b'Content-Disposition: form-data; name="archive"; filename="project.tar.gz"\r\n' +
            b'Content-Type: application/gzip\r\n\r\n' +
            archive_bytes + crlf +
            f"--{boundary}--\r\n".encode("utf-8")
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }

        print("🚀 Uploading archive to Antideploy...")
        deploy_url = f"https://antideploy.com/api/v1/deploy?applicationId={app_id}"
        req = urllib.request.Request(deploy_url, data=body_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                deploy_res = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            print(f"❌ Deploy upload failed ({e.code}): {err_msg}")
            sys.exit(1)

        task_id = deploy_res.get("taskId") or deploy_res.get("id")
        print(f"📋 Deployment queued! Task ID: {task_id}")
        print("⏳ Watching deployment progress...")

        watch_path = f"/api/v1/deployments/{task_id}"
        last_step = None
        while True:
            time.sleep(3)
            poll_status, poll_res = api_call(watch_path)
            if poll_status != 200 or not isinstance(poll_res, dict):
                print(f"Polling status {poll_status}: {poll_res}")
                continue

            status = poll_res.get("status")
            step = poll_res.get("step") or poll_res.get("progress")
            if step != last_step:
                print(f"⚙️ Step: {step or status}")
                last_step = step

            if status == "succeeded":
                print("\n🎉 =================================================")
                print("🎉 DEPLOYMENT SUCCEEDED!")
                print("🎉 =================================================")
                summary = poll_res.get("summary")
                url = poll_res.get("url") or poll_res.get("address")
                account = poll_res.get("account", {})
                print(f"🌐 Summary: {summary}")
                print(f"🔗 Live URL: {url}")
                print(f"👤 Account: {account.get('label') or account.get('email')}")
                
                sec = poll_res.get("security", {})
                issues = sec.get("issues", [])
                if issues:
                    print(f"⚠️ Security Issues ({len(issues)}):")
                    for iss in issues:
                        print(f"   - {iss.get('title')}: {iss.get('recommendation')}")
                else:
                    print("🛡️ Security Check: Passed cleanly with 0 issues.")
                break
            elif status == "failed":
                print("\n❌ =================================================")
                print("❌ DEPLOYMENT FAILED")
                print("❌ =================================================")
                print(f"Error: {poll_res.get('error')}")
                print(f"Failed Step: {poll_res.get('failedStep')}")
                deployment = poll_res.get("deployment", {})
                if deployment.get("buildLog"):
                    print("\n--- Build Log ---")
                    print(deployment["buildLog"][-2000:])
                if deployment.get("runtimeLog"):
                    print("\n--- Runtime Log ---")
                    print(deployment["runtimeLog"][-2000:])
                sys.exit(1)

