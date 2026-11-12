import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')

    print("=" * 65)
    print("🎓 STUDENT SAARTHI - SCHOLARSHIP PORTAL")
    print("=" * 65)
    print(f"📡 Server Status: RUNNING")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐞 Debug Mode: {debug}")
    print("\n🔐 Default Administrator Credentials:")
    print("   - Username: admin")
    print("   - Password: admin123")
    print("\n🔗 Quick Access Links:")
    print(f"   - Portal Home:       http://127.0.0.1:{port}/")
    print(f"   - Scholarships:      http://127.0.0.1:{port}/scholarships.html")
    print(f"   - Student Login:     http://127.0.0.1:{port}/login.html")
    print(f"   - Admin Dashboard:   http://127.0.0.1:{port}/admin-dashboard.html")
    print("=" * 65)
    print("Press CTRL+C to stop the server.\n")

    app.run(host=host, port=port, debug=debug)

