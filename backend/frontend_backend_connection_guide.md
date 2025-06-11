# Frontend-Backend Connection Guide

## 🔗 Connection Overview

Your Daily Post project now has a properly separated frontend and backend architecture with seamless integration.

## 📁 Project Structure

```
Daily Post/
├── frontend/                    # All UI Components
│   ├── templates/              # Main application templates
│   │   ├── base.html          # Base template with navigation
│   │   ├── index.html         # Homepage
│   │   ├── admin.html         # Admin panel
│   │   ├── post.html          # Individual post view
│   │   ├── edit_post.html     # Post editing
│   │   ├── new_post.html      # New post creation
│   │   ├── category.html      # Category view
│   │   └── search.html        # Search results
│   ├── db_templates/          # Database manager templates
│   │   ├── db_home.html       # Database manager interface
│   │   └── login.html         # Database manager login
│   └── static/                # Static assets
│       ├── css/
│       │   └── style.css      # Main stylesheet
│       ├── js/
│       │   └── main.js        # Frontend JavaScript
│       └── images/            # Uploaded images
├── backend/                    # All Server-Side Code
│   ├── app.py                 # Main Flask application
│   ├── db_project_manager.py  # Database management app
│   ├── requirements.txt       # Python dependencies
│   ├── instance/              # Database files
│   └── *.py                   # Other backend files
└── start_project.py           # Project launcher
```

## ⚙️ Flask Configuration

### Main Application (backend/app.py)
```python
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# File upload configuration
app.config['UPLOAD_FOLDER'] = '../frontend/static/images'
```

### Database Manager (backend/db_project_manager.py)
```python
db_app = Flask(__name__, 
               template_folder='../frontend/db_templates',
               static_folder='../frontend/static')

# File upload configuration
db_app.config['UPLOAD_FOLDER'] = '../frontend/static/images'
```

## 🌐 Application URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Main App** | http://localhost:5000 | Daily Post website |
| **Admin Panel** | http://localhost:5000/admin | Content management |
| **API** | http://localhost:5000/api/posts | JSON data access |
| **DB Manager** | http://localhost:5001 | Database administration |
| **DB Login** | http://localhost:5001/login | Database manager login |

## 🔧 How the Connection Works

### 1. **Template Rendering**
- Backend Flask apps serve HTML templates from frontend folders
- Templates use Jinja2 templating with shared base templates
- Dynamic content is passed from backend routes to frontend templates

### 2. **Static File Serving**
- CSS, JavaScript, and images served from `frontend/static/`
- Both applications share the same static assets
- URL routing: `/static/css/style.css` → `frontend/static/css/style.css`

### 3. **Image Uploads**
- Files uploaded through either application
- Stored in `frontend/static/images/`
- Accessible via `/static/images/filename.jpg`

### 4. **Database Integration**
- Backend handles all database operations
- Frontend templates display data passed from backend
- Real-time updates through form submissions and AJAX

## 🚀 Starting the Project

### Option 1: Use the Project Launcher
```bash
python start_project.py
```

### Option 2: Manual Start
```bash
# Terminal 1 - Main Application
cd backend
python app.py

# Terminal 2 - Database Manager
cd backend
python db_project_manager.py
```

## 📊 Features Available

### Main Application (Port 5000)
- ✅ Homepage with post listings
- ✅ Individual post views
- ✅ Category-based browsing
- ✅ Search functionality
- ✅ Admin panel for content management
- ✅ Post creation and editing
- ✅ Image upload support
- ✅ API endpoints for external access

### Database Manager (Port 5001)
- ✅ PostgreSQL and SQLite management
- ✅ Query console for direct SQL execution
- ✅ Post management interface
- ✅ Category management
- ✅ Data export functionality
- ✅ Table information viewer
- ✅ Secure login system

## 🔐 Database Manager Login

**Default Credentials:**
- Username: `admin` | Password: `admin123`
- Username: `dbadmin` | Password: `database2024`
- Username: `manager` | Password: `manager456`

## 🎯 Benefits of This Architecture

### **Separation of Concerns**
- Frontend: UI/UX, templates, styling, client-side logic
- Backend: Business logic, database operations, API endpoints

### **Maintainability**
- Easy to update frontend without touching backend
- Backend changes don't affect frontend structure
- Clear organization of files and responsibilities

### **Scalability**
- Frontend can be served by CDN in production
- Backend can be deployed on separate servers
- Easy to add new frontend frameworks (React, Vue) later

### **Development Workflow**
- Frontend developers work in `frontend/` folder
- Backend developers work in `backend/` folder
- Shared static assets prevent duplication

## 🔧 Customization

### Adding New Templates
1. Create HTML file in `frontend/templates/`
2. Extend `base.html` for consistent layout
3. Add route in `backend/app.py` to render template

### Adding New Static Assets
1. Add CSS files to `frontend/static/css/`
2. Add JS files to `frontend/static/js/`
3. Reference in templates using `{{ url_for('static', filename='...') }}`

### Database Operations
1. Use Database Manager for direct SQL operations
2. Add new routes in `backend/app.py` for application features
3. Update templates to display new data

## 🐛 Troubleshooting

### Templates Not Found
- Check `template_folder` path in Flask configuration
- Ensure templates exist in `frontend/templates/`

### Static Files Not Loading
- Check `static_folder` path in Flask configuration
- Verify files exist in `frontend/static/`

### Database Connection Issues
- Check PostgreSQL service is running
- Verify database credentials in configuration
- Use Database Manager to test connections

## 📈 Next Steps

1. **Development**: Use the project launcher to start both services
2. **Testing**: Create posts and test all functionality
3. **Customization**: Modify templates and styles as needed
4. **Production**: Deploy with proper web server (nginx + gunicorn)

Your frontend and backend are now properly connected and ready for development! 🎉
