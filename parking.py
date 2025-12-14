from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify, current_app
from flask_login import login_required, current_user
from forms.parking import ParkingSpaceForm, BookingForm
from forms.feedback import FeedbackForm
from models.models import ParkingSpace, Booking, Feedback, ParkingImage, db
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

parking = Blueprint('parking', __name__)

@parking.route('/spaces')
def list_spaces():
    """List all available parking spaces with search and filtering"""
    # Get search and filter parameters
    search_query = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Base query for active parking spaces
    query = ParkingSpace.query.filter_by(is_active=True)
    
    # Apply search filter
    if search_query:
        query = query.filter(
            db.or_(
                ParkingSpace.title.contains(search_query),
                ParkingSpace.description.contains(search_query),
                ParkingSpace.address.contains(search_query)
            )
        )
    
    # Apply price filters
    if min_price is not None:
        query = query.filter(ParkingSpace.price_per_hour >= min_price)
    if max_price is not None:
        query = query.filter(ParkingSpace.price_per_hour <= max_price)
    
    # Execute query
    spaces = query.all()
    
    return render_template('parking/list.html', 
                         spaces=spaces, 
                         search_query=search_query,
                         min_price=min_price,
                         max_price=max_price)

@parking.route('/space/<int:space_id>')
def view_space(space_id):
    """View details of a specific parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    if not space.is_active and space.owner_id != current_user.id:
        abort(404)
    return render_template('parking/detail.html', space=space)

@parking.route('/space/<int:space_id>/book', methods=['GET', 'POST'])
@login_required
def book_space(space_id):
    """Book a parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    
    # Check if the user is trying to book their own space
    if space.owner_id == current_user.id:
        flash('You cannot book your own parking space.', 'error')
        return redirect(url_for('parking.view_space', space_id=space_id))
    
    form = BookingForm()
    if form.validate_on_submit():
        # Combine date with start and end times
        start_datetime = datetime.combine(form.date.data, form.start_time.data)
        end_datetime = datetime.combine(form.date.data, form.end_time.data)
        
        # Validate that end time is after start time
        if end_datetime <= start_datetime:
            flash('End time must be after start time.', 'error')
            return render_template('parking/book_space.html', form=form, space=space)
        
        # Calculate duration in hours
        duration = (end_datetime - start_datetime).total_seconds() / 3600
        
        # Calculate total price
        total_price = duration * space.price_per_hour
        
        # Create booking
        booking = Booking(
            start_time=start_datetime,
            end_time=end_datetime,
            total_price=total_price,
            status='pending',
            customer_id=current_user.id,
            owner_id=space.owner_id,
            parking_space_id=space.id
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking request sent successfully! Please wait for the owner to confirm.', 'success')
        return redirect(url_for('parking.my_bookings'))
    
    return render_template('parking/book_space.html', form=form, space=space)

@parking.route('/my-spaces')
@login_required
def my_spaces():
    """List parking spaces owned by current user"""
    spaces = ParkingSpace.query.filter_by(owner_id=current_user.id).all()
    return render_template('parking/my_spaces.html', spaces=spaces)

@parking.route('/add-space', methods=['GET', 'POST'])
@login_required
def add_space():
    """Add a new parking space"""
    form = ParkingSpaceForm()
    if form.validate_on_submit():
        space = ParkingSpace(
            title=form.title.data,
            description=form.description.data,
            address=form.address.data,
            latitude=form.latitude.data or None,
            longitude=form.longitude.data or None,
            price_per_hour=form.price_per_hour.data,
            availability_start=form.availability_start.data,
            availability_end=form.availability_end.data,
            is_active=form.is_active.data,
            owner_id=current_user.id
        )
        
        db.session.add(space)
        db.session.flush()  # Get the space ID before committing
        
        # Handle image uploads
        if form.images.data:
            uploaded_files = request.files.getlist("images")
            primary_set = False
            
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to filename to avoid conflicts
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    filename = timestamp + filename
                    
                    # Save file to upload folder
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Create relative URL for the image
                    image_url = url_for('static', filename=f'uploads/{filename}')
                    
                    # Create ParkingImage record
                    parking_image = ParkingImage(
                        image_url=image_url,
                        is_primary=not primary_set,  # First image is primary
                        parking_space_id=space.id
                    )
                    
                    db.session.add(parking_image)
                    primary_set = True  # Only first image is primary
        
        db.session.commit()
        
        flash('Parking space added successfully!', 'success')
        return redirect(url_for('parking.my_spaces'))
    
    return render_template('parking/add_space.html', form=form)

@parking.route('/edit-space/<int:space_id>', methods=['GET', 'POST'])
@login_required
def edit_space(space_id):
    """Edit an existing parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    
    # Check if current user owns this space
    if space.owner_id != current_user.id:
        abort(403)
    
    form = ParkingSpaceForm(obj=space)
    if form.validate_on_submit():
        space.title = form.title.data
        space.description = form.description.data
        space.address = form.address.data
        space.latitude = form.latitude.data or None
        space.longitude = form.longitude.data or None
        space.price_per_hour = form.price_per_hour.data
        space.availability_start = form.availability_start.data
        space.availability_end = form.availability_end.data
        space.is_active = form.is_active.data
        
        # Handle image uploads
        if form.images.data:
            uploaded_files = request.files.getlist("images")
            
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to filename to avoid conflicts
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    filename = timestamp + filename
                    
                    # Save file to upload folder
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Create relative URL for the image
                    image_url = url_for('static', filename=f'uploads/{filename}')
                    
                    # Check if this should be the primary image
                    is_primary = False
                    if not space.images:  # If no images exist yet, make this primary
                        is_primary = True
                    elif not any(img.is_primary for img in space.images):
                        is_primary = True  # If no primary image exists, make this one primary
                    
                    # Create ParkingImage record
                    parking_image = ParkingImage(
                        image_url=image_url,
                        is_primary=is_primary,
                        parking_space_id=space.id
                    )
                    
                    db.session.add(parking_image)
        
        db.session.commit()
        
        flash('Parking space updated successfully!', 'success')
        return redirect(url_for('parking.my_spaces'))
    
    return render_template('parking/edit_space.html', form=form, space=space)

@parking.route('/delete-space/<int:space_id>', methods=['POST'])
@login_required
def delete_space(space_id):
    """Delete a parking space"""
    space = ParkingSpace.query.get_or_404(space_id)
    
    # Check if current user owns this space
    if space.owner_id != current_user.id:
        abort(403)
    
    db.session.delete(space)
    db.session.commit()
    
    flash('Parking space deleted successfully!', 'success')
    return redirect(url_for('parking.my_spaces'))

@parking.route('/my-bookings')
@login_required
def my_bookings():
    """List bookings made by current user"""
    # Get bookings made by current user
    bookings = current_user.bookings_made
    # Get bookings received by current user (as owner)
    received_bookings = current_user.bookings_received
    return render_template('parking/my_bookings.html', 
                         bookings=bookings, 
                         received_bookings=received_bookings)

@parking.route('/booking/<int:booking_id>/confirm', methods=['POST'])
@login_required
def confirm_booking(booking_id):
    """Confirm a booking request"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if current user owns the parking space
    if booking.owner_id != current_user.id:
        abort(403)
    
    # Update booking status
    booking.status = 'confirmed'
    db.session.commit()
    
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('parking.my_bookings'))

