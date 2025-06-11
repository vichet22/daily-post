from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# PostgreSQL Database Configuration
# You can set these as environment variables for production
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'database': os.environ.get('DB_NAME', 'daily_post'),
    'user': os.environ.get('DB_USER', 'dailypost_user'),
    'password': os.environ.get('DB_PASSWORD', 'dailypost123')
}

# Construct PostgreSQL URI
POSTGRESQL_URI = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# File upload configuration
app.config['UPLOAD_FOLDER'] = '../frontend/static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='Admin')
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    category = db.Column(db.String(50), nullable=False, default='General')
    featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(500), nullable=True)  # For image URL or uploaded image path
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=5, error_out=False)
    featured_posts = Post.query.filter_by(featured=True).order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', posts=posts, featured_posts=featured_posts)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/admin')
def admin():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin.html', posts=posts)

@app.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author'] or 'Admin'
        category = request.form['category'] or 'General'
        featured = 'featured' in request.form
        image_url = request.form.get('image_url', '')

        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Create upload directory if it doesn't exist
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(file_path)
                image_url = f'/static/images/{filename}'

        post = Post(title=title, content=content, author=author,
                   category=category, featured=featured, image_url=image_url)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('new_post.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.category = request.form['category']
        post.featured = 'featured' in request.form

        # Handle image update
        image_url = request.form.get('image_url', '')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(file_path)
                image_url = f'/static/images/{filename}'

        if image_url:
            post.image_url = image_url

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('edit_post.html', post=post)

@app.route('/admin/delete/<int:id>')
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        posts = Post.query.filter(
            Post.title.contains(query) | Post.content.contains(query)
        ).order_by(Post.date_posted.desc()).all()
    else:
        posts = []
    return render_template('search.html', posts=posts, query=query)

@app.route('/category/<category>')
def category(category):
    posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).all()
    return render_template('category.html', posts=posts, category=category)

# API Routes
@app.route('/api/posts')
def api_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
        'author': post.author,
        'date_posted': post.date_posted.isoformat(),
        'category': post.category,
        'featured': post.featured,
        'image_url': post.image_url
    } for post in posts])

@app.route('/api/post/<int:id>')
def api_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author,
        'date_posted': post.date_posted.isoformat(),
        'category': post.category,
        'featured': post.featured,
        'image_url': post.image_url
    })

def create_sample_data():
    """Create sample data if database is empty"""
    if Post.query.count() == 0:
        print("Creating sample data...")
        sample_posts = [
            Post(
                title="Welcome to Daily Post with PostgreSQL!",
                content="Your Daily Post application is now running on PostgreSQL! This provides better performance, scalability, and features compared to SQLite. You can now handle more concurrent users and larger datasets.",
                author="Admin",
                category="Announcement",
                featured=True,
                image_url="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=400&fit=crop"
            ),
            Post(
                title="PostgreSQL Features",
                content="PostgreSQL offers advanced features like ACID compliance, foreign keys, joins, views, triggers, and stored procedures. It's perfect for production applications that need reliability and performance.",
                author="Admin",
                category="Technology",
                featured=True,
                image_url="https://images.unsplash.com/photo-1432888622747-4eb9a8efeb07?w=800&h=400&fit=crop"
            ),
            Post(
                title="Database Migration Complete",
                content="Your application has been successfully migrated from SQLite to PostgreSQL. All your data structure is preserved, and you now have access to enterprise-grade database features.",
                author="Admin",
                category="Update",
                featured=False,
                image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop"
            )
        ]

        for post in sample_posts:
            db.session.add(post)

        db.session.commit()
        print(f"✅ Created {len(sample_posts)} sample posts!")

if __name__ == '__main__':
    with app.app_context():
        try:
            # Test database connection
            with db.engine.connect() as connection:
                connection.execute(db.text("SELECT 1"))
            print("✅ PostgreSQL connection successful!")

            # Create tables if they don't exist
            db.create_all()
            print("✅ Database tables created/verified!")

            # Create sample data if needed
            create_sample_data()

        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("💡 Make sure PostgreSQL is running and the database 'daily_post' exists")
            print("💡 Check your database credentials in the configuration")
            exit(1)

    print("🚀 Starting Daily Post application on PostgreSQL...")
    app.run(debug=True, host='0.0.0.0', port=5000)
