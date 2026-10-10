# 🏨 Hotel Management System

A full-featured Hotel Management System built with **Python Flask and SQLite** that handles rooms, guests, bookings, billing and automated email notifications end-to-end. Built as a BCA 6th-semester major project — and structured to be genuinely freelance-deployable for small and medium hotels.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

---

> 🤝 **Project Type: Freelance**
>
> This project was built as part of a freelance engagement for a client. It is shared here with the client's permission to showcase my work, and sensitive details such as credentials, business data, and proprietary information have been removed. If you'd like a similar solution for your business, feel free to get in touch!

## ✨ Features

### 📊 Dashboard
- Overview of total rooms and availability stats
- Total guests count
- Active bookings overview
- Recent booking activity
- Quick access to all modules

### 🏨 Room Management
- Add, edit and delete rooms
- Set room type and pricing
- Real-time room availability tracking

### 👤 Guest Management
- Create and manage guest profiles
- Store contact details
- ID proof verification (Aadhar, PAN, Passport, etc.)
- Guest visit history

### ⚡ Quick Booking System
- One-step guest + booking creation
- Automatic night & price calculation
- Instant booking confirmation with email notification

### 📅 Booking Management
- Create / cancel bookings
- Check-in / check-out flow
- Status tracking: Confirmed → Checked-in → Checked-out → Cancelled
- Payment status tracking

### 💳 Billing & Invoices
- Automatic invoice generation
- Payment tracking
- Print-ready invoice format
- Invoice emailed directly to guests

### 📧 Email Notifications
- Booking confirmation emails
- Check-in notifications
- Check-out invoice emails
- Cancellation alerts

### 📱 Responsive Design
- Mobile-friendly, fully responsive Bootstrap layout
- Swipeable tables and touch-optimized UI on mobile
- Smooth UI animations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+, Flask 2.3.3, Flask-SQLAlchemy, Flask-WTF, Flask-Mail, WTForms, python-dotenv |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, Font Awesome, JavaScript (ES6), Google Fonts |
| **Database** | SQLite3 |

---

## 💻 System Requirements

- Python **3.8+**
- pip (Python package manager)
- A modern browser (Chrome / Firefox / Edge / Safari)
- A Gmail account (for sending email notifications)

---

## 📂 Project Structure

```
hotel-management-project/
│
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
├── app.py            # Flask application entry point
├── models.py          # SQLAlchemy models (Room, Guest, Booking)
├── forms.py            # WTForms form definitions
├── init_db.py            # Database initialization script
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation Guide

**1️⃣ Clone the repository**
```
git clone https://github.com/GouravK1107/hotel-management-project.git
cd hotel-management-project
```

**2️⃣ Create a virtual environment**
```
python -m venv env
```
Activate it:
```
env\Scripts\activate       # Windows
source env/bin/activate    # Mac / Linux
```

**3️⃣ Install dependencies**
```
pip install -r requirements.txt
```

**4️⃣ Set up environment variables**

Create a `.env` file:
```
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

**5️⃣ Initialize the database**
```
python init_db.py
```

**6️⃣ Run the application**
```
python app.py
```

Open
```
http://127.0.0.1:5000
```

---

## 🗄️ Database Schema

**Rooms**
`id · room_number · room_type · price · description · status`

**Guests**
`id · name · email · phone · id_proof_type · id_proof_number · address`

**Bookings**
`id · guest_id · room_id · check_in_date · check_out_date · total_amount · amount_paid · booking_status · payment_status`

---

## 📖 Usage Guide

1. Add rooms to the system
2. Register guests
3. Create a booking
4. Perform check-in
5. Process payments
6. Generate invoices
7. Complete check-out

Room availability and booking status update automatically at every step.

---

## 🚀 Future Enhancements

- 🌐 Online booking portal
- 💳 Payment gateway integration
- 🏢 Multi-hotel management
- 👥 Staff management module with role-based auth (Admin / Staff)
- 📊 Advanced analytics dashboard
- 📱 SMS notifications

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.
Fork → create a branch → commit → push → open a pull request.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 👨‍💻 Author

**Gourav R**
Backend Developer | Applied AI Developer

GitHub: https://github.com/GouravK1107
Portfolio: https://gouravk1107.github.io/my-portfolio/

---

Made with ❤️ and a lot of check-ins.
