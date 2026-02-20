# dashboard.py

from database import connect_db


def get_dashboard_stats():
    """
    Returns booking and fine statistics for admin dashboard
    """

    conn = connect_db()
    cur = conn.cursor()

    # Total bookings
    cur.execute("SELECT COUNT(*) FROM bookings")
    bookings = cur.fetchone()[0]

    # Total fines
    cur.execute("SELECT COUNT(*) FROM fines")
    fines = cur.fetchone()[0]

    # Paid fines
    cur.execute("SELECT COUNT(*) FROM fines WHERE status='PAID'")
    paid = cur.fetchone()[0]

    # Pending fines
    cur.execute("SELECT COUNT(*) FROM fines WHERE status='PENDING'")
    pending = cur.fetchone()[0]

    conn.close()

    return {
        "bookings": bookings,
        "fines": fines,
        "paid": paid,
        "pending": pending
    }
