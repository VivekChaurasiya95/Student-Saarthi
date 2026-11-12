"""
Student Saarthi - Application Entry Point (Compatibility Wrapper)
Delegates to run.py and Application Factory pattern.
"""
from run import app

if __name__ == '__main__':
    from run import host, port, debug
    app.run(host=host, port=port, debug=debug)
