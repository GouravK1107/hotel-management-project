# 🏨 Hotel Management System

A **full-featured Hotel Management System** built using **Python Flask and SQLite** that helps manage hotel operations such as rooms, guests, bookings, billing, and automated email notifications.

This project was developed as a **BCA 6th Semester Major Project** and also structured to be suitable for **freelancing deployment for small and medium hotels**.

---

# 👨‍💻 Developer

**Gaurav Kumar**
BCA – 6th Semester

**Project Type:**

* Major Academic Project
* Freelance-ready Hotel Management System

**Technologies Used:**
Python Flask, SQLite, Bootstrap 5, JavaScript

---

# ✨ Features

## 📊 Dashboard

* Overview of total rooms
* Available rooms statistics
* Total guests count
* Active bookings overview
* Recent booking activity
* Quick access to all modules

---

## 🏨 Room Management

* Add new rooms
* Edit room details
* Delete rooms
* Set room type and pricing
* Track room availability
* Real-time availability updates

---

## 👤 Guest Management

* Create and manage guest profiles
* Store contact details
* ID proof verification (Aadhar, PAN, Passport, etc.)
* Maintain guest visit history

---

## ⚡ Quick Booking System

* One-step guest + booking creation
* Automatic night calculation
* Automatic price calculation
* Instant booking confirmation
* Email notification to guest

---

## 📅 Booking Management

* Create bookings
* Cancel bookings
* Check-in / Check-out system
* Booking status tracking:

  * Confirmed
  * Checked-in
  * Checked-out
  * Cancelled
* Payment status tracking

---

## 💳 Billing & Invoices

* Automatic invoice generation
* Payment tracking
* Print-ready invoice format
* Email invoice to guests

---

## 📧 Email Notifications

* Booking confirmation emails
* Check-in notifications
* Check-out invoice emails
* Booking cancellation alerts

---

## 📱 Responsive Design

* Mobile friendly interface
* Responsive Bootstrap layout
* Swipeable tables on mobile
* Touch optimized UI
* Smooth animations

---

# 🛠 Technologies Used

## Backend

* Python 3.9+
* Flask 2.3.3
* Flask-SQLAlchemy
* Flask-WTF
* Flask-Mail
* WTForms
* email_validator
* python-dotenv

---

## Frontend

* HTML5
* CSS3
* Bootstrap 5.3
* Font Awesome
* JavaScript (ES6)
* Google Fonts

---

## Database

* SQLite3

---

# 💻 System Requirements

Make sure the following tools are installed:

* Python **3.8+**
* pip (Python Package Manager)
* Modern Browser (Chrome / Firefox / Edge / Safari)
* Gmail account (for sending email notifications)

---

# ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/hotel-management-system.git
cd hotel-management-system
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv env
```

Activate virtual environment:

**Windows**

```bash
env\Scripts\activate
```

**Mac/Linux**

```bash
source env/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

---

### 5️⃣ Initialize Database

```bash
python init_db.py
```

---

### 6️⃣ Run the Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 🗄 Database Schema

The system includes the following main database tables:

### Rooms

* id
* room_number
* room_type
* price
* description
* status

### Guests

* id
* name
* email
* phone
* id_proof_type
* id_proof_number
* address

### Bookings

* id
* guest_id
* room_id
* check_in_date
* check_out_date
* total_amount
* amount_paid
* booking_status
* payment_status

---

# 📁 Project Structure

```
hotel-management-system
│
├── env/
├── instance/
├── static/
│   ├── css
│   ├── js
│   └── images
│
├── templates/
│   ├── dashboard.html
│   ├── rooms.html
│   ├── guests.html
│   ├── bookings.html
│   └── invoice.html
│
├── app.py
├── models.py
├── forms.py
├── init_db.py
├── requirements.txt
└── README.md
```

---

# 📖 Usage Guide

1. Add rooms to the system.
2. Register guests.
3. Create a booking.
4. Perform check-in.
5. Process payments.
6. Generate invoices.
7. Complete check-out.

The system will automatically update room availability and booking status.

---

# 🚀 Future Enhancements

Possible improvements for future versions:

* Online booking portal
* Payment gateway integration
* Multi-hotel management
* Staff management module
* Advanced analytics dashboard
* SMS notifications
* Role-based authentication (Admin / Staff)

---

# 📜 License

This project is developed for **educational and freelance purposes**.
You are free to modify and extend it for learning or commercial use.

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* Fork the project
* Contribute improvements

---

**Developed by Gaurav Kumar**
