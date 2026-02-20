# fine_management.py

from database import connect_db

station_distances = {
    "STA001": 0,
    "STA002": 20,
    "STA003": 45,
    "STA004": 70,
    "STA005": 100
}

FARE_PER_KM = 0.5
PENALTY = 200


def calculate_distance(start_station, end_station):
    return abs(station_distances[start_station] - station_distances[end_station])


def calculate_fine(boarding_station, destination):
    distance = calculate_distance(boarding_station, destination)
    fare = distance * FARE_PER_KM
    return round(fare + PENALTY, 2)


def generate_fine(passenger_id, boarding_station, destination):

    fine_amount = calculate_fine(boarding_station, destination)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fines (
            passenger_id, boarding_station, destination,
            fine_amount, status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (passenger_id, boarding_station, destination, fine_amount, "UNPAID"))

    conn.commit()

    fine_id = cursor.lastrowid
    conn.close()

    print("\n🚨 Fine Generated (Fair System)")
    print(f"Passenger ID : {passenger_id}")
    print(f"From         : {boarding_station}")
    print(f"To           : {destination}")
    print(f"Fine Amount  : ₹{fine_amount}")

    return fine_id, fine_amount
