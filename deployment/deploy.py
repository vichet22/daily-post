#!/usr/bin/env python3
"""
Daily Post Deployment Helper Script
Automates the deployment process for various hosting platforms
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class DeploymentHelper:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.deployment_dir = Path(__file__).parent
        
    def check_requirements(self):
        """Check if all required files and dependencies are present"""
        print("🔍 Checking deployment requirements...")
        
        required_files = [
            'backend/app.py',
            'backend/requirements.txt',
            'frontend/templates',
            'frontend/static'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required files present")
        return True
    
    def create_env_file(self):
        """Create .env file from template"""
        env_example = self.deployment_dir / '.env.example'
        env_file = self.project_root / '.env'
        
        if env_file.exists():
            print("⚠️  .env file already exists")
            return True
        
        if env_example.exists():
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ .env file created. Please update with your actual values!")
            return True
        
        print("❌ .env.example template not found")
        return False
    
    def setup_vercel(self):
        """Setup Vercel deployment"""
        print("🚀 Setting up Vercel deployment...")
        
        # Copy vercel.json to project root
        vercel_config = self.deployment_dir / 'vercel.json'
        target_config = self.project_root / 'vercel.json'
        
        if vercel_config.exists():
            with open(vercel_config, 'r') as f:
                config = json.load(f)
            
            with open(target_config, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ vercel.json created")
        
        # Check if Vercel CLI is installed
        try:
            subprocess.run(['vercel', '--version'], check=True, capture_output=True)
            print("✅ Vercel CLI found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Vercel CLI not found. Install with: npm install -g vercel")
            return False
        
        print("🎯 Ready for Vercel deployment!")
        print("Run: vercel --prod")
        return True
    
    def setup_railway(self):
        """Setup Railway deployment"""
        print("🚂 Setting up Railway deployment...")
        
        # Copy railway.toml to project root
        railway_config = self.deployment_dir / 'railway.toml'
        target_config = self.project_root / 'railway.toml'
        
        if railway_config.exists():
            with open(railway_config, 'r') as f:
                content = f.read()
            
            with open(target_config, 'w') as f:
                f.write(content)
            
            print("✅ railway.toml created")
        
        print("🎯 Ready for Railway deployment!")
        print("1. Connect your GitHub repo to Railway")
        print("2. Add PostgreSQL service")
        print("3. Configure environment variables")
        return True
    
    def setup_heroku(self):
        """Setup Heroku deployment"""
        print("🟣 Setting up Heroku deployment...")
        
        # Copy Procfile to project root
        procfile = self.deployment_dir / 'Procfile'
        target_procfile = self.project_root / 'Procfile'
        
        if procfile.exists():
            with open(procfile, 'r') as f:
                content = f.read()
            
            with open(target_procfile, 'w') as f:
                f.write(content)
            
            print("✅ Procfile created")
        
        # Check if Heroku CLI is installed
        try:
            subprocess.run(['heroku', '--version'], check=True, capture_output=True)
            print("✅ Heroku CLI found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli")
            return False
        
        print("🎯 Ready for Heroku deployment!")
        print("Run the following commands:")
        print("1. heroku create your-app-name")
        print("2. heroku addons:create heroku-postgresql:mini")
        print("3. git push heroku main")
        return True
    
    def test_database_connection(self):
        """Test database connection with current environment"""
        print("🔌 Testing database connection...")
        
        try:
            import psycopg2
            from dotenv import load_dotenv
            
            load_dotenv()
            
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            
            cursor = conn.cursor()
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]
            
            print(f"✅ Database connection successful!")
            print(f"📊 PostgreSQL version: {version[:50]}...")
            
            cursor.close()
            conn.close()
            return True
            
        except ImportError:
            print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
            return False
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("💡 Check your .env file and database credentials")
            return False
    
    def show_menu(self):
        """Show deployment options menu"""
        print("\n" + "="*50)
        print("🚀 Daily Post Deployment Helper")
        print("="*50)
        print("1. Check requirements")
        print("2. Create .env file")
        print("3. Setup Vercel deployment")
        print("4. Setup Railway deployment")
        print("5. Setup Heroku deployment")
        print("6. Test database connection")
        print("7. Show deployment guide")
        print("0. Exit")
        print("="*50)
    
    def show_deployment_guide(self):
        """Show quick deployment guide"""
        print("\n📚 Quick Deployment Guide:")
        print("1. Choose your hosting platform:")
        print("   - Vercel + Supabase (Recommended for beginners)")
        print("   - Railway (Simple full-stack)")
        print("   - Heroku (Traditional)")
        print("   - DigitalOcean App Platform (Performance)")
        print("\n2. Setup database:")
        print("   - Supabase: Free PostgreSQL with web interface")
        print("   - Railway: Managed PostgreSQL")
        print("   - Heroku: Heroku Postgres add-on")
        print("\n3. Configure environment variables")
        print("4. Deploy your application")
        print("\n📖 For detailed instructions, see: deployment/supabase_setup.md")
    
    def run(self):
        """Main menu loop"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (0-7): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    self.check_requirements()
                elif choice == '2':
                    self.create_env_file()
                elif choice == '3':
                    self.setup_vercel()
                elif choice == '4':
                    self.setup_railway()
                elif choice == '5':
                    self.setup_heroku()
                elif choice == '6':
                    self.test_database_connection()
                elif choice == '7':
                    self.show_deployment_guide()
                else:
                    print("❌ Invalid choice. Please enter 0-7.")
                
                if choice != '0':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

if __name__ == '__main__':
    helper = DeploymentHelper()
    helper.run()
