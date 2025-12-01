from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.models import User, ParkingSpace, Booking, db

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def admin_required():
    """Ensure only admins can access admin routes"""
    if not current_user.is_admin:
        abort(403)

@admin.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_users = User.query.count()
    total_spaces = ParkingSpace.query.count()
    total_bookings = Booking.query.count()
    verified_users = User.query.filter_by(is_verified=True).count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_spaces=total_spaces,
                         total_bookings=total_bookings,
                         verified_users=verified_users)

@admin.route('/users')
def list_users():
    """List all users"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/user/<int:user_id>/verify', methods=['POST'])
def verify_user(user_id):
    """Verify a user"""
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    flash(f'User {user.username} has been verified.', 'success')
    return redirect(url_for('admin.list_users'))

@admin.route('/user/<int:user_id>/unverify', methods=['POST'])
def unverify_user(user_id):
    """Unverify a user"""
    user = User.query.get_or_404(user_id)
    user.is_verified = False
    db.session.commit()
    flash(f'User {user.username} has been unverified.', 'success')
    return redirect(url_for('admin.list_users'))

@admin.route('/user/<int:user_id>/make-admin', methods=['POST'])
def make_admin(user_id):
    """Make a user an admin"""
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'User {user.username} is now an admin.', 'success')
    return redirect(url_for('admin.list_users'))

@admin.route('/user/<int:user_id>/remove-admin', methods=['POST'])
def remove_admin(user_id):
    """Remove admin privileges from a user"""
    user = User.query.get_or_404(user_id)
    # Prevent removing admin from current user
    if user.id == current_user.id:
        flash('You cannot remove admin privileges from yourself.', 'error')
        return redirect(url_for('admin.list_users'))
    user.is_admin = False
    db.session.commit()
    flash(f'User {user.username} is no longer an admin.', 'success')
    return redirect(url_for('admin.list_users'))

@admin.route('/spaces')
def list_spaces():
    """List all parking spaces"""
    spaces = ParkingSpace.query.all()
    return render_template('admin/spaces.html', spaces=spaces)

@admin.route('/space/<int:space_id>/deactivate', methods=['POST'])
def deactivate_space(space_id):
    """Deactivate a parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    space.is_active = False
    db.session.commit()
    flash(f'Parking space "{space.title}" has been deactivated.', 'success')
    return redirect(url_for('admin.list_spaces'))

@admin.route('/space/<int:space_id>/activate', methods=['POST'])
def activate_space(space_id):
    """Activate a parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    space.is_active = True
    db.session.commit()
    flash(f'Parking space "{space.title}" has been activated.', 'success')
    return redirect(url_for('admin.list_spaces'))