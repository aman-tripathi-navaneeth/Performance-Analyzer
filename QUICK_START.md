# 🚀 Performance Analyzer v2 - Quick Start Guide

## ✅ What's Fixed
- ✅ Fixed broken dependencies in `requirements.txt`
- ✅ Created development startup script with hot reload
- ✅ Added comprehensive CORS configuration
- ✅ Fixed database initialization issues
- ✅ Created easy startup scripts

## 🎯 Quick Start (Windows)

### Option 1: One-Click Startup
```bash
# Double-click this file or run in command prompt:
start_app.bat
```

### Option 2: Manual Startup

#### 1. Start Backend Server
```bash
cd backend
python start_dev.py
```

#### 2. Start Frontend Server (in new terminal)
```bash
cd frontend
npm start
```

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/v1/cors/health

## 🔑 Login Credentials
- **Email**: aman@gmail.com
- **Password**: aman123

## 📊 Features Available

### For Teachers:
- 📈 **Dashboard**: View class performance overview
- 👥 **Students**: Browse and search students by year/section
- 📊 **Class Performance**: Detailed analytics for each class
- 📤 **Upload**: Upload Excel files with student data
- 👤 **Student Profiles**: Individual student performance analysis

### For Admins:
- 👨‍🏫 **Teacher Management**: Manage teacher accounts
- 📊 **System Analytics**: Overall system statistics
- 🔧 **Admin Dashboard**: Administrative controls

## 📁 Project Structure
```
performance-analyzer-v2-main/
├── backend/                 # Flask API server
│   ├── app/                # Main application code
│   ├── uploads/            # File upload storage
│   ├── sample_data/        # Test datasets
│   └── start_dev.py        # Development server
├── frontend/               # React application
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── package.json       # Dependencies
└── start_app.bat          # One-click startup
```

## 🛠️ Development

### Backend Development
- **Hot Reload**: Enabled (auto-restart on file changes)
- **Debug Mode**: Enabled with detailed error messages
- **Database**: SQLite with automatic table creation
- **CORS**: Configured for React development

### Frontend Development
- **Hot Reload**: React development server
- **API Integration**: Connected to backend at localhost:5000
- **Error Boundaries**: Comprehensive error handling

## 📊 Sample Data
The application includes sample datasets for testing:
- Mathematics (1st Year)
- Data Structures (2nd Year)
- Electronics (3rd Year)
- Operating Systems (4th Year)

## 🔧 Troubleshooting

### Backend Issues
1. **Port 5000 in use**: Change port in `start_dev.py`
2. **Database errors**: Delete `database.db` and restart
3. **Import errors**: Run `pip install -r requirements.txt`

### Frontend Issues
1. **Port 3000 in use**: React will automatically use next available port
2. **API connection**: Check if backend is running on port 5000
3. **Build errors**: Run `npm install` to install dependencies

### Common Solutions
```bash
# Reset everything
cd backend
rm database.db
python start_dev.py

# In another terminal:
cd frontend
npm install
npm start
```

## 🎉 Success Indicators
- ✅ Backend shows "🚀 STARTING FLASK DEVELOPMENT SERVER"
- ✅ Frontend shows "Local: http://localhost:3000"
- ✅ Can login with aman@gmail.com / aman123
- ✅ Can access Students page
- ✅ Can upload Excel files

## 📞 Support
If you encounter issues:
1. Check the console logs in both terminals
2. Verify all dependencies are installed
3. Ensure ports 3000 and 5000 are available
4. Check the troubleshooting section above

---
**🎯 The Performance Analyzer v2 is now ready to use!** 