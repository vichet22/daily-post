#!/usr/bin/env python3
"""
Database Project Manager - User Management Tool
Utility to manage user credentials for the Database Project Manager
"""

from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

class UserManager:
    def __init__(self, credentials_file='db_credentials.json'):
        self.credentials_file = credentials_file
        self.load_credentials()
    
    def load_credentials(self):
        """Load credentials from file or create default ones"""
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                self.credentials = json.load(f)
        else:
            # Default credentials
            self.credentials = {
                'admin': generate_password_hash('admin123'),
                'dbadmin': generate_password_hash('database2024'),
                'manager': generate_password_hash('manager456')
            }
            self.save_credentials()
    
    def save_credentials(self):
        """Save credentials to file"""
        with open(self.credentials_file, 'w') as f:
            json.dump(self.credentials, f, indent=2)
        print(f"✅ Credentials saved to {self.credentials_file}")
    
    def add_user(self, username, password):
        """Add a new user"""
        if username in self.credentials:
            print(f"❌ User '{username}' already exists!")
            return False
        
        self.credentials[username] = generate_password_hash(password)
        self.save_credentials()
        print(f"✅ User '{username}' added successfully!")
        return True
    
    def update_password(self, username, new_password):
        """Update user password"""
        if username not in self.credentials:
            print(f"❌ User '{username}' not found!")
            return False
        
        self.credentials[username] = generate_password_hash(new_password)
        self.save_credentials()
        print(f"✅ Password updated for user '{username}'!")
        return True
    
    def remove_user(self, username):
        """Remove a user"""
        if username not in self.credentials:
            print(f"❌ User '{username}' not found!")
            return False
        
        if username == 'admin':
            print("❌ Cannot remove the admin user!")
            return False
        
        del self.credentials[username]
        self.save_credentials()
        print(f"✅ User '{username}' removed successfully!")
        return True
    
    def list_users(self):
        """List all users"""
        print("\n👥 Database Manager Users:")
        print("-" * 30)
        for i, username in enumerate(self.credentials.keys(), 1):
            print(f"{i}. {username}")
        print(f"\nTotal users: {len(self.credentials)}")
    
    def verify_password(self, username, password):
        """Verify user password"""
        if username not in self.credentials:
            return False
        return check_password_hash(self.credentials[username], password)
    
    def test_login(self, username, password):
        """Test login credentials"""
        if self.verify_password(username, password):
            print(f"✅ Login successful for user '{username}'!")
            return True
        else:
            print(f"❌ Login failed for user '{username}'!")
            return False

def main():
    """Main interactive menu"""
    user_manager = UserManager()
    
    while True:
        print("\n" + "=" * 50)
        print("🗄️ Database Project Manager - User Management")
        print("=" * 50)
        print("1. List all users")
        print("2. Add new user")
        print("3. Update user password")
        print("4. Remove user")
        print("5. Test login")
        print("6. Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            user_manager.list_users()
        
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if username and password:
                user_manager.add_user(username, password)
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '3':
            username = input("Enter username: ").strip()
            new_password = input("Enter new password: ").strip()
            if username and new_password:
                user_manager.update_password(username, new_password)
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '4':
            username = input("Enter username to remove: ").strip()
            if username:
                confirm = input(f"Are you sure you want to remove '{username}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    user_manager.remove_user(username)
            else:
                print("❌ Username cannot be empty!")
        
        elif choice == '5':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if username and password:
                user_manager.test_login(username, password)
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '6':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please enter 1-6.")

if __name__ == '__main__':
    main()
