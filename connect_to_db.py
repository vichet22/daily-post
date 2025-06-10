#!/usr/bin/env python3
"""
Connect to PostgreSQL Database and provide interactive access
"""

import psycopg2
import sys
from datetime import datetime

def connect_to_database():
    """Connect to the PostgreSQL database"""
    try:
        # Database connection parameters
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'daily_post',
            'user': 'dailypost_user',
            'password': 'dailypost123'
        }
        
        print("🔌 Connecting to PostgreSQL database...")
        print(f"Host: {conn_params['host']}:{conn_params['port']}")
        print(f"Database: {conn_params['database']}")
        print(f"User: {conn_params['user']}")
        
        # Establish connection
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("✅ Successfully connected to PostgreSQL!")
        
        # Get database version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"📊 Database version: {version[:50]}...")
        
        # Get current database info
        cursor.execute("SELECT current_database(), current_user, current_timestamp;")
        db_info = cursor.fetchone()
        print(f"📋 Database: {db_info[0]}")
        print(f"👤 User: {db_info[1]}")
        print(f"🕒 Time: {db_info[2]}")
        
        return conn, cursor
        
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None, None

def show_database_info(cursor):
    """Display database information"""
    print("\n" + "="*60)
    print("📊 DATABASE INFORMATION")
    print("="*60)
    
    try:
        # Show tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📋 Tables: {[table[0] for table in tables]}")
        
        # Show post count
        cursor.execute("SELECT COUNT(*) FROM post;")
        post_count = cursor.fetchone()[0]
        print(f"📝 Total posts: {post_count}")
        
        # Show categories
        cursor.execute("SELECT DISTINCT category FROM post ORDER BY category;")
        categories = cursor.fetchall()
        print(f"📂 Categories: {[cat[0] for cat in categories]}")
        
        # Show featured posts
        cursor.execute("SELECT COUNT(*) FROM post WHERE featured = true;")
        featured_count = cursor.fetchone()[0]
        print(f"⭐ Featured posts: {featured_count}")
        
        # Show recent posts
        print(f"\n📰 Recent posts:")
        cursor.execute("""
            SELECT id, title, author, category, date_posted 
            FROM post 
            ORDER BY date_posted DESC 
            LIMIT 5;
        """)
        recent_posts = cursor.fetchall()
        
        for post in recent_posts:
            print(f"  {post[0]:2d}. {post[1][:40]:<40} | {post[2]:<15} | {post[3]:<12}")
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")

def execute_sample_queries(cursor):
    """Execute some sample queries"""
    print("\n" + "="*60)
    print("🔍 SAMPLE QUERIES")
    print("="*60)
    
    queries = [
        {
            'name': 'Posts by Category',
            'sql': 'SELECT category, COUNT(*) as count FROM post GROUP BY category ORDER BY count DESC;'
        },
        {
            'name': 'Featured Posts',
            'sql': 'SELECT title, author, category FROM post WHERE featured = true;'
        },
        {
            'name': 'Latest Posts',
            'sql': 'SELECT title, date_posted FROM post ORDER BY date_posted DESC LIMIT 3;'
        }
    ]
    
    for query in queries:
        try:
            print(f"\n📊 {query['name']}:")
            print(f"SQL: {query['sql']}")
            cursor.execute(query['sql'])
            results = cursor.fetchall()
            
            if results:
                for row in results:
                    print(f"  {row}")
            else:
                print("  No results found")
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")

def interactive_mode(conn, cursor):
    """Interactive SQL mode"""
    print("\n" + "="*60)
    print("💻 INTERACTIVE SQL MODE")
    print("="*60)
    print("Enter SQL queries (type 'exit' to quit, 'help' for commands)")
    print("Examples:")
    print("  SELECT * FROM post LIMIT 3;")
    print("  SELECT COUNT(*) FROM post;")
    print("  \\dt  (show tables)")
    
    while True:
        try:
            query = input("\ndaily_post=# ").strip()
            
            if query.lower() in ['exit', 'quit', '\\q']:
                print("👋 Goodbye!")
                break
            elif query.lower() in ['help', '\\h']:
                print("Available commands:")
                print("  SELECT * FROM post;     - Show all posts")
                print("  \\dt                     - Show tables")
                print("  \\d post                 - Describe post table")
                print("  exit                    - Quit")
                continue
            elif query == '\\dt':
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                tables = cursor.fetchall()
                print("Tables:")
                for table in tables:
                    print(f"  {table[0]}")
                continue
            elif query == '\\d post':
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = 'post' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print("Post table structure:")
                for col in columns:
                    print(f"  {col[0]:<20} {col[1]:<20} {col[2]}")
                continue
            elif not query:
                continue
            
            # Execute the query
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if results:
                    # Get column names
                    columns = [desc[0] for desc in cursor.description]
                    print(f"Columns: {columns}")
                    print("-" * 50)
                    for row in results:
                        print(row)
                    print(f"\n({len(results)} rows)")
                else:
                    print("No results found")
            else:
                conn.commit()
                print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🐘 PostgreSQL Database Connection Tool")
    print("=" * 60)
    
    # Connect to database
    conn, cursor = connect_to_database()
    
    if not conn:
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure PostgreSQL server is running")
        print("2. Verify the database 'daily_post' exists")
        print("3. Check if user 'dailypost_user' has proper permissions")
        print("4. Try connecting as postgres user first")
        return
    
    try:
        # Show database information
        show_database_info(cursor)
        
        # Execute sample queries
        execute_sample_queries(cursor)
        
        # Interactive mode
        interactive_mode(conn, cursor)
        
    finally:
        # Close connections
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("🔌 Database connection closed")

if __name__ == '__main__':
    main()
