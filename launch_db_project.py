#!/usr/bin/env python3
"""
Database Project Launcher
Simple launcher to open database projects
"""

import os
import subprocess
import sys
import webbrowser
import time

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🗄️  DATABASE PROJECT LAUNCHER")
    print("="*50)
    print()
    print("Available Database Projects:")
    print()
    print("1. 🌐 Database Project Manager (Web Interface)")
    print("2. 🐘 PostgreSQL Command Line")
    print("3. 📊 SQLite Database Browser")
    print("4. 🚀 Daily Post Application")
    print("5. 📁 View Database Files")
    print("6. ⚙️  Database Status Check")
    print("7. 📖 Help & Documentation")
    print("8. ❌ Exit")
    print()

def launch_web_manager():
    """Launch the Database Project Manager"""
    print("🌐 Starting Database Project Manager...")
    print("📊 Web interface will open at: http://localhost:5001")
    print("⏳ Please wait while the server starts...")
    
    try:
        # Start the database manager in a new process
        subprocess.Popen([sys.executable, 'db_project_manager.py'])
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open('http://localhost:5001')
        print("✅ Database Project Manager launched successfully!")
        print("💡 The web interface should open in your browser")
        
    except Exception as e:
        print(f"❌ Failed to launch Database Project Manager: {e}")
        print("💡 Try running manually: python db_project_manager.py")

def launch_postgresql_cli():
    """Launch PostgreSQL command line"""
    print("🐘 Opening PostgreSQL Command Line...")
    print("📊 Database: daily_post")
    print("👤 User: dailypost_user")
    print()
    
    psql_path = r"C:\Program Files\PostgreSQL\17\bin\psql.exe"
    
    if os.path.exists(psql_path):
        try:
            subprocess.run([psql_path, '-U', 'dailypost_user', '-d', 'daily_post'])
        except Exception as e:
            print(f"❌ Failed to launch PostgreSQL CLI: {e}")
    else:
        print("❌ PostgreSQL not found at expected location")
        print("💡 Try: psql -U dailypost_user -d daily_post")

def launch_sqlite_browser():
    """Launch SQLite browser"""
    print("📊 Opening SQLite Database...")
    
    sqlite_file = "instance/news.db"
    
    if os.path.exists(sqlite_file):
        print(f"✅ Found SQLite database: {sqlite_file}")
        print("💡 Opening file location...")
        
        # Open the directory containing the SQLite file
        if os.name == 'nt':  # Windows
            subprocess.run(['explorer', 'instance'])
        else:  # Linux/Mac
            subprocess.run(['open', 'instance'])
            
        print("💡 You can open the .db file with:")
        print("   - DB Browser for SQLite")
        print("   - SQLite Studio")
        print("   - Command: sqlite3 instance/news.db")
    else:
        print("❌ SQLite database not found!")
        print(f"💡 Expected location: {sqlite_file}")
        
        # Create instance directory if it doesn't exist
        os.makedirs('instance', exist_ok=True)
        print("✅ Created instance directory")

def launch_daily_post():
    """Launch Daily Post application"""
    print("🚀 Starting Daily Post Application...")
    print("🌐 Web interface will open at: http://localhost:5000")
    print("⏳ Please wait while the server starts...")
    
    try:
        # Start the Daily Post app
        subprocess.Popen([sys.executable, 'app.py'])
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open('http://localhost:5000')
        print("✅ Daily Post Application launched successfully!")
        
    except Exception as e:
        print(f"❌ Failed to launch Daily Post: {e}")
        print("💡 Try running manually: python app.py")

def view_database_files():
    """Show database-related files"""
    print("📁 Database Project Files:")
    print("="*40)
    
    # Python files
    print("\n🐍 Python Files:")
    for file in os.listdir('.'):
        if file.endswith('.py') and any(keyword in file.lower() for keyword in ['db', 'database', 'init']):
            print(f"   📄 {file}")
    
    # Documentation files
    print("\n📖 Documentation:")
    for file in os.listdir('.'):
        if file.endswith('.md') and any(keyword in file.lower() for keyword in ['db', 'database', 'postgresql']):
            print(f"   📋 {file}")
    
    # Configuration files
    print("\n⚙️  Configuration:")
    config_files = ['.env', 'requirements.txt', 'daily_post_postgresql_config.py']
    for file in config_files:
        if os.path.exists(file):
            print(f"   🔧 {file}")
    
    # Directories
    print("\n📂 Directories:")
    dirs = ['instance', 'migrations', 'db_templates', 'templates', 'static']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"   📁 {dir_name}/")

def check_database_status():
    """Check database status"""
    print("⚙️  Database Status Check:")
    print("="*40)
    
    # Check PostgreSQL
    print("\n🐘 PostgreSQL:")
    try:
        result = subprocess.run(['pg_isready'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ PostgreSQL server is running")
            print(f"   📊 Status: {result.stdout.strip()}")
        else:
            print("   ❌ PostgreSQL server not accessible")
    except FileNotFoundError:
        print("   ❌ PostgreSQL tools not found in PATH")
    
    # Check SQLite
    print("\n📊 SQLite:")
    sqlite_file = "instance/news.db"
    if os.path.exists(sqlite_file):
        size = os.path.getsize(sqlite_file)
        print(f"   ✅ SQLite database found")
        print(f"   📏 Size: {size} bytes")
    else:
        print("   ❌ SQLite database not found")
    
    # Check running processes
    print("\n🔄 Running Services:")
    try:
        # Check if ports are in use
        import socket
        
        # Check port 5000 (Daily Post)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        if result == 0:
            print("   ✅ Daily Post app running on port 5000")
        else:
            print("   ❌ Daily Post app not running on port 5000")
        sock.close()
        
        # Check port 5001 (DB Manager)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5001))
        if result == 0:
            print("   ✅ Database Manager running on port 5001")
        else:
            print("   ❌ Database Manager not running on port 5001")
        sock.close()
        
    except Exception as e:
        print(f"   ⚠️  Could not check running services: {e}")

def show_help():
    """Show help and documentation"""
    print("📖 Database Project Help:")
    print("="*40)
    print("""
🎯 Quick Start:
   1. Choose option 1 to open the Database Project Manager
   2. Use the web interface to explore your databases
   3. Run queries and export data as needed

🗄️ Available Databases:
   • PostgreSQL: daily_post database (production)
   • SQLite: instance/news.db (legacy)

🌐 Web Interfaces:
   • Database Manager: http://localhost:5001
   • Daily Post App: http://localhost:5000

💻 Command Line Access:
   • PostgreSQL: psql -U dailypost_user -d daily_post
   • SQLite: sqlite3 instance/news.db

📊 Sample Queries:
   • SELECT * FROM post;
   • SELECT category, COUNT(*) FROM post GROUP BY category;
   • SELECT * FROM post WHERE featured = true;

🔧 Troubleshooting:
   • Use option 6 to check database status
   • Ensure PostgreSQL service is running
   • Check that database files exist
""")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                launch_web_manager()
            elif choice == '2':
                launch_postgresql_cli()
            elif choice == '3':
                launch_sqlite_browser()
            elif choice == '4':
                launch_daily_post()
            elif choice == '5':
                view_database_files()
            elif choice == '6':
                check_database_status()
            elif choice == '7':
                show_help()
            elif choice == '8':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-8.")
            
            if choice != '8':
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
