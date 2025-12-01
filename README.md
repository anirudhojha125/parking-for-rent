# Smart Park System

A modern parking space sharing platform built with Flask and designed to work with XAMPP MySQL.

## Features

- User registration and authentication
- List and search for parking spaces
- Real-time booking system
- Payment processing
- Admin panel for system management
- Responsive design for all devices

## Prerequisites

- XAMPP (with MySQL service)
- Python 3.7+
- pip (Python package installer)

## Installation

1. **Install XAMPP**
   - Download and install XAMPP from [https://www.apachefriends.org/index.html](https://www.apachefriends.org/index.html)
   - Make sure to include MySQL in your installation

2. **Clone or download this repository**
   ```
   git clone <repository-url>
   ```

3. **Install Python dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - Double-click `setup_database.bat` to create the database and tables
   - Or run from command line:
     ```
     python init_db.py
     ```

## Running the Application

1. **Start XAMPP services**
   - Open XAMPP Control Panel
   - Start MySQL service

2. **Run the application**
   - Double-click `start_app.bat`
   - Or run from command line:
     ```
     python app.py
     ```

3. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## Database Configuration

The application is configured to work with XAMPP MySQL using these settings:
- Host: localhost
- Port: 3306
- Username: root
- Password: (empty)
- Database: smart_park_system

To modify these settings, update the `app.py` file:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/smart_park_system'
```

## Project Structure

```
smart_park_system/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── setup_database.bat  # Database setup script
├── start_app.bat       # Application startup script
├── init_db.py          # Database initialization script
├── models/             # Database models
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── forms/              # Form definitions
└── README.md           # This file
```

## Troubleshooting

### Database Connection Issues
- Ensure XAMPP MySQL is running
- Check that the database name is correct
- Verify MySQL is using port 3306 (default XAMPP setting)

### Missing Dependencies
- Run `pip install -r requirements.txt` to install all required packages

### Port Conflicts
- If port 5000 is in use, modify `app.py` to use a different port:
  ```python
  app.run(debug=True, port=5001)
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.