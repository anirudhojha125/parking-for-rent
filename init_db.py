import pymysql
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Database configuration for XAMPP MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': 3306,
    'charset': 'utf8mb4'
}

DATABASE_NAME = 'smart_park_system'

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database first
        config_without_db = DB_CONFIG.copy()
        conn = pymysql.connect(**config_without_db)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' created or already exists.")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def initialize_tables():
    """Initialize tables in the database"""
    try:
        # Connect to the specific database
        db_config_with_db = DB_CONFIG.copy()
        db_config_with_db['database'] = DATABASE_NAME
        conn = pymysql.connect(**db_config_with_db)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL,
                phone VARCHAR(20),
                is_verified BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE,
                is_main_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create parking_spaces table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_spaces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                address VARCHAR(300) NOT NULL,
                latitude FLOAT,
                longitude FLOAT,
                price_per_hour FLOAT NOT NULL,
                availability_start TIME NOT NULL,
                availability_end TIME NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                owner_id INT NOT NULL,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create parking_images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_url VARCHAR(500) NOT NULL,
                is_primary BOOLEAN DEFAULT FALSE,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                parking_space_id INT NOT NULL,
                FOREIGN KEY (parking_space_id) REFERENCES parking_spaces(id) ON DELETE CASCADE
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                start_time DATETIME NOT NULL,
                end_time DATETIME NOT NULL,
                total_price FLOAT NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                customer_id INT NOT NULL,
                owner_id INT NOT NULL,
                parking_space_id INT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (parking_space_id) REFERENCES parking_spaces(id) ON DELETE CASCADE
            )
        ''')
        
        # Create feedbacks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rating INT NOT NULL,
                comment TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                booking_id INT NOT NULL,
                FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("All tables created successfully.")
        return True
    except Exception as e:
        print(f"Error initializing tables: {e}")
        return False

def main():
    """Main function to create database and initialize tables"""
    print("Initializing Smart Park System database for XAMPP MySQL...")
    
    if create_database():
        print("Database creation successful.")
        if initialize_tables():
            print("Database initialization completed successfully!")
        else:
            print("Failed to initialize tables.")
    else:
        print("Failed to create database.")

if __name__ == "__main__":
    main()