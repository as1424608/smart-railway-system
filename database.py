# database.py

import sqlite3

DB_NAME = "railway_system.db"

def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # Station entry table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS station_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id TEXT,
        station_id TEXT,
        entry_time TEXT
    )
    """)

    # Booking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id TEXT,
        train_id TEXT,
        date TEXT
    )
    """)

    # Fines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id TEXT,
        boarding_station TEXT,
        destination TEXT,
        fine_amount REAL,
        status TEXT,
        transaction_id TEXT,
        payment_time TEXT,
        due_date TEXT
    )
    """)

    conn.commit()
    conn.close()
def create_ticket_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            passenger_id TEXT,
            train_id TEXT,
            date TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


    #-------gate logs------
def create_tickets_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            passenger_id TEXT,
            train_id TEXT,
            date TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
def create_gate_logs_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS gate_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            passenger_id TEXT,
            train_id TEXT,
            scan_time TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()
def add_qr_column():
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("ALTER TABLE tickets ADD COLUMN qr_code TEXT")
        print("✅ qr_code column added")
    except Exception as e:
        print("ℹ️ Column may already exist:", e)

    conn.commit()
    conn.close()


# Run once to setup DB
if __name__ == "__main__":
    create_tables()
    print("✅ Database & Tables Created Successfully")
if __name__ == "__main__":
    create_tickets_table()
if __name__ == "__main__":
    create_gate_logs_table()
if __name__ == "__main__":
    add_qr_column()\
    
