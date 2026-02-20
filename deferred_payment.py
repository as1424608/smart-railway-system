# deferred_payment.py

from datetime import datetime, timedelta
from database import connect_db

def mark_as_deferred(fine_id, days_allowed=2):

    due_date = (datetime.now() + timedelta(days=days_allowed)).strftime("%Y-%m-%d %H:%M:%S")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE fines
        SET status = ?, due_date = ?
        WHERE id = ?
    """, ("PENDING", due_date, fine_id))

    conn.commit()
    conn.close()

    print("\n🕒 Deferred Payment Activated (Elder Friendly)")
    print(f"Fine ID   : {fine_id}")
    print(f"Due Date  : {due_date}")
