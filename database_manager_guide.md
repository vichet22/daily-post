# Database Project Manager Guide

## 🎯 Using Your Database Project Manager Interface

You now have the Database Project Manager open at **http://localhost:5001**. Here's how to use all its features:

### 🔌 **Connection Testing**

#### **PostgreSQL Database (Left Panel)**
- **✅ Connect Button**: Test connection to your Daily Post production database
- **📊 Tables Button**: View table structure information (logged to browser console)
- **💾 Export Button**: Download complete database data as JSON

#### **SQLite Database (Right Panel)**
- **✅ Connect Button**: Test connection to legacy SQLite database
- **📊 Tables Button**: View SQLite table information
- **💾 Export Button**: Export SQLite data

### 💻 **Query Console (Bottom Panel)**

The query console allows you to execute SQL commands on either database:

#### **How to Use:**
1. **Select Database**: Choose PostgreSQL or SQLite from dropdown
2. **Enter Query**: Type SQL in the text area
3. **Execute**: Click "Execute Query" button
4. **View Results**: See formatted results below

#### **Sample Queries to Try:**

```sql
-- View all posts
SELECT * FROM post ORDER BY id;

-- Count posts by category
SELECT category, COUNT(*) as count 
FROM post 
GROUP BY category 
ORDER BY count DESC;

-- Get featured posts
SELECT id, title, author, category 
FROM post 
WHERE featured = true;

-- Recent posts with details
SELECT id, title, author, category, date_posted 
FROM post 
ORDER BY date_posted DESC 
LIMIT 5;

-- Search posts by title
SELECT id, title, category 
FROM post 
WHERE title ILIKE '%news%';

-- Get post statistics
SELECT 
    COUNT(*) as total_posts,
    COUNT(CASE WHEN featured = true THEN 1 END) as featured_posts,
    COUNT(DISTINCT category) as categories
FROM post;
```

### 📊 **Advanced Database Operations**

#### **Table Structure Queries:**
```sql
-- View table structure (PostgreSQL)
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'post' 
ORDER BY ordinal_position;

-- Check table size (PostgreSQL)
SELECT pg_size_pretty(pg_total_relation_size('post')) as table_size;

-- View indexes (PostgreSQL)
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'post';
```

#### **Data Analysis Queries:**
```sql
-- Posts per month
SELECT 
    DATE_TRUNC('month', date_posted) as month,
    COUNT(*) as posts_count
FROM post 
GROUP BY month 
ORDER BY month DESC;

-- Average content length by category
SELECT 
    category,
    AVG(LENGTH(content)) as avg_content_length,
    COUNT(*) as post_count
FROM post 
GROUP BY category;

-- Authors and their post counts
SELECT 
    author,
    COUNT(*) as post_count,
    COUNT(CASE WHEN featured = true THEN 1 END) as featured_count
FROM post 
GROUP BY author 
ORDER BY post_count DESC;
```

### 💾 **Data Export Features**

#### **Export Options:**
1. **JSON Export**: Click "Export" button to download structured data
2. **Query Results**: Copy results from query console
3. **Custom Exports**: Use SELECT queries to export specific data

#### **Export Data Structure:**
```json
{
  "database_type": "postgresql",
  "export_date": "2025-06-09T19:40:00",
  "table": "post",
  "columns": ["id", "title", "content", "author", "date_posted", "category", "featured", "image_url"],
  "data": [
    [1, "Post Title", "Content...", "Author", "2025-06-09", "Category", true, "image_url"]
  ]
}
```

### 🔍 **Troubleshooting Tips**

#### **If Connection Fails:**
- Ensure PostgreSQL server is running
- Check if Daily Post app is running (python app.py)
- Verify database credentials

#### **If Queries Fail:**
- Check SQL syntax
- Ensure table names are correct
- Verify column names match database schema

#### **Browser Console:**
- Press F12 to open developer tools
- Check Console tab for detailed table information
- View network requests for debugging

### 🚀 **Pro Tips**

#### **Efficient Querying:**
1. **Use LIMIT**: Add `LIMIT 10` to large queries
2. **Filter Early**: Use WHERE clauses to reduce data
3. **Index Usage**: Query by id or date_posted for best performance

#### **Data Exploration:**
1. **Start Simple**: Begin with `SELECT * FROM post LIMIT 5;`
2. **Build Complexity**: Add WHERE, GROUP BY, ORDER BY gradually
3. **Save Queries**: Keep useful queries in a text file

#### **Performance Monitoring:**
```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM post WHERE category = 'News';

-- View database statistics
SELECT * FROM pg_stat_user_tables WHERE relname = 'post';
```

### 📱 **Integration with Daily Post App**

Your Database Project Manager works alongside your Daily Post application:

- **Daily Post App**: http://localhost:5000 (User interface)
- **Database Manager**: http://localhost:5001 (Admin interface)
- **Both access the same PostgreSQL database**

#### **Workflow:**
1. **Create Content**: Use Daily Post app admin panel
2. **Analyze Data**: Use Database Manager for insights
3. **Monitor Performance**: Check database statistics
4. **Export Backups**: Regular data exports for safety

### 🎯 **Next Steps**

1. **Try Sample Queries**: Execute the provided SQL examples
2. **Explore Data**: Use different WHERE conditions
3. **Export Data**: Create backups of your content
4. **Monitor Growth**: Track posts and categories over time
5. **Optimize Performance**: Use EXPLAIN to understand query performance

Your Database Project Manager is a powerful tool for managing and analyzing your Daily Post database!
