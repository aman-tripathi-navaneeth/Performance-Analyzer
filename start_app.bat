@echo off
echo ========================================
echo 🚀 Performance Analyzer v2 - Startup
echo ========================================
echo.

echo 📦 Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python start_dev.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo ✅ Both servers are starting up!
echo ========================================
echo.
echo 📍 Backend: http://localhost:5000
echo 📍 Frontend: http://localhost:3000
echo.
echo 🔑 Login Credentials:
echo    Email: aman@gmail.com
echo    Password: aman123
echo.
echo Press any key to open the application...
pause > nul

start http://localhost:3000 