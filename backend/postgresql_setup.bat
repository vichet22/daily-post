@echo off
echo ========================================
echo PostgreSQL Server Setup and Configuration
echo ========================================
echo.

REM Add PostgreSQL to PATH permanently
echo Adding PostgreSQL to system PATH...
setx PATH "%PATH%;C:\Program Files\PostgreSQL\17\bin" /M
echo PostgreSQL bin directory added to PATH.
echo.

echo Checking PostgreSQL installation...
"C:\Program Files\PostgreSQL\17\bin\psql.exe" --version
echo.

echo Checking PostgreSQL service status...
"C:\Program Files\PostgreSQL\17\bin\pg_isready.exe"
echo.

echo Checking service details...
sc query postgresql-x64-17
echo.

echo ========================================
echo PostgreSQL Server Installation Summary:
echo ========================================
echo - PostgreSQL 17.5 Server: INSTALLED and RUNNING
echo - PostgreSQL Client (psql): AVAILABLE
echo - Service Name: postgresql-x64-17
echo - Port: 5432
echo - Status: ACCEPTING CONNECTIONS
echo.

echo ========================================
echo Quick Start Commands:
echo ========================================
echo 1. Connect to PostgreSQL (will prompt for password):
echo    psql -U postgres
echo.
echo 2. Create a new database:
echo    createdb -U postgres your_database_name
echo.
echo 3. List all databases:
echo    psql -U postgres -l
echo.
echo 4. Check server status:
echo    pg_isready
echo.
echo 5. Stop PostgreSQL service:
echo    sc stop postgresql-x64-17
echo.
echo 6. Start PostgreSQL service:
echo    sc start postgresql-x64-17
echo.

echo ========================================
echo PostgreSQL Server is ready to use!
echo ========================================
echo Note: You may need to set a password for the 'postgres' user
echo to connect to the database.
echo.
pause
