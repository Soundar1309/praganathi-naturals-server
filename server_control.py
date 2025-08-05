#!/usr/bin/env python3
"""
Django Server Control Script
"""

import os
import sys
import subprocess
import signal
import psutil
import time

def find_django_process():
    """Find Django runserver process"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'manage.py' in ' '.join(proc.info['cmdline']):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def check_server_status():
    """Check if Django server is running"""
    proc = find_django_process()
    if proc:
        print(f"✅ Django server is running (PID: {proc.pid})")
        print(f"   URL: http://localhost:8000/")
        print(f"   API: http://localhost:8000/api/")
        print(f"   Admin: http://localhost:8000/admin/")
        return True
    else:
        print("❌ Django server is not running")
        return False

def stop_server():
    """Stop Django server"""
    proc = find_django_process()
    if proc:
        print(f"🛑 Stopping Django server (PID: {proc.pid})...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
            print("✅ Server stopped successfully")
        except psutil.TimeoutExpired:
            print("⚠️ Server didn't stop gracefully, forcing...")
            proc.kill()
            print("✅ Server force stopped")
    else:
        print("❌ No Django server found to stop")

def start_server():
    """Start Django server"""
    if check_server_status():
        print("⚠️ Server is already running!")
        return
    
    print("🚀 Starting Django server...")
    try:
        # Start server in background using python3
        subprocess.Popen([
            'python3', 'manage.py', 'runserver'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        if check_server_status():
            print("✅ Server started successfully!")
        else:
            print("❌ Failed to start server")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def restart_server():
    """Restart Django server"""
    print("🔄 Restarting Django server...")
    stop_server()
    time.sleep(1)
    start_server()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 server_control.py [start|stop|restart|status]")
        print("\nCommands:")
        print("  start   - Start the Django server")
        print("  stop    - Stop the Django server")
        print("  restart - Restart the Django server")
        print("  status  - Check server status")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_server()
    elif command == 'stop':
        stop_server()
    elif command == 'restart':
        restart_server()
    elif command == 'status':
        check_server_status()
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: start, stop, restart, status")

if __name__ == "__main__":
    main() 