# Database Projects Overview

## 🗄️ Available Database Projects

You now have access to multiple database projects and management tools:

### 1. **Daily Post PostgreSQL Database** (Primary)
- **Type**: PostgreSQL 17.5
- **Database**: `daily_post`
- **Host**: localhost:5432
- **User**: `dailypost_user`
- **Status**: ✅ Active and Running
- **Purpose**: Production database for Daily Post application

#### **Tables & Data:**
- **post** table with 8 records
- **Categories**: News, Technology, Business, Sports, Entertainment, General
- **Features**: Full-text search, ACID compliance, concurrent access

#### **Access Methods:**
- **Web App**: http://localhost:5000 (Daily Post application)
- **Database Manager**: http://localhost:5001 (Database Project Manager)
- **Direct Connection**: `psql -U dailypost_user -d daily_post`

### 2. **Legacy SQLite Database** (Archive)
- **Type**: SQLite
- **File**: `instance/news.db`
- **Status**: ✅ Available (Legacy)
- **Purpose**: Original database before PostgreSQL migration

#### **Access Methods:**
- **Database Manager**: http://localhost:5001
- **Direct Access**: SQLite browser tools
- **Command Line**: `sqlite3 instance/news.db`

### 3. **Database Project Manager** (Tool)
- **Type**: Web-based management interface
- **URL**: http://localhost:5001
- **Status**: ✅ Running
- **Purpose**: Unified database management and exploration

#### **Features:**
- **Connection Testing**: Test PostgreSQL and SQLite connections
- **Query Console**: Execute SQL queries on both databases
- **Table Explorer**: View table structures and data
- **Data Export**: Export data in JSON format
- **Real-time Results**: Interactive query execution

## 🛠️ Database Management Tools

### **Database Project Manager** (http://localhost:5001)
A comprehensive web interface providing:

#### **Connection Management**
- ✅ PostgreSQL connection testing
- ✅ SQLite connection testing
- ✅ Real-time status indicators
- ✅ Version information display

#### **Query Console**
- ✅ Multi-database query execution
- ✅ Syntax highlighting interface
- ✅ Tabular result display
- ✅ Error handling and reporting

#### **Data Operations**
- ✅ Table structure exploration
- ✅ Data export functionality
- ✅ Query result pagination
- ✅ Real-time query execution

#### **Export Capabilities**
- ✅ JSON data export
- ✅ Timestamped exports
- ✅ Complete table dumps
- ✅ Structured data format

### **Command Line Tools**

#### **PostgreSQL Tools**
```bash
# Connect to database
psql -U dailypost_user -d daily_post

# Database backup
pg_dump -U dailypost_user daily_post > backup.sql

# Database restore
psql -U dailypost_user daily_post < backup.sql

# Check server status
pg_isready
```

#### **SQLite Tools**
```bash
# Open SQLite database
sqlite3 instance/news.db

# Export to SQL
sqlite3 instance/news.db .dump > sqlite_backup.sql

# Show tables
sqlite3 instance/news.db ".tables"
```

## 📊 Database Statistics

### **PostgreSQL Database (daily_post)**
- **Total Posts**: 8
- **Categories**: 6 unique categories
- **Featured Posts**: 4
- **Database Size**: ~50KB (with sample data)
- **Performance**: Optimized for concurrent access

### **SQLite Database (news.db)**
- **Status**: Legacy/Archive
- **Size**: Variable (depends on previous data)
- **Purpose**: Historical data reference

## 🚀 Quick Start Guide

### **1. Access Database Project Manager**
```
Open: http://localhost:5001
```

### **2. Test Connections**
- Click "Connect" for PostgreSQL
- Click "Connect" for SQLite
- Verify green status indicators

### **3. Execute Queries**
- Select database type (PostgreSQL/SQLite)
- Enter SQL query in console
- Click "Execute Query"
- View results in table format

### **4. Export Data**
- Click "Export" for desired database
- Download JSON file with complete data
- Use for backups or data analysis

## 🔧 Advanced Operations

### **Database Migrations**
```bash
# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback migrations
flask db downgrade
```

### **Performance Monitoring**
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('daily_post'));

-- View active connections
SELECT * FROM pg_stat_activity;

-- Check table sizes
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats WHERE tablename = 'post';
```

### **Data Analysis Queries**
```sql
-- Posts by category
SELECT category, COUNT(*) as count 
FROM post GROUP BY category ORDER BY count DESC;

-- Featured posts
SELECT title, author, category 
FROM post WHERE featured = true;

-- Recent posts
SELECT title, date_posted 
FROM post ORDER BY date_posted DESC LIMIT 5;
```

## 📱 Integration Options

### **API Access**
- **All Posts**: http://localhost:5000/api/posts
- **Single Post**: http://localhost:5000/api/post/[id]
- **JSON Format**: Structured data for external applications

### **Web Interface**
- **Main App**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Category Views**: http://localhost:5000/category/[category]

### **Database Tools**
- **Project Manager**: http://localhost:5001
- **Query Console**: Interactive SQL execution
- **Export Tools**: Data backup and analysis

## 🎯 Next Steps

1. **Explore Database Manager**: Use http://localhost:5001 to interact with databases
2. **Run Sample Queries**: Test the query console with different SQL commands
3. **Export Data**: Create backups using the export functionality
4. **Monitor Performance**: Use built-in PostgreSQL monitoring queries
5. **Develop Features**: Use the database tools to plan new application features

Your database projects are now fully accessible and manageable through multiple interfaces!
