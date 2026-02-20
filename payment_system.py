# payment_system.py

import uuid
from datetime import datetime
from database import connect_db

def process_payment(fine_id):

    transaction_id = str(uuid.uuid4())
    payment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE fines
        SET status = ?, transaction_id = ?, payment_time = ?
        WHERE id = ?
    """, ("PAID", transaction_id, payment_time, fine_id))

    conn.commit()
    conn.close()

    print("\n💳 Digital Payment Successful!")
    print(f"Transaction ID : {transaction_id}")
    print(f"Payment Time   : {payment_time}")

    return transaction_id


def generate_receipt(fine_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fines WHERE id = ?", (fine_id,))
    fine = cursor.fetchone()

    conn.close()

    print("\n🧾 OFFICIAL DIGITAL RECEIPT")
    print("---------------------------")
    print(f"Passenger ID : {fine[1]}")
    print(f"From         : {fine[2]}")
    print(f"To           : {fine[3]}")
    print(f"Amount Paid  : ₹{fine[4]}")
    print(f"Status       : {fine[5]}")
    print(f"Transaction  : {fine[6]}")
    print("---------------------------")
