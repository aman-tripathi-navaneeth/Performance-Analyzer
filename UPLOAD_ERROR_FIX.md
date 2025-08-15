# 🔧 Upload Error Fix Guide

## 🐛 **The Problem**
You're getting these errors when trying to upload files:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
Error uploading file: AxiosError
Upload error: Error: Failed to upload file
```

This means your **React frontend can't connect to the Flask backend**.

## ✅ **Step-by-Step Fix**

### **Step 1: Start the Backend Server**

Open a **new terminal/command prompt** and run:

```bash
cd backend
python start_backend_simple.py
```

**You should see:**
```
🚀 Starting Flask Backend Server...
📍 Backend URL: http://localhost:5000
✅ CORS enabled for React frontend (port 3000)
* Running on http://127.0.0.1:5000
* Debugger PIN: xxx-xxx-xxx
```

**⚠️ IMPORTANT**: Keep this terminal open! The server must stay running.

### **Step 2: Verify Backend is Running**

Open your browser and go to: `http://localhost:5000/api/v1/cors/health`

**You should see:**
```json
{
  "success": true,
  "message": "Backend server is running!",
  "status": "healthy"
}
```

### **Step 3: Test Upload Endpoint**

Go to: `http://localhost:5000/api/v1/upload/subject`

**You should see:**
```json
{
  "success": false,
  "error": "No file provided"
}
```
*(This error is normal - it means the endpoint is working but needs a file)*

### **Step 4: Start Frontend (if not already running)**

In a **second terminal**:
```bash
cd frontend
npm start
```

### **Step 5: Test File Upload**

1. Go to your React app: `http://localhost:3000`
2. Navigate to the Upload page
3. Try uploading one of the test CSV files
4. Check the browser console - no more connection errors!

## 🔍 **Troubleshooting**

### **If Backend Won't Start:**

#### **Missing Dependencies Error:**
```bash
cd backend
pip install flask flask-sqlalchemy flask-cors pandas openpyxl python-dotenv
```

#### **Port 5000 Already in Use:**
```bash
# Check what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### **Python Path Issues:**
```bash
cd backend
python -m pip install --upgrade pip
python -c "import flask; print('Flask installed successfully')"
```

### **If Frontend Can't Connect:**

#### **Check Backend URL in Frontend:**
The frontend should be connecting to `http://localhost:5000/api/v1`

#### **Clear Browser Cache:**
- Hard refresh: `Ctrl + F5`
- Or open Developer Tools → Network tab → check "Disable cache"

#### **Check CORS Headers:**
In browser Developer Tools → Network tab, look for:
- `Access-Control-Allow-Origin: http://localhost:3000`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`

## 🚀 **Quick Start Commands**

### **Terminal 1 (Backend):**
```bash
cd backend
python start_backend_simple.py
```

### **Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

### **Terminal 3 (Test - Optional):**
```bash
python backend/test_server_running.py
```

## 📊 **Expected Results After Fix**

### **Backend Terminal Should Show:**
```
🚀 Starting Flask Backend Server...
📍 Backend URL: http://localhost:5000
✅ CORS enabled for React frontend (port 3000)
* Running on http://127.0.0.1:5000
```

### **Frontend Should Work:**
- No connection errors in browser console
- File upload form should work
- Success messages after upload
- Students should appear in the database

### **Upload Success Message:**
```json
{
  "success": true,
  "message": "File processed successfully",
  "data": {
    "students_processed": 20,
    "records_created": 20
  }
}
```

## 🎯 **Test Upload with Sample Data**

Once both servers are running, try uploading:

1. **Physics_2nd_Year_CSEA.csv**
   - Subject: `Physics`
   - Year: `2nd Year`
   - Section: `CSE A`

2. **Chemistry_2nd_Year_CSEA.csv**
   - Subject: `Chemistry`
   - Year: `2nd Year`
   - Section: `CSE A`

## ⚡ **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| `ERR_CONNECTION_REFUSED` | Backend not running - start with `python start_backend_simple.py` |
| `CORS Error` | Backend running but CORS not configured - use the enhanced startup script |
| `Module not found` | Install dependencies: `pip install flask flask-sqlalchemy flask-cors pandas openpyxl python-dotenv` |
| `Port already in use` | Kill existing process or use different port |
| `Upload fails silently` | Check backend logs in terminal for detailed error messages |

## 🔧 **Advanced Debugging**

### **Check Backend Logs:**
Watch the backend terminal for detailed logs during upload:
```
INFO:app.api.uploads:Received file upload request
INFO:app.services.data_processor:Successfully loaded CSV file with shape: (20, 6)
INFO:app.api.uploads:Created new student: 22A91A0501 - Aarav Sharma
```

### **Check Network Tab:**
In browser Developer Tools → Network tab:
- Look for failed requests (red entries)
- Check request/response headers
- Verify request URL is correct

### **Test API Directly:**
Use browser or Postman to test:
- `GET http://localhost:5000/api/v1/cors/health`
- `GET http://localhost:5000/api/v1/students`

The upload error should be completely resolved once both servers are running properly! 🎉