@parking.route('/booking/<int:booking_id>/reject', methods=['POST'])
@login_required
def reject_booking(booking_id):
    """Reject a booking request"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if current user owns the parking space
    if booking.owner_id != current_user.id:
        abort(403)
    
    # Update booking status
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking rejected.', 'info')
    return redirect(url_for('parking.my_bookings'))

@parking.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking request"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if current user made the booking
    if booking.customer_id != current_user.id:
        abort(403)
    
    # Update booking status
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled.', 'info')
    return redirect(url_for('parking.my_bookings'))

@parking.route('/booking/<int:booking_id>/complete', methods=['POST'])
@login_required
def complete_booking(booking_id):
    """Mark a booking as completed"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if current user is involved in the booking
    if booking.customer_id != current_user.id and booking.owner_id != current_user.id:
        abort(403)
    
    # Update booking status
    booking.status = 'completed'
    db.session.commit()
    
    flash('Booking marked as completed.', 'success')
    return redirect(url_for('parking.my_bookings'))

@parking.route('/booking/<int:booking_id>/feedback', methods=['GET', 'POST'])
@login_required
def submit_feedback(booking_id):
    """Submit feedback for a completed booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if current user is the customer
    if booking.customer_id != current_user.id:
        abort(403)
    
    # Check if booking is completed
    if booking.status != 'completed':
        flash('You can only submit feedback for completed bookings.', 'error')
        return redirect(url_for('parking.my_bookings'))
    
    # Check if feedback already exists
    if booking.feedback:
        flash('Feedback already submitted for this booking.', 'error')
        return redirect(url_for('parking.my_bookings'))
    
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            rating=form.rating.data,
            comment=form.comment.data,
            booking_id=booking.id
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('parking.my_bookings'))
    
    return render_template('parking/submit_feedback.html', form=form, booking=booking)

@parking.route('/map')
def map_view():
    """Display the map with parking spaces and user location"""
    # Get all active parking spaces with coordinates
    spaces = ParkingSpace.query.filter(
        ParkingSpace.is_active == True,
        ParkingSpace.latitude.isnot(None),
        ParkingSpace.longitude.isnot(None)
    ).all()
    
    return render_template('parking/map.html', spaces=spaces)

@parking.route('/api/user-location', methods=['POST'])
@login_required
def update_user_location():
    """Update the current user's location"""
    data = request.get_json()
    
    if 'latitude' not in data or 'longitude' not in data:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    # In a real implementation, you would save this to the database
    # For now, we'll just return success
    return jsonify({'message': 'Location updated successfully'})

@parking.route('/api/parking-spaces')
def api_parking_spaces():
    """API endpoint to get all parking spaces with coordinates"""
    spaces = ParkingSpace.query.filter(
        ParkingSpace.is_active == True,
        ParkingSpace.latitude.isnot(None),
        ParkingSpace.longitude.isnot(None)
    ).all()
    
    # Convert to JSON serializable format
    spaces_data = []
    for space in spaces:
        # Get owner rating
        owner_rating = space.owner.get_average_rating()
        owner_total_ratings = space.owner.get_total_ratings()
        
        spaces_data.append({
            'id': space.id,
            'title': space.title,
            'address': space.address,
            'latitude': float(space.latitude) if space.latitude else None,
            'longitude': float(space.longitude) if space.longitude else None,
            'price_per_hour': float(space.price_per_hour),
            'owner_username': space.owner.username,
            'owner_rating': float(owner_rating) if owner_rating else None,
            'owner_total_ratings': owner_total_ratings
        })
    
    return jsonify(spaces_data)
