from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from forms.auth import RegistrationForm, LoginForm
from models.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Check if any users exist
    user_count = User.query.count()
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already registered', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        
        # First user becomes main admin
        if user_count == 0:
            user.is_verified = True  # Main admin is auto verified
            user.is_admin = True
            user.is_main_admin = True
            flash('Registration completed successfully! You are now the main administrator.', 'success')
        else:
            # Other users need admin verification
            user.is_verified = False
            user.is_admin = False
            user.is_main_admin = False
            flash('Registration successful! Your account is pending administrator verification.', 'info')
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        if user_count == 0:
            # First user can log in immediately
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            # Other users need to wait for verification
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            # Check if user is verified (except for main admin)
            if user.is_main_admin or user.is_verified:
                login_user(user)
                flash('Logged in successfully!', 'success')
                
                # Redirect to next page or home
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Your account is pending administrator verification.', 'warning')
                return render_template('auth/login.html', form=form)
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@auth.route('/profile')
@login_required
def profile():
    """Display user profile"""
    return render_template('auth/profile.html')