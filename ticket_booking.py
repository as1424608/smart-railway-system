# ticket_booking.py
import qrcode
import uuid
import os
from database import connect_db
from crowd_prediction import predict_crowd 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os 

available_trains = ["Train42", "Train50", "Train60"]

def save_booking(passenger_id, train_id, date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (passenger_id, train_id, date)
        VALUES (?, ?, ?)
    """, (passenger_id, train_id, date))

    conn.commit()
    conn.close()


def confirm_booking(passenger_id, date):

    print("\n📊 Train Crowd Status:")

    for i, train in enumerate(available_trains, start=1):
        level = predict_crowd(train)

        if level == "LOW":
            print(f"{i}. {train} → LOW crowd (Seats likely available)")
        else:
            chance = confirmation_probability(train)
            print(f"{i}. {train} → {level} crowd | Confirmation Chance: {chance}")

    choice = int(input("\nEnter the number of train you want to book: "))

    selected_train = available_trains[choice - 1]

    save_booking(passenger_id, selected_train, date)

    print("\n✅ Booking Confirmed & Saved!")
    print(f"Passenger : {passenger_id}")
    print(f"Train     : {selected_train}")
    print(f"Date      : {date}")
    print(f"Crowd     : {predict_crowd(selected_train)}")

    return selected_train
 # 👈 only if generate_qr_ticket is in same file, REMOVE this line

def web_confirm_booking(passenger_id, train_id, date):

    # 1. Generate QR ticket
    ticket_id, qr_path = generate_qr_ticket(passenger_id, train_id, date)

    # 2. Save ticket in database
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
             INSERT INTO tickets (ticket_id, passenger_id, train_id, date, status, qr_code)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (ticket_id, passenger_id, train_id, date, "VALID", qr_path))


    conn.commit()
    conn.close()

    # 3. Return data to web layer
    return {
    "ticket_id": ticket_id,
    "passenger": passenger_id,
    "train": train_id,
    "date": date,
    "qr": qr_path
}


def generate_qr_ticket(passenger_id, train_id, date):
    """
    Generates ticket ID and QR code image
    """

    ticket_id = str(uuid.uuid4())

    qr_data = f"TICKET_ID:{ticket_id}|PASSENGER:{passenger_id}|TRAIN:{train_id}|DATE:{date}"

    qr = qrcode.make(qr_data)

    qr_folder = "static/qr"
    os.makedirs(qr_folder, exist_ok=True)

    qr_path = f"{qr_folder}/{ticket_id}.png"
    qr.save(qr_path)

    return ticket_id, qr_path



def generate_ticket_pdf(ticket_id, passenger_id, train_id, date, qr_path):

    folder = "tickets"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = f"{folder}/{ticket_id}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "Smart Railway Ticket")

    # Ticket info
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Ticket ID : {ticket_id}")
    c.drawString(100, 670, f"Passenger : {passenger_id}")
    c.drawString(100, 640, f"Train     : {train_id}")
    c.drawString(100, 610, f"Date      : {date}")

    # QR IMAGE
    if qr_path and os.path.exists(qr_path):
        c.drawImage(qr_path, 400, 600, width=120, height=120)

    c.drawString(100, 560, "Please show this QR at entry gate.")

    c.save()

    return file_path

 

