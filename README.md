# 🚆 Smart Railway Management System

A Full-Stack Railway Management System developed using **Python, Flask, SQLite, HTML, CSS, JavaScript, QR Code Technology, and Data Analytics**.

The system provides smart ticket booking, QR-based ticket verification, PDF ticket generation, gate access control, fraud detection, fine management, and an admin analytics dashboard.

---

## 🌟 Key Features

### 🎫 Smart Ticket Booking
- Passenger ticket booking interface
- Train selection system
- Travel date management
- Automatic ticket generation

### 📱 QR Code Based Tickets
- Unique QR code generated for every ticket
- Secure passenger verification
- QR stored with ticket information

### 📄 PDF Ticket Generation
- Downloadable railway tickets
- Passenger and journey information
- Embedded QR code
- Professional ticket format

### 🚪 Smart Entry Gate System
- Ticket verification at entry gate
- Automatic access approval/rejection
- Used-ticket detection
- Invalid-ticket detection

### 📷 Live QR Scanner
- Browser-based QR scanner
- Real-time ticket validation
- Railway gate simulation

### 🚨 Fraud Detection System
- Detects multiple scans of same ticket
- Suspicious activity alerts
- Fraud prevention mechanism

### 💳 Fine Management
- Digital fine generation
- Fine payment tracking
- Deferred payment support
- Fine status management

### 📊 Admin Dashboard
- Total bookings overview
- Fine statistics
- Paid/Pending fine monitoring
- Gate activity management

### 📈 Analytics & Visualization
- Booking statistics
- Fine collection trends
- Fine status graphs
- Administrative insights

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Database
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Libraries Used
- qrcode
- Pillow
- ReportLab
- Matplotlib

---

## 📂 Project Structure

  smart-railway-system/
│
├── web_app.py
├── database.py
├── ticket_booking.py
├── station_entry.py
├── validation.py
├── fine_management.py
├── deferred_payment.py
├── payment_system.py
├── crowd_prediction.py
├── enforcement.py
├── dashboard.py
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── dashboard.html
│ ├── ticket.html
│ ├── gate.html
│ ├── gate_logs.html
│ └── scan_qr.html
│
├── static/
│ ├── style.css
│ └── qr/
│
├── railway_system.db
├── requirements.txt
└── README.md


---

## ⚙️ Installation Guide

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-railway-system.git
cd smart-railway-system


*** Create Virtual Environment
python -m venv venv
*** Activate Virtual Environment
Windows:
venv\Scripts\activate
Linux/Mac:
source venv/bin/activate
*** Install Dependencies
pip install -r requirements.txt


*** Run Application

Initialize Database:

python database.py

Start Flask Server:

python web_app.py

Open Browser:

http://127.0.0.1:5000

🔄 System Workflow

Passenger
↓
Book Ticket
↓
Generate QR Code
↓
Generate PDF Ticket
↓
Entry Gate Verification
↓
QR Scan Validation
↓
Access Granted / Denied
↓
Fraud Detection & Logging
↓
Admin Dashboard Analytics


// screenshots of the project frontend
<img width="1567" height="985" alt="Screenshot 2026-06-01 232030" src="https://github.com/user-attachments/assets/9313d579-697f-4f54-b05b-21920c4c8d50" />


<img width="1902" height="1039" alt="Screenshot 2026-06-01 232007" src="https://github.com/user-attachments/assets/ff617afe-ddb8-469f-983e-e9da1908a44d" />

<img width="719" height="995" alt="Screenshot 2026-06-01 232132" src="https://github.com/user-attachments/assets/43c16db0-8611-450b-be16-d695166333d0" />
