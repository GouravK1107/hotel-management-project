from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired(), Length(max=10)])
    room_type = SelectField('Room Type', choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], validators=[DataRequired()])
    price = FloatField('Price per Night', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Optional()])
    is_available = BooleanField('Available', default=True)

class GuestForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    proof_type = SelectField('ID Proof Type', choices=[
        ('', 'Select ID Proof Type'),
        ('Aadhar Card', 'Aadhar Card'),
        ('PAN Card', 'PAN Card'),
        ('Passport', 'Passport'),
        ('Driver License', 'Driver License'),
        ('Voter ID', 'Voter ID'),
        ('Other', 'Other')
    ], validators=[Optional()])
    id_proof = StringField('ID Proof Number', validators=[Optional(), Length(max=100)])

class QuickBookingForm(FlaskForm):
    # Guest Details
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    proof_type = SelectField('ID Proof Type', choices=[
        ('', 'Select ID Proof Type'),
        ('Aadhar Card', 'Aadhar Card'),
        ('PAN Card', 'PAN Card'),
        ('Passport', 'Passport'),
        ('Driver License', 'Driver License'),
        ('Voter ID', 'Voter ID'),
        ('Other', 'Other')
    ], validators=[Optional()])
    id_proof = StringField('ID Proof Number', validators=[Optional(), Length(max=100)])
    
    # Booking Details
    room_id = SelectField('Select Room', coerce=int, validators=[DataRequired()])
    check_in_date = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    paid_amount = FloatField('Advance Payment', validators=[Optional(), NumberRange(min=0)], default=0)

class BookingForm(FlaskForm):
    guest_id = SelectField('Select Guest', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Select Room', coerce=int, validators=[DataRequired()])
    check_in_date = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('confirmed', 'Confirmed'),
        ('checked-in', 'Checked In'),
        ('checked-out', 'Checked Out'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()], default='confirmed')
    total_amount = FloatField('Total Amount', validators=[Optional(), NumberRange(min=0)], default=0)
    paid_amount = FloatField('Advance Payment', validators=[Optional(), NumberRange(min=0)], default=0)

class CheckInForm(FlaskForm):
    pass

class CheckOutForm(FlaskForm):
    final_payment = FloatField('Final Payment', validators=[DataRequired(), NumberRange(min=0)])