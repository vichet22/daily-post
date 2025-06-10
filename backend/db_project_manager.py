#!/usr/bin/env python3
"""
Database Project Manager for Daily Post
A comprehensive tool to manage database projects and connections
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import psycopg2
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Create a separate Flask app for database management
db_app = Flask(__name__,
               template_folder='../frontend/db_templates',
               static_folder='../frontend/static')

# Configure Flask app for sessions
db_app.config['SECRET_KEY'] = secrets.token_hex(16)
db_app.config['SESSION_PERMANENT'] = False

# Default admin credentials (in production, store these securely)
ADMIN_CREDENTIALS = {
    'admin': generate_password_hash('admin123'),
    'dbadmin': generate_password_hash('database2024'),
    'manager': generate_password_hash('manager456')
}

def login_required(f):
    """Decorator to require login for protected routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(username, password):
    """Authenticate user credentials"""
    if username in ADMIN_CREDENTIALS:
        return check_password_hash(ADMIN_CREDENTIALS[username], password)
    return False

# File upload configuration
db_app.config['UPLOAD_FOLDER'] = '../frontend/static/images'
db_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class DatabaseManager:
    def __init__(self):
        self.connections = {
            'postgresql': {
                'host': 'localhost',
                'port': 5432,
                'database': 'daily_post',
                'user': 'dailypost_user',
                'password': 'dailypost123'
            },
            'sqlite': {
                'database': '../backend/instance/news.db'
            }
        }
    
    def get_postgresql_connection(self):
        """Get PostgreSQL connection"""
        try:
            config = self.connections['postgresql']
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            return conn
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            return None
    
    def get_sqlite_connection(self):
        """Get SQLite connection"""
        try:
            db_path = self.connections['sqlite']['database']
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                return conn
            else:
                print(f"SQLite database not found: {db_path}")
                return None
        except Exception as e:
            print(f"SQLite connection failed: {e}")
            return None
    
    def execute_query(self, db_type, query):
        """Execute a query on the specified database"""
        try:
            if db_type == 'postgresql':
                conn = self.get_postgresql_connection()
            elif db_type == 'sqlite':
                conn = self.get_sqlite_connection()
            else:
                return {'error': 'Invalid database type'}
            
            if not conn:
                return {'error': f'Could not connect to {db_type} database'}
            
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = {
                    'columns': columns,
                    'rows': rows,
                    'count': len(rows)
                }
            else:
                conn.commit()
                result = {'message': 'Query executed successfully', 'rowcount': cursor.rowcount}
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_table_info(self, db_type):
        """Get information about tables in the database"""
        try:
            if db_type == 'postgresql':
                query = """
                SELECT table_name, column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
                """
            elif db_type == 'sqlite':
                # For SQLite, we'll get table names first, then describe each
                conn = self.get_sqlite_connection()
                if not conn:
                    return {'error': 'Could not connect to SQLite database'}
                
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                table_info = {}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    table_info[table_name] = columns
                
                cursor.close()
                conn.close()
                return {'tables': table_info}
            
            result = self.execute_query(db_type, query)
            return result
            
        except Exception as e:
            return {'error': str(e)}

# Initialize database manager
db_manager = DatabaseManager()

@db_app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if authenticate_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('db_home'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')

@db_app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

@db_app.route('/')
@login_required
def db_home():
    """Database project home page"""
    return render_template('db_home.html')

@db_app.route('/connect/<db_type>')
@login_required
def connect_db(db_type):
    """Test database connection"""
    if db_type == 'postgresql':
        conn = db_manager.get_postgresql_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': f'Connected to PostgreSQL', 'version': version})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to PostgreSQL'})
    
    elif db_type == 'sqlite':
        conn = db_manager.get_sqlite_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': f'Connected to SQLite', 'version': version})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to connect to SQLite'})
    
    return jsonify({'status': 'error', 'message': 'Invalid database type'})

@db_app.route('/query', methods=['POST'])
@login_required
def execute_query():
    """Execute a database query"""
    data = request.get_json()
    db_type = data.get('db_type')
    query = data.get('query')
    
    if not db_type or not query:
        return jsonify({'error': 'Database type and query are required'})
    
    result = db_manager.execute_query(db_type, query)
    return jsonify(result)

@db_app.route('/tables/<db_type>')
def get_tables(db_type):
    """Get table information"""
    result = db_manager.get_table_info(db_type)
    return jsonify(result)

