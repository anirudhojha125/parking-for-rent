from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, TimeField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ParkingSpaceForm(FlaskForm):
    """Form for adding/editing parking spaces"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    address = StringField('Address', validators=[DataRequired(), Length(max=300)])
    latitude = FloatField('Latitude', validators=[Optional(), NumberRange(-90, 90)], default=0.0)
    longitude = FloatField('Longitude', validators=[Optional(), NumberRange(-180, 180)], default=0.0)
    price_per_hour = FloatField('Price per Hour ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    availability_start = TimeField('Available From', validators=[DataRequired()])
    availability_end = TimeField('Available Until', validators=[DataRequired()])
    is_active = BooleanField('Active Listing', default=True)
    submit = SubmitField('Save Parking Space')

class BookingForm(FlaskForm):
    """Form for booking a parking space"""
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Request Booking')