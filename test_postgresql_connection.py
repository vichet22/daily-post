#!/usr/bin/env python3
"""
PostgreSQL Connection Test Script
"""

import subprocess
import sys

def install_psycopg2():
    """Install psycopg2 for PostgreSQL connectivity"""
    print("📦 Installing psycopg2 (PostgreSQL adapter for Python)...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'], 
                      check=True)
        print("✅ psycopg2-binary installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install psycopg2: {e}")
        return False

def test_basic_connection():
    """Test basic PostgreSQL connection"""
    print("\n🔗 Testing PostgreSQL Connection...")
    
    try:
        import psycopg2
        
        # Try to connect with common default settings
        print("Attempting to connect to PostgreSQL...")
        print("Note: This may prompt for the postgres user password")
        
        # Try connection without password first (for trust authentication)
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                database="postgres",
                user="postgres"
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connected successfully!")
            print(f"📊 Database version: {version[0]}")
            
            # List databases
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print(f"📋 Available databases: {[db[0] for db in databases]}")
            
            cursor.close()
            conn.close()
            return True
            
        except psycopg2.OperationalError as e:
            if "password" in str(e).lower():
                print("❌ Connection requires password authentication")
                print("💡 You need to set a password for the postgres user")
                print("💡 Run: psql -U postgres -c \"ALTER USER postgres PASSWORD 'your_password';\"")
            else:
                print(f"❌ Connection failed: {e}")
            return False
        
    except ImportError:
        print("❌ psycopg2 not installed. Installing now...")
        return install_psycopg2()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_flask_config():
    """Create Flask configuration for PostgreSQL"""
    print("\n⚙️ Creating Flask PostgreSQL Configuration...")
    
    config = '''# PostgreSQL Configuration for Flask
# Add this to your app.py

import os

# PostgreSQL Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'daily_post',  # Change this to your database name
    'user': 'postgres',
    'password': os.environ.get('POSTGRES_PASSWORD', 'your_password_here')
}

# SQLAlchemy Database URI for PostgreSQL
POSTGRESQL_URI = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Update your Flask app configuration:
# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI

# Example usage in app.py:
# Replace this line:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
# With this line:
# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI
'''
    
    with open('flask_postgresql_config.py', 'w') as f:
        f.write(config)
    
    print("✅ Flask configuration saved to flask_postgresql_config.py")

def main():
    """Main function"""
    print("🐘 PostgreSQL Connection Test")
    print("=" * 50)
    
    # Install psycopg2 if needed
    install_psycopg2()
    
    # Test connection
    test_basic_connection()
    
    # Create Flask config
    create_flask_config()
    
    print("\n" + "=" * 50)
    print("🎉 PostgreSQL Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Set postgres password (if needed):")
    print("   psql -U postgres -c \"ALTER USER postgres PASSWORD 'your_password';\"")
    print("2. Create your application database:")
    print("   createdb -U postgres daily_post")
    print("3. Update your Flask app to use PostgreSQL")
    print("4. Test your application with the new database")

if __name__ == '__main__':
    main()
