@echo off
echo ========================================
echo Database Project Launcher
echo ========================================
echo.

echo Available Database Projects:
echo.
echo 1. Database Project Manager (Web Interface)
echo 2. PostgreSQL Command Line
echo 3. SQLite Browser
echo 4. Daily Post Application (with database)
echo 5. View Database Files
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto web_manager
if "%choice%"=="2" goto postgresql_cli
if "%choice%"=="3" goto sqlite_browser
if "%choice%"=="4" goto daily_post_app
if "%choice%"=="5" goto view_files

echo Invalid choice. Please try again.
pause
goto :eof

:web_manager
echo.
echo Starting Database Project Manager...
echo This will open a web interface at http://localhost:5001
echo.
python db_project_manager.py
goto :eof

:postgresql_cli
echo.
echo Opening PostgreSQL Command Line...
echo Database: daily_post
echo User: dailypost_user
echo.
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U dailypost_user -d daily_post
goto :eof

:sqlite_browser
echo.
echo Opening SQLite Database...
echo File: instance\news.db
echo.
if exist "instance\news.db" (
    "C:\Program Files\PostgreSQL\17\bin\psql.exe" --help >nul 2>&1
    if errorlevel 1 (
        echo SQLite command line tools not found.
        echo Opening file location instead...
        explorer instance
    ) else (
        echo Use: sqlite3 instance\news.db
        echo Or open the file with a SQLite browser tool
        explorer instance
    )
) else (
    echo SQLite database file not found!
    echo Creating instance directory...
    mkdir instance
    echo Please check if the database file exists.
)
goto :eof

:daily_post_app
echo.
echo Starting Daily Post Application...
echo This includes database access through the web interface
echo URL: http://localhost:5000
echo.
python app.py
goto :eof

:view_files
echo.
echo Database Project Files:
echo ========================================
dir /b *.py | findstr /i "db\|database\|init"
echo.
dir /b *.md | findstr /i "db\|database\|postgresql"
echo.
echo Database Directories:
if exist "instance" echo - instance\ (SQLite database)
if exist "migrations" echo - migrations\ (Database migrations)
if exist "db_templates" echo - db_templates\ (Database manager templates)
echo.
echo Configuration Files:
if exist ".env" echo - .env (Environment configuration)
if exist "requirements.txt" echo - requirements.txt (Python packages)
echo.
pause
goto :eof
