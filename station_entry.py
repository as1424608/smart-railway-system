# station_entry.py

from database import connect_db

def register_station_entry(passenger_id, station_id, entry_time):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO station_entries (passenger_id, station_id, entry_time)
        VALUES (?, ?, ?)
    """, (passenger_id, station_id, entry_time))

    conn.commit()
    conn.close()

    print(f"Passenger {passenger_id} entered station {station_id} at {entry_time}")

    return {
        "passenger_id": passenger_id,
        "station_id": station_id,
        "entry_time": entry_time
    }