@db_app.route('/export/<db_type>')
def export_data(db_type):
    """Export database data"""
    try:
        if db_type == 'postgresql':
            # Export PostgreSQL data
            result = db_manager.execute_query(db_type, "SELECT * FROM post ORDER BY id;")
        elif db_type == 'sqlite':
            # Export SQLite data
            result = db_manager.execute_query(db_type, "SELECT * FROM post ORDER BY id;")
        else:
            return jsonify({'error': 'Invalid database type'})

        if 'error' in result:
            return jsonify(result)

        # Convert to exportable format
        export_data = {
            'database_type': db_type,
            'export_date': datetime.now().isoformat(),
            'table': 'post',
            'columns': result['columns'],
            'data': result['rows']
        }

        return jsonify(export_data)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/posts/<db_type>')
def get_posts(db_type):
    """Get all posts for management"""
    try:
        query = "SELECT id, title, author, category, featured, date_posted FROM post ORDER BY id DESC;"
        result = db_manager.execute_query(db_type, query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/post/<db_type>/<int:post_id>')
def get_post(db_type, post_id):
    """Get single post for editing"""
    try:
        query = f"SELECT * FROM post WHERE id = {post_id};"
        result = db_manager.execute_query(db_type, query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/update_post', methods=['POST'])
def update_post():
    """Update a post"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        post_id = data.get('id')
        title = data.get('title', '').replace("'", "''")
        content = data.get('content', '').replace("'", "''")
        author = data.get('author', '').replace("'", "''")
        category = data.get('category', '')
        featured = data.get('featured', False)
        image_url = data.get('image_url', '').replace("'", "''")

        query = f"""
        UPDATE post SET
            title = '{title}',
            content = '{content}',
            author = '{author}',
            category = '{category}',
            featured = {featured},
            image_url = '{image_url}'
        WHERE id = {post_id};
        """

        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/delete_post', methods=['POST'])
def delete_post():
    """Delete a post"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        post_id = data.get('id')

        query = f"DELETE FROM post WHERE id = {post_id};"
        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/categories/<db_type>')
@login_required
def get_categories(db_type):
    """Get all categories with post counts"""
    try:
        query = """
        SELECT category, COUNT(*) as post_count
        FROM post
        GROUP BY category
        ORDER BY category;
        """
        result = db_manager.execute_query(db_type, query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/update_category', methods=['POST'])
def update_category():
    """Update/rename a category across all posts"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        old_category = data.get('old_category', '').replace("'", "''")
        new_category = data.get('new_category', '').replace("'", "''")

        if not old_category or not new_category:
            return jsonify({'error': 'Both old and new category names are required'})

        if old_category == new_category:
            return jsonify({'error': 'New category name must be different from the old one'})

        query = f"""
        UPDATE post SET category = '{new_category}'
        WHERE category = '{old_category}';
        """

        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/delete_category', methods=['POST'])
def delete_category():
    """Delete a category and handle posts"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        category = data.get('category', '').replace("'", "''")
        action = data.get('action', 'move_to_general')  # 'move_to_general' or 'delete_posts'

        if not category:
            return jsonify({'error': 'Category name is required'})

        if action == 'delete_posts':
            # Delete all posts in this category
            query = f"DELETE FROM post WHERE category = '{category}';"
        else:
            # Move posts to 'General' category
            query = f"UPDATE post SET category = 'General' WHERE category = '{category}';"

        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/delete_database', methods=['POST'])
def delete_database():
    """Delete the SQLite database file"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')

        # Only allow deletion of SQLite database for safety
        if db_type != 'sqlite':
            return jsonify({'error': 'Only SQLite database deletion is allowed for safety reasons'})

        # Get the SQLite database path
        sqlite_path = db_manager.connections['sqlite']['database']

        # Check if file exists
        if not os.path.exists(sqlite_path):
            return jsonify({'error': 'SQLite database file not found'})

        # Delete the database file
        os.remove(sqlite_path)

        return jsonify({
            'message': 'SQLite database deleted successfully',
            'deleted_file': sqlite_path
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/create_category', methods=['POST'])
@login_required
def create_category():
    """Create a new category by creating a sample post"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        category = data.get('category', '').replace("'", "''")

        if not category:
            return jsonify({'error': 'Category name is required'})

        # Check if category already exists
        check_query = f"SELECT COUNT(*) FROM post WHERE category = '{category}';"
        check_result = db_manager.execute_query(db_type, check_query)

        if check_result.get('rows') and check_result['rows'][0][0] > 0:
            return jsonify({'error': f'Category "{category}" already exists'})

        # Create a sample post with the new category
        title = f"Welcome to {category}"
        content = f"This is a sample post for the {category} category. You can edit or delete this post and create new ones in this category."
        author = "Admin"

        if db_type == 'postgresql':
            query = f"""
            INSERT INTO post (title, content, author, category, featured, image_url, date_posted)
            VALUES ('{title}', '{content}', '{author}', '{category}', false, '', NOW());
            """
        else:
            query = f"""
            INSERT INTO post (title, content, author, category, featured, image_url, date_posted)
            VALUES ('{title}', '{content}', '{author}', '{category}', false, '', datetime('now'));
            """

        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/upload_image', methods=['POST'])
def upload_image():
    """Handle image upload"""
    try:
        if 'image_file' not in request.files:
            return jsonify({'error': 'No file selected'})

        file = request.files['image_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid filename conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            # Create upload directory if it doesn't exist
            os.makedirs(db_app.config['UPLOAD_FOLDER'], exist_ok=True)

            file_path = os.path.join(db_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Return the URL path for the uploaded image
            image_url = f'/static/images/{filename}'
            return jsonify({'success': True, 'image_url': image_url, 'filename': filename})
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files.'})

    except Exception as e:
        return jsonify({'error': str(e)})

@db_app.route('/create_post', methods=['POST'])
def create_post():
    """Create a new post"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        title = data.get('title', '').replace("'", "''")
        content = data.get('content', '').replace("'", "''")
        author = data.get('author', 'Admin').replace("'", "''")
        category = data.get('category', 'General')
        featured = data.get('featured', False)
        image_url = data.get('image_url', '').replace("'", "''")

        if db_type == 'postgresql':
            query = f"""
            INSERT INTO post (title, content, author, category, featured, image_url, date_posted)
            VALUES ('{title}', '{content}', '{author}', '{category}', {featured}, '{image_url}', NOW());
            """
        else:
            query = f"""
            INSERT INTO post (title, content, author, category, featured, image_url, date_posted)
            VALUES ('{title}', '{content}', '{author}', '{category}', {featured}, '{image_url}', datetime('now'));
            """

        result = db_manager.execute_query(db_type, query)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

def create_db_templates():
    """Create database management templates"""
    os.makedirs('db_templates', exist_ok=True)

    # Create login template
    login_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Project Manager - Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px 15px 0 0;
        }
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .btn-login {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .btn-login:hover {
            transform: translateY(-2px);
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="card login-card">
                    <div class="card-header login-header text-center py-4">
                        <h3 class="mb-0">
                            <i class="fas fa-database me-2"></i>
                            Database Manager
                        </h3>
                        <p class="mb-0 mt-2 opacity-75">Secure Access Portal</p>
                    </div>
                    <div class="card-body p-4">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% if messages %}
                                {% for category, message in messages %}
                                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                        <i class="fas fa-{{ 'exclamation-triangle' if category == 'error' else 'check-circle' if category == 'success' else 'info-circle' }} me-2"></i>
                                        {{ message }}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                    </div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}

                        <form method="POST">
                            <div class="mb-3">
                                <label for="username" class="form-label">
                                    <i class="fas fa-user me-2"></i>Username
                                </label>
                                <input type="text" class="form-control" id="username" name="username" required
                                       placeholder="Enter your username" autocomplete="username">
                            </div>
                            <div class="mb-4">
                                <label for="password" class="form-label">
                                    <i class="fas fa-lock me-2"></i>Password
                                </label>
                                <input type="password" class="form-control" id="password" name="password" required
                                       placeholder="Enter your password" autocomplete="current-password">
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-login">
                                    <i class="fas fa-sign-in-alt me-2"></i>Login
                                </button>
                            </div>
                        </form>
                    </div>
                    <div class="card-footer text-center py-3 bg-transparent">
                        <small class="text-muted">
                            <i class="fas fa-shield-alt me-1"></i>
                            Secure Database Management System
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

    # Create main template
    db_home_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Project Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .db-card { transition: transform 0.2s; }
        .db-card:hover { transform: translateY(-5px); }
        .query-result { max-height: 400px; overflow-y: auto; }
        .status-success { color: #28a745; }
        .status-error { color: #dc3545; }
        .post-row { cursor: pointer; }
        .post-row:hover { background-color: #f8f9fa; }
        .modal-lg { max-width: 800px; }
        .btn-group-sm .btn { padding: 0.25rem 0.5rem; font-size: 0.875rem; }
        .hidden { display: none; }
    </style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand">
                <i class="fas fa-database me-2"></i>Database Project Manager
            </span>
            <div class="navbar-nav ms-auto">
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle text-white" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user me-1"></i>{{ session.username if session.username else 'User' }}
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="/logout">
                            <i class="fas fa-sign-out-alt me-2"></i>Logout
                        </a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-6">
                <div class="card db-card">
                    <div class="card-header bg-primary text-white">
                        <h5><i class="fas fa-elephant me-2"></i>PostgreSQL Database</h5>
                    </div>
                    <div class="card-body">
                        <p>Daily Post Production Database</p>
                        <button type="button" class="btn btn-primary" onclick="connectDB('postgresql')">
                            <i class="fas fa-plug me-2"></i>Connect
                        </button>
                        <button type="button" class="btn btn-info" onclick="showTables('postgresql')">
                            <i class="fas fa-table me-2"></i>Tables
                        </button>
                        <button type="button" class="btn btn-success" onclick="exportData('postgresql')">
                            <i class="fas fa-download me-2"></i>Export
                        </button>
                        <button type="button" class="btn btn-warning" onclick="managePosts('postgresql')">
                            <i class="fas fa-edit me-2"></i>Manage Posts
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="manageCategories('postgresql')">
                            <i class="fas fa-tags me-2"></i>Categories
                        </button>
                        <div id="postgresql-status" class="mt-2"></div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card db-card">
                    <div class="card-header bg-secondary text-white">
                        <h5><i class="fas fa-database me-2"></i>SQLite Database</h5>
                    </div>
                    <div class="card-body">
                        <p>Legacy SQLite Database</p>
                        <button type="button" class="btn btn-secondary" onclick="connectDB('sqlite')">
                            <i class="fas fa-plug me-2"></i>Connect
                        </button>
                        <button type="button" class="btn btn-info" onclick="showTables('sqlite')">
                            <i class="fas fa-table me-2"></i>Tables
                        </button>
                        <button type="button" class="btn btn-success" onclick="exportData('sqlite')">
                            <i class="fas fa-download me-2"></i>Export
                        </button>
                        <button type="button" class="btn btn-warning" onclick="managePosts('sqlite')">
                            <i class="fas fa-edit me-2"></i>Manage Posts
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="manageCategories('sqlite')">
                            <i class="fas fa-tags me-2"></i>Categories
                        </button>
                        <button type="button" class="btn btn-danger" onclick="deleteSQLiteDatabase()">
                            <i class="fas fa-trash me-2"></i>Delete Database
                        </button>
                        <div id="sqlite-status" class="mt-2"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Post Management Section -->
        <div class="row mt-4 hidden" id="postManagement">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-edit me-2"></i>Post Management</h5>
                        <div>
                            <button type="button" class="btn btn-success btn-sm" onclick="showCreateModal()">
                                <i class="fas fa-plus me-2"></i>New Post
                            </button>
                            <button type="button" class="btn btn-secondary btn-sm" onclick="hidePostManagement()">
                                <i class="fas fa-times me-2"></i>Close
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div id="postsTable"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-terminal me-2"></i>Query Console</h5>
                    </div>
                    <div class="card-body">
                        <div class="row mb-3">
                            <div class="col-md-3">
                                <select class="form-select" id="queryDbType" title="Select Database Type" aria-label="Database Type">
                                    <option value="postgresql">PostgreSQL</option>
                                    <option value="sqlite">SQLite</option>
                                </select>
                            </div>
                            <div class="col-md-9">
                                <button type="button" class="btn btn-primary" onclick="executeQuery()">
                                    <i class="fas fa-play me-2"></i>Execute Query
                                </button>
                                <button type="button" class="btn btn-secondary" onclick="clearQuery()">
                                    <i class="fas fa-trash me-2"></i>Clear
                                </button>
                            </div>
                        </div>
                        <textarea class="form-control mb-3" id="queryText" rows="4" 
                                  placeholder="Enter SQL query here...">SELECT * FROM post LIMIT 10;</textarea>
                        <div id="queryResult" class="query-result"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit Post Modal -->
    <div class="modal fade" id="editPostModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editPostForm">
                        <input type="hidden" id="editPostId">
                        <input type="hidden" id="editDbType">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <label for="editTitle" class="form-label">Title</label>
                                <input type="text" class="form-control" id="editTitle" required>
                            </div>
                            <div class="col-md-4">
                                <label for="editCategory" class="form-label">Category</label>
                                <select class="form-select" id="editCategory">
                                    <option value="News">News</option>
                                    <option value="Technology">Technology</option>
                                    <option value="Business">Business</option>
                                    <option value="Sports">Sports</option>
                                    <option value="Entertainment">Entertainment</option>
                                    <option value="General">General</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label for="editAuthor" class="form-label">Author</label>
                                <input type="text" class="form-control" id="editAuthor">
                            </div>
                            <div class="col-md-6">
                                <label for="editImageUrl" class="form-label">Image URL</label>
                                <input type="url" class="form-control" id="editImageUrl" placeholder="Enter image URL or upload below">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-12">
                                <label for="editImageFile" class="form-label">Or Upload New Image</label>
                                <div class="input-group">
                                    <input type="file" class="form-control" id="editImageFile" accept="image/*">
                                    <button type="button" class="btn btn-outline-secondary" onclick="uploadImage('edit')">
                                        <i class="fas fa-upload"></i> Upload
                                    </button>
                                </div>
                                <div class="form-text">Supported formats: PNG, JPG, JPEG, GIF, WEBP (Max: 16MB)</div>
                                <div id="editUploadStatus" class="mt-2"></div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="editContent" class="form-label">Content</label>
                            <textarea class="form-control" id="editContent" rows="6" required></textarea>
                        </div>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="editFeatured">
                                <label class="form-check-label" for="editFeatured">Featured Post</label>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="updatePost()">Update Post</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Category Management Modal -->
    <div class="modal fade" id="categoryModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-tags me-2"></i>Category Management</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" title="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h6>Categories</h6>
                                <div>
                                    <button type="button" class="btn btn-success btn-sm me-2" onclick="showCreateCategory()">
                                        <i class="fas fa-plus me-1"></i>Create Category
                                    </button>
                                    <span class="badge bg-info" id="categoryDbType"></span>
                                </div>
                            </div>
                            <div id="categoriesTable">
                                <div class="text-center">
                                    <div class="spinner-border" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Create Category Modal -->
    <div class="modal fade" id="createCategoryModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-plus me-2"></i>Create New Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" title="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="createCategoryForm">
                        <input type="hidden" id="createCategoryDbType">
                        <div class="mb-3">
                            <label for="createCategoryName" class="form-label">Category Name</label>
                            <input type="text" class="form-control" id="createCategoryName" required placeholder="Enter category name">
                            <div class="form-text">A sample post will be created to establish this category.</div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" onclick="createCategory()">
                        <i class="fas fa-plus me-2"></i>Create Category
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Edit Category Modal -->
    <div class="modal fade" id="editCategoryModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-edit me-2"></i>Edit Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" title="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editCategoryForm">
                        <input type="hidden" id="editCategoryDbType">
                        <input type="hidden" id="editCategoryOldName">
                        <div class="mb-3">
                            <label for="editCategoryNewName" class="form-label">Category Name</label>
                            <input type="text" class="form-control" id="editCategoryNewName" required>
                            <div class="form-text">This will update all posts using this category.</div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="updateCategory()">
                        <i class="fas fa-save me-2"></i>Update Category
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Category Modal -->
    <div class="modal fade" id="deleteCategoryModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"><i class="fas fa-trash me-2"></i>Delete Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" title="Close"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="deleteCategoryDbType">
                    <input type="hidden" id="deleteCategoryName">
                    <p>What would you like to do with posts in the "<strong id="deleteCategoryDisplayName"></strong>" category?</p>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="deleteAction" id="moveToGeneral" value="move_to_general" checked>
                        <label class="form-check-label" for="moveToGeneral">
                            Move posts to "General" category
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="deleteAction" id="deletePosts" value="delete_posts">
                        <label class="form-check-label" for="deletePosts">
                            Delete all posts in this category
                        </label>
                    </div>
                    <div class="alert alert-warning mt-3">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        This action cannot be undone!
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" onclick="deleteCategory()">
                        <i class="fas fa-trash me-2"></i>Delete Category
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Create Post Modal -->
    <div class="modal fade" id="createPostModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Create New Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="createPostForm">
                        <input type="hidden" id="createDbType">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <label for="createTitle" class="form-label">Title</label>
                                <input type="text" class="form-control" id="createTitle" required>
                            </div>
                            <div class="col-md-4">
                                <label for="createCategory" class="form-label">Category</label>
                                <select class="form-select" id="createCategory">
                                    <option value="News">News</option>
                                    <option value="Technology">Technology</option>
                                    <option value="Business">Business</option>
                                    <option value="Sports">Sports</option>
                                    <option value="Entertainment">Entertainment</option>
                                    <option value="General">General</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label for="createAuthor" class="form-label">Author</label>
                                <input type="text" class="form-control" id="createAuthor" value="Admin">
                            </div>
                            <div class="col-md-6">
                                <label for="createImageUrl" class="form-label">Image URL</label>
                                <input type="url" class="form-control" id="createImageUrl" placeholder="Enter image URL or upload below">
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-12">
                                <label for="createImageFile" class="form-label">Or Upload Image</label>
                                <div class="input-group">
                                    <input type="file" class="form-control" id="createImageFile" accept="image/*">
                                    <button type="button" class="btn btn-outline-secondary" onclick="uploadImage('create')">
                                        <i class="fas fa-upload"></i> Upload
                                    </button>
                                </div>
                                <div class="form-text">Supported formats: PNG, JPG, JPEG, GIF, WEBP (Max: 16MB)</div>
                                <div id="createUploadStatus" class="mt-2"></div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="createContent" class="form-label">Content</label>
                            <textarea class="form-control" id="createContent" rows="6" required></textarea>
                        </div>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="createFeatured">
                                <label class="form-check-label" for="createFeatured">Featured Post</label>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" onclick="createPost()">Create Post</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function connectDB(dbType) {
            fetch(`/connect/${dbType}`)
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById(`${dbType}-status`);
                    if (data.status === 'success') {
                        statusDiv.innerHTML = `<small class="status-success"><i class="fas fa-check-circle"></i> ${data.message}</small>`;
                    } else {
                        statusDiv.innerHTML = `<small class="status-error"><i class="fas fa-times-circle"></i> ${data.message}</small>`;
                    }
                });
        }

        function executeQuery() {
            const dbType = document.getElementById('queryDbType').value;
            const query = document.getElementById('queryText').value;
            
            fetch('/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({db_type: dbType, query: query})
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('queryResult');
                if (data.error) {
                    resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                } else if (data.columns) {
                    let html = '<div class="table-responsive"><table class="table table-striped table-sm">';
                    html += '<thead><tr>';
                    data.columns.forEach(col => html += `<th>${col}</th>`);
                    html += '</tr></thead><tbody>';
                    data.rows.forEach(row => {
                        html += '<tr>';
                        row.forEach(cell => html += `<td>${cell || ''}</td>`);
                        html += '</tr>';
                    });
                    html += '</tbody></table></div>';
                    html += `<small class="text-muted">${data.count} rows returned</small>`;
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                }
            });
        }

        function clearQuery() {
            document.getElementById('queryText').value = '';
            document.getElementById('queryResult').innerHTML = '';
        }

        function showTables(dbType) {
            fetch(`/tables/${dbType}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Tables:', data);
                    alert(`Table information logged to console for ${dbType}`);
                });
        }

        function exportData(dbType) {
            fetch(`/export/${dbType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(`Export failed: ${data.error}`);
                    } else {
                        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `${dbType}_export_${new Date().toISOString().split('T')[0]}.json`;
                        a.click();
                    }
                });
        }

        // Post Management Functions
        let currentDbType = 'postgresql';

        function managePosts(dbType) {
            currentDbType = dbType;
            document.getElementById('postManagement').classList.remove('hidden');
            loadPosts(dbType);
        }

        function manageCategories(dbType) {
            currentDbType = dbType;
            document.getElementById('categoryDbType').textContent = dbType.toUpperCase();
            loadCategories(dbType);
            new bootstrap.Modal(document.getElementById('categoryModal')).show();
        }

        function loadCategories(dbType) {
            fetch(`/categories/${dbType}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('categoriesTable').innerHTML =
                        `<div class="alert alert-danger">${data.error}</div>`;
                } else {
                    displayCategories(data, dbType);
                }
            });
        }

        function displayCategories(data, dbType) {
            let html = '<div class="table-responsive"><table class="table table-striped table-hover">';
            html += '<thead class="table-dark"><tr>';
            html += '<th>Category</th><th>Post Count</th><th>Actions</th>';
            html += '</tr></thead><tbody>';

            data.rows.forEach(row => {
                const [category, postCount] = row;
                html += `<tr>
                    <td><span class="badge bg-secondary fs-6">${category}</span></td>
                    <td><span class="badge bg-info">${postCount} posts</span></td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editCategory('${category}', '${dbType}')" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="confirmDeleteCategory('${category}', '${dbType}')" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>`;
            });

            html += '</tbody></table></div>';
            html += `<small class="text-muted">${data.rows.length} categories found</small>`;
            document.getElementById('categoriesTable').innerHTML = html;
        }

        function showCreateCategory() {
            document.getElementById('createCategoryDbType').value = currentDbType;
            document.getElementById('createCategoryName').value = '';
            new bootstrap.Modal(document.getElementById('createCategoryModal')).show();
        }

        function createCategory() {
            const categoryData = {
                db_type: document.getElementById('createCategoryDbType').value,
                category: document.getElementById('createCategoryName').value.trim()
            };

            if (!categoryData.category) {
                alert('Please enter a category name');
                return;
            }

            fetch('/create_category', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(categoryData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Create failed: ${data.error}`);
                } else {
                    alert('Category created successfully!');
                    bootstrap.Modal.getInstance(document.getElementById('createCategoryModal')).hide();
                    loadCategories(currentDbType);
                }
            });
        }

        function editCategory(categoryName, dbType) {
            document.getElementById('editCategoryDbType').value = dbType;
            document.getElementById('editCategoryOldName').value = categoryName;
            document.getElementById('editCategoryNewName').value = categoryName;
            new bootstrap.Modal(document.getElementById('editCategoryModal')).show();
        }

        function updateCategory() {
            const categoryData = {
                db_type: document.getElementById('editCategoryDbType').value,
                old_category: document.getElementById('editCategoryOldName').value,
                new_category: document.getElementById('editCategoryNewName').value
            };

            fetch('/update_category', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(categoryData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Update failed: ${data.error}`);
                } else {
                    alert('Category updated successfully!');
                    bootstrap.Modal.getInstance(document.getElementById('editCategoryModal')).hide();
                    loadCategories(currentDbType);
                }
            });
        }

        function confirmDeleteCategory(categoryName, dbType) {
            document.getElementById('deleteCategoryDbType').value = dbType;
            document.getElementById('deleteCategoryName').value = categoryName;
            document.getElementById('deleteCategoryDisplayName').textContent = categoryName;
            new bootstrap.Modal(document.getElementById('deleteCategoryModal')).show();
        }

        function deleteCategory() {
            const action = document.querySelector('input[name="deleteAction"]:checked').value;
            const categoryData = {
                db_type: document.getElementById('deleteCategoryDbType').value,
                category: document.getElementById('deleteCategoryName').value,
                action: action
            };

            fetch('/delete_category', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(categoryData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Delete failed: ${data.error}`);
                } else {
                    const actionText = action === 'delete_posts' ? 'deleted with all posts' : 'deleted (posts moved to General)';
                    alert(`Category ${actionText} successfully!`);
                    bootstrap.Modal.getInstance(document.getElementById('deleteCategoryModal')).hide();
                    loadCategories(currentDbType);
                }
            });
        }

        function hidePostManagement() {
            document.getElementById('postManagement').classList.add('hidden');
        }

        function loadPosts(dbType) {
            fetch(`/posts/${dbType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('postsTable').innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    } else {
                        displayPosts(data, dbType);
                    }
                });
        }

        function displayPosts(data, dbType) {
            let html = '<div class="table-responsive"><table class="table table-striped table-hover">';
            html += '<thead class="table-dark"><tr>';
            html += '<th>ID</th><th>Title</th><th>Author</th><th>Category</th><th>Featured</th><th>Date</th><th>Actions</th>';
            html += '</tr></thead><tbody>';

            data.rows.forEach(row => {
                const [id, title, author, category, featured, date_posted] = row;
                const featuredBadge = featured ? '<span class="badge bg-warning">Featured</span>' : '';
                const shortTitle = title.length > 40 ? title.substring(0, 40) + '...' : title;
                const formattedDate = new Date(date_posted).toLocaleDateString();

                html += `<tr class="post-row">
                    <td>${id}</td>
                    <td>${shortTitle}</td>
                    <td>${author || 'N/A'}</td>
                    <td><span class="badge bg-secondary">${category}</span></td>
                    <td>${featuredBadge}</td>
                    <td>${formattedDate}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editPost(${id}, '${dbType}')" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deletePost(${id}, '${dbType}')" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>`;
            });

            html += '</tbody></table></div>';
            html += `<small class="text-muted">${data.rows.length} posts found</small>`;
            document.getElementById('postsTable').innerHTML = html;
        }

        function editPost(postId, dbType) {
            fetch(`/post/${dbType}/${postId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(`Error loading post: ${data.error}`);
                    } else {
                        const post = data.rows[0];
                        document.getElementById('editPostId').value = post[0];
                        document.getElementById('editDbType').value = dbType;
                        document.getElementById('editTitle').value = post[1];
                        document.getElementById('editContent').value = post[2];
                        document.getElementById('editAuthor').value = post[3];
                        document.getElementById('editCategory').value = post[5];
                        document.getElementById('editFeatured').checked = post[6];
                        document.getElementById('editImageUrl').value = post[7] || '';
                        document.getElementById('editUploadStatus').innerHTML = '';
                        document.getElementById('editImageFile').value = '';

                        new bootstrap.Modal(document.getElementById('editPostModal')).show();
                    }
                });
        }

        function updatePost() {
            const postData = {
                db_type: document.getElementById('editDbType').value,
                id: document.getElementById('editPostId').value,
                title: document.getElementById('editTitle').value,
                content: document.getElementById('editContent').value,
                author: document.getElementById('editAuthor').value,
                category: document.getElementById('editCategory').value,
                featured: document.getElementById('editFeatured').checked,
                image_url: document.getElementById('editImageUrl').value
            };

            fetch('/update_post', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Update failed: ${data.error}`);
                } else {
                    alert('Post updated successfully!');
                    bootstrap.Modal.getInstance(document.getElementById('editPostModal')).hide();
                    loadPosts(currentDbType);
                }
            });
        }

        function deletePost(postId, dbType) {
            if (confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
                fetch('/delete_post', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({db_type: dbType, id: postId})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(`Delete failed: ${data.error}`);
                    } else {
                        alert('Post deleted successfully!');
                        loadPosts(currentDbType);
                    }
                });
            }
        }

        function showCreateModal() {
            document.getElementById('createDbType').value = currentDbType;
            document.getElementById('createPostForm').reset();
            document.getElementById('createAuthor').value = 'Admin';
            document.getElementById('createUploadStatus').innerHTML = '';
            document.getElementById('createImageFile').value = '';
            new bootstrap.Modal(document.getElementById('createPostModal')).show();
        }

        function uploadImage(modalType) {
            const fileInput = document.getElementById(modalType + 'ImageFile');
            const statusDiv = document.getElementById(modalType + 'UploadStatus');
            const imageUrlInput = document.getElementById(modalType + 'ImageUrl');

            if (!fileInput.files[0]) {
                statusDiv.innerHTML = '<small class="text-danger">Please select a file first.</small>';
                return;
            }

            const formData = new FormData();
            formData.append('image_file', fileInput.files[0]);

            statusDiv.innerHTML = '<small class="text-info"><i class="fas fa-spinner fa-spin"></i> Uploading...</small>';

            fetch('/upload_image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    statusDiv.innerHTML = `<small class="text-danger"><i class="fas fa-times"></i> ${data.error}</small>`;
                } else {
                    statusDiv.innerHTML = `<small class="text-success"><i class="fas fa-check"></i> Upload successful!</small>`;
                    imageUrlInput.value = data.image_url;
                    fileInput.value = ''; // Clear the file input
                }
            })
            .catch(error => {
                statusDiv.innerHTML = `<small class="text-danger"><i class="fas fa-times"></i> Upload failed: ${error}</small>`;
            });
        }

        function createPost() {
            const postData = {
                db_type: document.getElementById('createDbType').value,
                title: document.getElementById('createTitle').value,
                content: document.getElementById('createContent').value,
                author: document.getElementById('createAuthor').value,
                category: document.getElementById('createCategory').value,
                featured: document.getElementById('createFeatured').checked,
                image_url: document.getElementById('createImageUrl').value
            };

            fetch('/create_post', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(`Create failed: ${data.error}`);
                } else {
                    alert('Post created successfully!');
                    bootstrap.Modal.getInstance(document.getElementById('createPostModal')).hide();
                    loadPosts(currentDbType);
                }
            });
        }

        function deleteSQLiteDatabase() {
            if (confirm('⚠️ WARNING: This will permanently delete the entire SQLite database and all its data!\\n\\nThis action cannot be undone. Are you absolutely sure you want to proceed?')) {
                if (confirm('🔴 FINAL CONFIRMATION: Delete the SQLite database permanently?')) {
                    fetch('/delete_database', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({db_type: 'sqlite'})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert(`Delete failed: ${data.error}`);
                        } else {
                            alert('✅ SQLite database deleted successfully!\\n\\nDeleted file: ' + data.deleted_file);
                            // Update the status to show database is deleted
                            document.getElementById('sqlite-status').innerHTML =
                                '<small class="status-error"><i class="fas fa-times-circle"></i> Database deleted</small>';
                        }
                    })
                    .catch(error => {
                        alert(`Delete failed: ${error}`);
                    });
                }
            }
        }
    </script>
</body>
</html>'''
    
    with open('db_templates/db_home.html', 'w', encoding='utf-8') as f:
        f.write(db_home_template)

    # Save login template
    with open('db_templates/login.html', 'w', encoding='utf-8') as f:
        f.write(login_template)

if __name__ == '__main__':
    print("🗄️ Database Project Manager")
    print("=" * 50)
    
    # Create templates
    create_db_templates()
    print("✅ Database templates created")
    
    # Start the database management server
    print("🚀 Starting Database Project Manager...")
    print("📊 Access your database project at: http://localhost:5001")
    print("\nFeatures available:")
    print("- PostgreSQL connection and management")
    print("- SQLite database access")
    print("- Query console")
    print("- Data export")
    print("- Table information")
    
    db_app.run(debug=True, host='0.0.0.0', port=5001)
