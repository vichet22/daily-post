#!/usr/bin/env python3
"""
Daily Post Project Launcher
Starts both the main application and database manager with proper frontend-backend connections
"""

import os
import subprocess
import sys
import webbrowser
import time
import threading
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking project requirements...")
    
    # Check if backend directory exists
    if not os.path.exists('backend'):
        print("❌ Backend directory not found!")
        return False
    
    # Check if frontend directory exists
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        return False
    
    # Check if main app.py exists
    if not os.path.exists('backend/app.py'):
        print("❌ Main application (backend/app.py) not found!")
        return False
    
    # Check if database manager exists
    if not os.path.exists('backend/db_project_manager.py'):
        print("❌ Database manager (backend/db_project_manager.py) not found!")
        return False
    
    # Check if frontend templates exist
    if not os.path.exists('frontend/templates'):
        print("❌ Frontend templates directory not found!")
        return False
    
    # Check if frontend static files exist
    if not os.path.exists('frontend/static'):
        print("❌ Frontend static files directory not found!")
        return False
    
    print("✅ All requirements met!")
    return True

def start_main_app():
    """Start the main Daily Post application"""
    print("🚀 Starting Daily Post Application...")
    print("📍 Location: backend/app.py")
    print("🌐 URL: http://localhost:5000")
    
    try:
        # Change to backend directory and start the app
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Daily Post Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting Daily Post Application: {e}")
    finally:
        # Change back to root directory
        os.chdir('..')

def start_db_manager():
    """Start the Database Project Manager"""
    print("🗄️  Starting Database Project Manager...")
    print("📍 Location: backend/db_project_manager.py")
    print("🌐 URL: http://localhost:5001")
    
    try:
        # Change to backend directory and start the db manager
        os.chdir('backend')
        subprocess.run([sys.executable, 'db_project_manager.py'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Database Project Manager stopped by user")
    except Exception as e:
        print(f"❌ Error starting Database Project Manager: {e}")
    finally:
        # Change back to root directory
        os.chdir('..')

def start_both_apps():
    """Start both applications in separate threads"""
    print("🚀 Starting both applications...")
    
    # Start main app in a separate thread
    main_app_thread = threading.Thread(target=start_main_app, daemon=True)
    main_app_thread.start()
    
    # Wait a moment for the main app to start
    time.sleep(3)
    
    # Start database manager in a separate thread
    db_manager_thread = threading.Thread(target=start_db_manager, daemon=True)
    db_manager_thread.start()
    
    # Wait a moment for both to start
    time.sleep(3)
    
    # Open browsers
    print("🌐 Opening web browsers...")
    webbrowser.open('http://localhost:5000')
    time.sleep(1)
    webbrowser.open('http://localhost:5001')
    
    print("\n" + "="*60)
    print("🎉 DAILY POST PROJECT RUNNING!")
    print("="*60)
    print("📱 Main Application: http://localhost:5000")
    print("🗄️  Database Manager: http://localhost:5001")
    print("📁 Frontend: frontend/ folder")
    print("⚙️  Backend: backend/ folder")
    print("="*60)
    print("Press Ctrl+C to stop all services")
    print("="*60)
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down all services...")

def show_menu():
    """Show the main menu"""
    print("\n" + "="*60)
    print("🗞️  DAILY POST PROJECT LAUNCHER")
    print("="*60)
    print("Choose an option:")
    print()
    print("1. 🚀 Start Main Application Only (Port 5000)")
    print("2. 🗄️  Start Database Manager Only (Port 5001)")
    print("3. 🌐 Start Both Applications")
    print("4. 📊 Check Project Status")
    print("5. 📖 Show Connection Info")
    print("6. ❌ Exit")
    print()

def check_project_status():
    """Check the status of project components"""
    print("\n📊 PROJECT STATUS CHECK")
    print("="*40)
    
    # Check directories
    print("\n📁 Directory Structure:")
    dirs = ['backend', 'frontend', 'frontend/templates', 'frontend/static', 'backend/instance']
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (missing)")
    
    # Check key files
    print("\n📄 Key Files:")
    files = [
        'backend/app.py',
        'backend/db_project_manager.py',
        'backend/requirements.txt',
        'frontend/templates/base.html',
        'frontend/templates/index.html',
        'frontend/static/css/style.css',
        'frontend/static/js/main.js'
    ]
    for file_path in files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
    
    # Check ports
    print("\n🌐 Port Status:")
    import socket
    
    ports = [5000, 5001]
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        if result == 0:
            print(f"   🟢 Port {port}: In use")
        else:
            print(f"   🔴 Port {port}: Available")
        sock.close()

def show_connection_info():
    """Show frontend-backend connection information"""
    print("\n🔗 FRONTEND-BACKEND CONNECTION INFO")
    print("="*50)
    print("""
📁 Project Structure:
   ├── frontend/              # All UI components
   │   ├── templates/         # HTML templates
   │   ├── static/           # CSS, JS, images
   │   └── db_templates/     # Database UI templates
   └── backend/              # All server-side code
       ├── app.py           # Main Flask app
       ├── db_project_manager.py  # Database manager
       └── instance/        # Database files

🔗 Connection Configuration:
   • Main App (app.py):
     - Templates: ../frontend/templates
     - Static: ../frontend/static
     - Upload: ../frontend/static/images
   
   • DB Manager (db_project_manager.py):
     - Templates: ../frontend/db_templates
     - Static: ../frontend/static
     - Upload: ../frontend/static/images

🌐 Access URLs:
   • Main Application: http://localhost:5000
   • Database Manager: http://localhost:5001
   • Admin Panel: http://localhost:5000/admin
   • API Endpoints: http://localhost:5000/api/posts

🔧 Features:
   • Shared static assets between both apps
   • Separate template folders for different purposes
   • Common image upload directory
   • PostgreSQL database integration
   • Real-time frontend updates
""")

def main():
    """Main launcher function"""
    print("🗞️  Daily Post Project Launcher")
    print("Connecting Frontend and Backend...")
    
    # Check requirements first
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                start_main_app()
            elif choice == '2':
                start_db_manager()
            elif choice == '3':
                start_both_apps()
            elif choice == '4':
                check_project_status()
            elif choice == '5':
                show_connection_info()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
            
            if choice not in ['3', '6']:
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
