# graph_dashboard.py

import sqlite3
import matplotlib.pyplot as plt

DB_NAME = "railway_system.db"

def show_fine_graph():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_time, fine_amount 
        FROM fines 
        WHERE status='PAID'
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No paid fines available to plot.")
        return

    times = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8,5))
    plt.plot(times, amounts)
    plt.xticks(rotation=45)
    plt.xlabel("Payment Time")
    plt.ylabel("Fine Amount")
    plt.title("Fines Collected Over Time")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    show_fine_graph()
