from flask import Flask, render_template
from flask_login import LoginManager
from models.database import db
from models.models import User
import pymysql

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    # Configure for XAMPP MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/smart_park_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    from parking import parking
    app.register_blueprint(parking, url_prefix='/parking')
    
    from admin import admin
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Routes
    @app.route('/')
    def home():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)