from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import bcrypt
from models.database import db

class User(db.Model, UserMixin):
    """User model for both parking space owners and customers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with parking spaces
    parking_spaces = db.relationship('ParkingSpace', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    # Relationship with bookings
    bookings_made = db.relationship('Booking', foreign_keys='Booking.customer_id', backref='customer', lazy=True)
    bookings_received = db.relationship('Booking', foreign_keys='Booking.owner_id', backref='booking_owner', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}>'

class ParkingSpace(db.Model):
    """Model for parking spaces listed by owners"""
    __tablename__ = 'parking_spaces'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    price_per_hour = db.Column(db.Float, nullable=False)
    availability_start = db.Column(db.Time, nullable=False)
    availability_end = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to owner
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='parking_space', lazy=True, cascade='all, delete-orphan')
    
    # Relationship with images
    images = db.relationship('ParkingImage', backref='parking_space', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingSpace {self.title}>'

class ParkingImage(db.Model):
    """Model for storing parking space images"""
    __tablename__ = 'parking_images'
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to parking space
    parking_space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    
    def __repr__(self):
        return f'<ParkingImage {self.image_url}>'

class Booking(db.Model):
    """Model for parking space bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, confirmed, cancelled, completed
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    
    # Relationship with feedback
    feedback = db.relationship('Feedback', backref='booking', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Booking {self.id}>'

class Feedback(db.Model):
    """Model for feedback on bookings"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to booking
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    
    def __repr__(self):
        return f'<Feedback {self.id}>'