#!/usr/bin/env python3
"""
Daily Post Deployment Helper
Helps you deploy your Daily Post application to various hosting platforms
"""

import os
import sys
import secrets
import subprocess
import webbrowser

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def check_git_status():
    """Check if git repository is clean"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        return len(result.stdout.strip()) == 0
    except:
        return False

def show_deployment_options():
    """Show available deployment options"""
    print("\n" + "="*60)
    print("🚀 DAILY POST DEPLOYMENT HELPER")
    print("="*60)
    print("\nChoose your hosting platform:")
    print()
    print("1. 🚂 Railway (Recommended - $5/month)")
    print("   - Built-in PostgreSQL")
    print("   - Easy deployment")
    print("   - Great for production")
    print()
    print("2. 🎨 Render (Free tier available)")
    print("   - Free tier with limitations")
    print("   - Good for testing")
    print("   - Managed PostgreSQL")
    print()
    print("3. 🟣 Heroku (Classic choice)")
    print("   - Reliable platform")
    print("   - PostgreSQL add-on")
    print("   - Good documentation")
    print()
    print("4. ⚡ Vercel (Already configured)")
    print("   - Serverless functions")
    print("   - Need external database")
    print("   - Good for static sites")
    print()
    print("5. 🔑 Generate Secret Key")
    print("6. 📖 Show Environment Variables")
    print("7. ❌ Exit")
    print()

def deploy_railway():
    """Guide for Railway deployment"""
    print("\n🚂 RAILWAY DEPLOYMENT")
    print("="*40)
    print("\n1. Go to: https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your Daily Post repository")
    print("5. Add PostgreSQL database service")
    print("6. Set environment variables (see option 6)")
    print("7. Deploy!")
    print("\n💡 Railway will automatically detect your Procfile and deploy!")
    
    choice = input("\nOpen Railway website? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://railway.app')

def deploy_render():
    """Guide for Render deployment"""
    print("\n🎨 RENDER DEPLOYMENT")
    print("="*40)
    print("\n1. Go to: https://render.com")
    print("2. Connect GitHub repository")
    print("3. Create Web Service")
    print("4. Build Command: pip install -r requirements.txt")
    print("5. Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT")
    print("6. Add PostgreSQL database")
    print("7. Set environment variables")
    
    choice = input("\nOpen Render website? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://render.com')

def deploy_heroku():
    """Guide for Heroku deployment"""
    print("\n🟣 HEROKU DEPLOYMENT")
    print("="*40)
    print("\nCommands to run:")
    print("1. heroku create your-app-name")
    print("2. heroku addons:create heroku-postgresql:mini")
    print("3. heroku config:set SECRET_KEY=your-secret-key")
    print("4. heroku config:set FLASK_ENV=production")
    print("5. git push heroku main")
    
    choice = input("\nOpen Heroku website? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://heroku.com')

def deploy_vercel():
    """Guide for Vercel deployment"""
    print("\n⚡ VERCEL DEPLOYMENT")
    print("="*40)
    print("\nYour app is already configured for Vercel!")
    print("Current URL: https://daily-post-six.vercel.app")
    print("\nTo redeploy:")
    print("1. Install Vercel CLI: npm i -g vercel")
    print("2. Run: vercel --prod")
    print("3. Set environment variables in Vercel dashboard")
    
    choice = input("\nOpen Vercel dashboard? (y/n): ").lower()
    if choice == 'y':
        webbrowser.open('https://vercel.com/dashboard')

def show_env_variables():
    """Show required environment variables"""
    secret_key = generate_secret_key()
    
    print("\n🔑 ENVIRONMENT VARIABLES")
    print("="*40)
    print("\nSet these in your hosting platform:")
    print()
    print(f"SECRET_KEY={secret_key}")
    print("DB_HOST=your-postgresql-host")
    print("DB_NAME=daily_post")
    print("DB_USER=your-database-user")
    print("DB_PASSWORD=your-secure-database-password")
    print("DB_PORT=5432")
    print("FLASK_ENV=production")
    print("UPLOAD_FOLDER=/tmp/uploads")
    print("MAX_CONTENT_LENGTH=16777216")
    print()
    print("💡 Copy these values to your hosting platform's environment variables section")

def main():
    """Main deployment helper"""
    print("🗞️  Daily Post Deployment Helper")
    print("Preparing your application for hosting...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend/app.py'):
        print("❌ Error: Please run this script from the Daily Post root directory")
        return
    
    while True:
        show_deployment_options()
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                deploy_railway()
            elif choice == '2':
                deploy_render()
            elif choice == '3':
                deploy_heroku()
            elif choice == '4':
                deploy_vercel()
            elif choice == '5':
                secret_key = generate_secret_key()
                print(f"\n🔑 Generated Secret Key:")
                print(f"{secret_key}")
                print("\n💡 Use this as your SECRET_KEY environment variable")
            elif choice == '6':
                show_env_variables()
            elif choice == '7':
                print("👋 Happy deploying!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
            
            if choice != '7':
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
