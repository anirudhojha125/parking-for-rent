# Smart Park System Setup Guide

This guide will walk you through setting up the Smart Park System on your local machine using XAMPP.

## Prerequisites

Before you begin, ensure you have the following installed:
- Windows Operating System (Windows 10 or later recommended)
- XAMPP with MySQL
- Python 3.7 or later

## Step 1: Install XAMPP

1. Download XAMPP from [https://www.apachefriends.org/download.html](https://www.apachefriends.org/download.html)
2. Run the installer and follow the installation wizard
3. During installation, make sure to select MySQL (this is required)
4. Complete the installation process

## Step 2: Start XAMPP Services

1. Open XAMPP Control Panel
2. Click the "Start" button next to "Apache"
3. Click the "Start" button next to "MySQL"
4. Both services should show a green "Running" status

## Step 3: Install Python Dependencies

You have two options:

### Option A: Using the Batch File (Recommended)
1. Navigate to the `smart_park_system` folder
2. Double-click on `install_dependencies.bat`
3. Wait for the installation to complete

### Option B: Manual Installation
1. Open Command Prompt
2. Navigate to the `smart_park_system` folder:
   ```
   cd path\to\smart_park_system
   ```
3. Run the following command:
   ```
   pip install -r requirements.txt
   ```

## Step 4: Set Up the Database

1. Navigate to the `smart_park_system` folder
2. Double-click on `setup_database.bat`
3. The script will:
   - Check if XAMPP is installed
   - Start MySQL service if not already running
   - Create the `smart_park_system` database
   - Create all required tables

## Step 5: Run the Application

1. Navigate to the `smart_park_system` folder
2. Double-click on `start_app.bat`
3. The application will start and display a message indicating it's running on `http://localhost:5000`

## Step 6: Access the Application

1. Open your web browser
2. Go to `http://localhost:5000`
3. You should see the Smart Park System homepage

## Initial User Setup

To get started with the application:

1. Click "Register" to create a new account
2. Fill in the registration form with your details
3. After registering, you can:
   - List your parking spaces (if you have available spaces)
   - Search for parking spaces near your destination
   - Book parking spaces

## Admin Access

To access the admin panel:

1. Register a regular user account first
2. The first user registered will automatically become an admin
3. Log in with your admin account
4. Navigate to "Admin Panel" in the navigation menu

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Access denied for user 'root'@'localhost'"
Solution: Make sure XAMPP MySQL is running and that you haven't set a password for the root user.

#### Issue: "Port 5000 is already in use"
Solution: Edit `app.py` and change the port:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

#### Issue: "ModuleNotFoundError" when running the application
Solution: Make sure you've installed all dependencies using `install_dependencies.bat` or manually with pip.

#### Issue: Database connection errors
Solution:
1. Ensure XAMPP MySQL is running
2. Check that the database name is `smart_park_system`
3. Verify MySQL is using port 3306 (default XAMPP setting)

### Resetting the Database

If you need to reset the database:

1. Open phpMyAdmin (usually at `http://localhost/phpmyadmin`)
2. Delete the `smart_park_system` database
3. Run `setup_database.bat` again

## File Structure Overview

```
smart_park_system/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── install.py              # Python installation script
├── install_dependencies.bat # Batch file to install dependencies
├── setup_database.bat      # Batch file to set up database
├── start_app.bat           # Batch file to start application
├── init_db.py              # Database initialization script
├── models/                 # Database models
│   ├── database.py         # Database configuration
│   └── models.py           # Model definitions
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── forms/                  # Form definitions
├── admin.py                # Admin blueprint
├── auth.py                 # Authentication blueprint
├── parking.py              # Parking management blueprint
├── README.md               # Project overview
└── SETUP_GUIDE.md          # This file
```

## Support

For additional help, please contact:
- Email: support@smartpark.com
- Phone: +1 (555) 123-4567

## License

This project is licensed under the MIT License.