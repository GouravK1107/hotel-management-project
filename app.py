import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, session
from models import db, User, Room, Guest, Booking, Invoice
from forms import *
from functools import wraps
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gouravnav45@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'sfcr oypy bxkf ucwu'  # Your app password
app.config['MAIL_DEFAULT_SENDER'] = 'gouravnav45@gmail.com'  # Replace with your email

mail = Mail(app)
db.init_app(app)

# Create tables and admin user on startup
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
    print("✅ Database tables created/verified")

# Email sending function
def send_email(recipient, subject, body):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.html = body
        mail.send(msg)
        print(f"✅ Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False

# Generate email templates (same as before, update to include proof_type if needed)
def get_booking_confirmation_email(booking):
    guest = booking.guest
    room = booking.room
    proof_display = f"{guest.proof_type}: {guest.id_proof}" if guest.proof_type and guest.id_proof else "Not provided"
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f8f9fa; }}
            .details {{ background-color: white; padding: 15px; border-radius: 5px; }}
            .footer {{ text-align: center; padding: 20px; color: #6c757d; }}
            .badge {{ background-color: #28a745; color: white; padding: 5px 10px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Hotel Management System</h2>
                <h3>Booking Confirmation</h3>
            </div>
            <div class="content">
                <p>Dear {guest.first_name} {guest.last_name},</p>
                <p>Thank you for choosing our hotel. Your booking has been confirmed.</p>
                
                <div class="details">
                    <h4>Booking Details:</h4>
                    <p><strong>Booking ID:</strong> #{booking.id}</p>
                    <p><strong>Room:</strong> {room.room_number} ({room.room_type})</p>
                    <p><strong>Check-in:</strong> {booking.check_in_date.strftime('%d-%m-%Y')}</p>
                    <p><strong>Check-out:</strong> {booking.check_out_date.strftime('%d-%m-%Y')}</p>
                    <p><strong>Nights:</strong> {booking.nights()}</p>
                    <p><strong>Total Amount:</strong> ${booking.total_amount}</p>
                    <p><strong>Paid Amount:</strong> ${booking.paid_amount}</p>
                    <p><strong>Balance:</strong> ${booking.balance()}</p>
                    <p><strong>ID Proof:</strong> {proof_display}</p>
                    <p><strong>Status:</strong> <span class="badge">Confirmed</span></p>
                </div>
                
                <p>We look forward to welcoming you!</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply.</p>
                <p>&copy; {datetime.now().year} Hotel Management System</p>
            </div>
        </div>
    </body>
    </html>
    """

def get_cancellation_email(booking):
    guest = booking.guest
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f8f9fa; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Booking Cancellation</h2>
            </div>
            <div class="content">
                <p>Dear {guest.first_name} {guest.last_name},</p>
                <p>Your booking #{booking.id} has been cancelled as requested.</p>
                <p>If you have any questions, please contact us.</p>
            </div>
        </div>
    </body>
    </html>
    """

def get_checkout_email(booking, invoice):
    guest = booking.guest
    room = booking.room
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f8f9fa; }}
            .invoice {{ background-color: white; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Thank You for Staying With Us!</h2>
            </div>
            <div class="content">
                <p>Dear {guest.first_name} {guest.last_name},</p>
                <p>Thank you for choosing our hotel. We hope you enjoyed your stay.</p>
                
                <div class="invoice">
                    <h4>Final Invoice</h4>
                    <p><strong>Invoice #:</strong> {invoice.id}</p>
                    <p><strong>Booking ID:</strong> #{booking.id}</p>
                    <p><strong>Room:</strong> {room.room_number} ({room.room_type})</p>
                    <p><strong>Check-in:</strong> {booking.check_in_date.strftime('%d-%m-%Y')}</p>
                    <p><strong>Check-out:</strong> {booking.check_out_date.strftime('%d-%m-%Y')}</p>
                    <p><strong>Nights:</strong> {booking.nights()}</p>
                    <p><strong>Total Amount:</strong> ${booking.total_amount}</p>
                    <p><strong>Total Paid:</strong> ${booking.paid_amount}</p>
                    <p><strong>Status:</strong> {'Paid' if invoice.paid else 'Partial Payment'}</p>
                </div>
                
                <p>We look forward to welcoming you again!</p>
            </div>
        </div>
    </body>
    </html>
    """

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor
@app.context_processor
def inject_year():
    return {'current_year': datetime.utcnow().year}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(is_available=True).count()
    total_guests = Guest.query.count()
    active_bookings = Booking.query.filter(Booking.status.in_(['confirmed', 'checked-in'])).count()
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()
    return render_template('dashboard.html', total_rooms=total_rooms, available_rooms=available_rooms,
                           total_guests=total_guests, active_bookings=active_bookings,
                           recent_bookings=recent_bookings)

# Quick Booking - Combined Guest & Booking
# Quick Booking - Combined Guest & Booking
@app.route('/quick-booking', methods=['GET', 'POST'])
@login_required
def quick_booking():
    form = QuickBookingForm()
    # Only show available rooms
    available_rooms = Room.query.filter_by(is_available=True).all()
    form.room_id.choices = [(r.id, f"{r.room_number} ({r.room_type}) - ${r.price}/night") for r in available_rooms]
    
    # Create a dictionary of room prices for JavaScript
    room_prices = {room.id: room.price for room in available_rooms}
    
    if form.validate_on_submit():
        # Check if guest already exists
        guest = Guest.query.filter_by(email=form.email.data).first()
        if not guest:
            # Create new guest with proof type
            guest = Guest(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                address=form.address.data,
                proof_type=form.proof_type.data,
                id_proof=form.id_proof.data
            )
            db.session.add(guest)
            db.session.flush()  # Get guest ID without committing
        
        # Get room and calculate total
        room = Room.query.get(form.room_id.data)
        nights = (form.check_out_date.data - form.check_in_date.data).days
        
        if nights <= 0:
            flash('Check-out date must be after check-in date.', 'danger')
            return render_template('quick_booking.html', form=form, room_prices=room_prices)
        
        total_amount = nights * room.price
        
        # Create booking
        booking = Booking(
            guest_id=guest.id,
            room_id=form.room_id.data,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,
            status='confirmed',
            total_amount=total_amount,
            paid_amount=form.paid_amount.data
        )
        
        db.session.add(booking)
        room.is_available = False
        db.session.commit()
        
        # Send confirmation email
        email_body = get_booking_confirmation_email(booking)
        send_email(guest.email, f"Booking Confirmation - #{booking.id}", email_body)
        
        flash(f'Booking created successfully! Confirmation email sent to {guest.email}', 'success')
        return redirect(url_for('booking_detail', id=booking.id))
    
    return render_template('quick_booking.html', form=form, room_prices=room_prices)
# Room management
@app.route('/rooms')
@login_required
def rooms():
    all_rooms = Room.query.all()
    return render_template('rooms.html', rooms=all_rooms)

@app.route('/rooms/add', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            price=form.price.data,
            description=form.description.data,
            is_available=form.is_available.data
        )
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('rooms'))
    return render_template('add_room.html', form=form)

@app.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room(id):
    room = Room.query.get_or_404(id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.room_number = form.room_number.data
        room.room_type = form.room_type.data
        room.price = form.price.data
        room.description = form.description.data
        room.is_available = form.is_available.data
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('rooms'))
    return render_template('edit_room.html', form=form, room=room)

@app.route('/rooms/delete/<int:id>')
@login_required
def delete_room(id):
    room = Room.query.get_or_404(id)
    if Booking.query.filter_by(room_id=id).first():
        flash('Cannot delete room with existing bookings.', 'danger')
    else:
        db.session.delete(room)
        db.session.commit()
        flash('Room deleted successfully!', 'success')
    return redirect(url_for('rooms'))

# Guest management
@app.route('/guests')
@login_required
def guests():
    all_guests = Guest.query.all()
    return render_template('guests.html', guests=all_guests)

@app.route('/guests/add', methods=['GET', 'POST'])
@login_required
def add_guest():
    form = GuestForm()
    if form.validate_on_submit():
        guest = Guest(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            proof_type=form.proof_type.data,
            id_proof=form.id_proof.data
        )
        db.session.add(guest)
        db.session.commit()
        flash('Guest added successfully!', 'success')
        return redirect(url_for('guests'))
    return render_template('add_guest.html', form=form)

@app.route('/guests/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_guest(id):
    guest = Guest.query.get_or_404(id)
    form = GuestForm(obj=guest)
    if form.validate_on_submit():
        guest.first_name = form.first_name.data
        guest.last_name = form.last_name.data
        guest.email = form.email.data
        guest.phone = form.phone.data
        guest.address = form.address.data
        guest.proof_type = form.proof_type.data
        guest.id_proof = form.id_proof.data
        db.session.commit()
        flash('Guest updated successfully!', 'success')
        return redirect(url_for('guests'))
    return render_template('edit_guest.html', form=form, guest=guest)

@app.route('/guests/delete/<int:id>')
@login_required
def delete_guest(id):
    guest = Guest.query.get_or_404(id)
    if Booking.query.filter_by(guest_id=id).first():
        flash('Cannot delete guest with existing bookings.', 'danger')
    else:
        db.session.delete(guest)
        db.session.commit()
        flash('Guest deleted successfully!', 'success')
    return redirect(url_for('guests'))

# Booking management
@app.route('/bookings')
@login_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template('bookings.html', bookings=all_bookings)

@app.route('/bookings/add', methods=['GET', 'POST'])
@login_required
def add_booking():
    form = BookingForm()
    form.guest_id.choices = [(g.id, f"{g.first_name} {g.last_name}") for g in Guest.query.all()]
    # Only show available rooms for new bookings
    available_rooms = Room.query.filter_by(is_available=True).all()
    form.room_id.choices = [(r.id, f"{r.room_number} ({r.room_type}) - ${r.price}/night") for r in available_rooms]
    
    if form.validate_on_submit():
        room = Room.query.get(form.room_id.data)
        nights = (form.check_out_date.data - form.check_in_date.data).days
        
        if nights <= 0:
            flash('Check-out date must be after check-in date.', 'danger')
            return render_template('add_booking.html', form=form)
        
        total_amount = nights * room.price
        
        booking = Booking(
            guest_id=form.guest_id.data,
            room_id=form.room_id.data,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,
            status='confirmed',  # Always set to confirmed for new bookings
            total_amount=total_amount,
            paid_amount=form.paid_amount.data
        )
        
        db.session.add(booking)
        room.is_available = False
        db.session.commit()
        
        # Send confirmation email
        guest = Guest.query.get(form.guest_id.data)
        email_body = get_booking_confirmation_email(booking)
        send_email(guest.email, f"Booking Confirmation - #{booking.id}", email_body)
        
        flash(f'Booking created successfully! Confirmation email sent to {guest.email}', 'success')
        return redirect(url_for('bookings'))
    
    return render_template('add_booking.html', form=form)

@app.route('/bookings/<int:id>')
@login_required
def booking_detail(id):
    booking = Booking.query.get_or_404(id)
    return render_template('booking_detail.html', booking=booking)

@app.route('/bookings/checkin/<int:id>', methods=['GET', 'POST'])
@login_required
def check_in(id):
    booking = Booking.query.get_or_404(id)
    if booking.status != 'confirmed':
        flash('Booking cannot be checked in (current status: {})'.format(booking.status), 'warning')
        return redirect(url_for('booking_detail', id=id))
    
    form = CheckInForm()
    if form.validate_on_submit():
        booking.status = 'checked-in'
        booking.room.is_available = False
        db.session.commit()
        
        # Send check-in notification
        guest = booking.guest
        email_body = f"""
        <html>
        <body>
            <h2>Check-in Confirmation</h2>
            <p>Dear {guest.first_name},</p>
            <p>You have successfully checked in to Room {booking.room.room_number}.</p>
            <p>Check-in: {booking.check_in_date}<br>
            Check-out: {booking.check_out_date}</p>
            <p>Enjoy your stay!</p>
        </body>
        </html>
        """
        send_email(guest.email, f"Check-in Confirmation - Booking #{booking.id}", email_body)
        
        flash('Guest checked in successfully. Notification email sent.', 'success')
        return redirect(url_for('booking_detail', id=id))
    
    return render_template('check_in.html', form=form, booking=booking)

@app.route('/bookings/checkout/<int:id>', methods=['GET', 'POST'])
@login_required
def check_out(id):
    booking = Booking.query.get_or_404(id)
    if booking.status != 'checked-in':
        flash('Booking is not checked in.', 'warning')
        return redirect(url_for('booking_detail', id=id))
    
    form = CheckOutForm()
    if form.validate_on_submit():
        payment = form.final_payment.data
        booking.paid_amount += payment
        
        if booking.paid_amount >= booking.total_amount:
            booking.paid_amount = booking.total_amount
            booking.status = 'checked-out'
            booking.room.is_available = True
            invoice = Invoice(booking_id=booking.id, amount=booking.total_amount, paid=True)
            db.session.add(invoice)
            db.session.commit()
            
            # Send checkout email with invoice
            email_body = get_checkout_email(booking, invoice)
            send_email(booking.guest.email, f"Thank You & Invoice - Booking #{booking.id}", email_body)
            
            flash('Check-out complete. Invoice generated and sent to guest email.', 'success')
        else:
            booking.status = 'checked-out'
            booking.room.is_available = True
            invoice = Invoice(booking_id=booking.id, amount=booking.total_amount, paid=False)
            db.session.add(invoice)
            db.session.commit()
            
            email_body = get_checkout_email(booking, invoice)
            send_email(booking.guest.email, f"Check-out & Invoice - Booking #{booking.id}", email_body)
            
            flash(f'Check-out complete with partial payment. Invoice sent to guest email.', 'warning')
        
        return redirect(url_for('booking_detail', id=id))
    
    return render_template('check_out.html', form=form, booking=booking)

@app.route('/bookings/cancel/<int:id>')
@login_required
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    if booking.status in ['checked-out', 'cancelled']:
        flash('Booking already {}'.format(booking.status), 'warning')
    else:
        booking.status = 'cancelled'
        booking.room.is_available = True
        db.session.commit()
        
        # Send cancellation email
        email_body = get_cancellation_email(booking)
        send_email(booking.guest.email, f"Booking Cancellation - #{booking.id}", email_body)
        
        flash('Booking cancelled. Cancellation email sent to guest.', 'success')
    
    return redirect(url_for('booking_detail', id=id))

@app.route('/invoice/<int:id>')
@login_required
def view_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    return render_template('invoice.html', invoice=invoice)

if __name__ == '__main__':
    app.run(debug=True)