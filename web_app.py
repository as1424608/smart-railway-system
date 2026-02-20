# web_app.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from flask import Flask, render_template, request, redirect, session
from ticket_booking import web_confirm_booking
from database import connect_db
import matplotlib
matplotlib.use('Agg')
import io
import base64
import matplotlib.pyplot as plt
from datetime import datetime
from flask import send_file
from ticket_booking import generate_ticket_pdf




app = Flask(__name__)
app.secret_key = "railway_secret"
# hashed version of "1234"
ADMIN_PASSWORD_HASH = generate_password_hash("1234")
#--------logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- HOME PAGE UI ----------------

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Smart Railway System</title>
<style>

body{
    margin:0;
    font-family: Arial;
    background:#f2f5f9;
}


header{
    background:#0b3c5d;
    color:white;
    padding:15px;
    text-align:center;
    font-size:24px;
}

.container{
    width:420px;
    margin:60px auto;
}

.card{
    background:white;
    padding:25px;
    border-radius:12px;
    margin-bottom:25px;
    box-shadow:0 5px 15px rgba(0,0,0,0.1);
}

h2{
    color:#0b3c5d;
}

input{
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:6px;
    border:1px solid #ccc;
}
select{
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:6px;
    border:1px solid #ccc;
}

button{
    width:100%;
    padding:12px;
    background:#ff8c00;
    color:white;
    border:none;
    border-radius:6px;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    background:#e67e00;
}

.admin-btn{
    background:#0b3c5d;
}

.admin-btn:hover{
    background:#072c45;
}

.footer{
    text-align:center;
    color:gray;
}

</style>
</head>

<body>

<header>🚆 Smart Railway Management System</header>

<div class="container">

<div class="card">
<h2>Book Ticket</h2>
<form method="post" action="/book">
<input name="pid" placeholder="Passenger ID" required>
<input name="date" placeholder="Travel Date (YYYY-MM-DD)" required>
<button>Book Ticket</button>
</form>
</div>

<div class="card">
<h2>Admin Panel</h2>
<form action="/login">
<button class="admin-btn">Admin Login</button>
</form>
</div>

<div class="footer">
Digital Railway Platform
</div>

</div>

</body>
</html>
"""

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- BOOKING ----------------

@app.route("/book", methods=["POST"])
def book():
    pid = request.form["pid"]
    date = request.form["date"]
    train = request.form["train"]

    result = web_confirm_booking(pid, train, date)

    return render_template(
        "ticket.html",
        ticket_id=result["ticket_id"],
        passenger=result["passenger"],
        train=result["train"],
        date=result["date"],
        qr=result["qr"]
    )




# ---------------- LOGIN ----------------

LOGIN_PAGE = """
<h2 style="text-align:center;">Admin Login</h2>
<form method="post" style="width:300px;margin:auto;">
<input name="user" placeholder="Username"><br><br>
<input name="pass" type="password" placeholder="Password"><br><br>
<button>Login</button>
</form>
"""
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["user"]
        password = request.form["pass"]

        if username == "admin" and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin"] = True
            session["last_active"] = datetime.now().timestamp()
            return redirect("/dashboard")

        else:
            return "❌ Wrong credentials"

    from flask import render_template
    return render_template("login.html")



# ---------------- DASHBOARD ----------------

from dashboard import get_dashboard_stats

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/login")

    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        bookings=stats["bookings"],
        fines=stats["fines"],
        paid=stats["paid"],
        pending=stats["pending"]
    )

#-------gate log-------
@app.route("/gate_logs")
def gate_logs():

    if not session.get("admin"):
        return redirect("/login")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT ticket_id, passenger_id, train_id, scan_time, result
        FROM gate_logs
        ORDER BY scan_time DESC
    """)

    logs = cur.fetchall()
    conn.close()

    return render_template("gate_logs.html", logs=logs)


# ---------------- GRAPH ----------------

@app.route("/fine_graph")
def fine_graph():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT payment_time, fine_amount FROM fines WHERE status='PAID'")
    data = cur.fetchall()
    conn.close()

    if not data:
        return "<h3>No paid fine data available</h3>"

    times = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6,4))
    plt.plot(times, amounts)
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Fine Amount")
    plt.title("Fines Collected Over Time")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()

    plt.close()

    return f"""
<h2>📈 Fine Collection Graph</h2>
<img src="data:image/png;base64,{graph_url}">
<br><br>
<a href="/dashboard">Back</a>
"""
@app.route("/booking_graph")
def booking_graph():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT train_id, COUNT(*) 
        FROM bookings 
        GROUP BY train_id
    """)
    data = cur.fetchall()
    conn.close()

    if not data:
        return "<h3>No booking data available</h3>"

    trains = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(6,4))
    plt.bar(trains, counts)
    plt.xlabel("Train")
    plt.ylabel("Bookings")
    plt.title("Bookings Per Train")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"""
    <h2>📊 Bookings Per Train</h2>
    <img src="data:image/png;base64,{graph_url}">
    <br><br>
    <a href="/dashboard">Back</a>
    """
@app.route("/fine_status_graph")
def fine_status_graph():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM fines WHERE status='PAID'")
    paid = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM fines WHERE status='PENDING'")
    pending = cur.fetchone()[0]

    conn.close()

    labels = ["Paid", "Pending"]
    values = [paid, pending]

    plt.figure(figsize=(5,4))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Fine Payment Status")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"""
    <h2>📉 Fine Status</h2>
    <img src="data:image/png;base64,{graph_url}">
    <br><br>
    <a href="/dashboard">Back</a>
    """

# for verification of qr
@app.route("/verify", methods=["GET", "POST"])
def verify_ticket():

    result = None
    color = "black"
    details = None

    if request.method == "POST":
        ticket_id = request.form["ticket_id"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT passenger_id, train_id, date, status
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,))

        row = cur.fetchone()

        if not row:
            result = "❌ INVALID TICKET"
            color = "red"

        else:
            passenger, train, date, status = row

            if status == "VALID":
                result = "✅ VALID TICKET"
                color = "green"

                # mark ticket as USED
                cur.execute(
                    "UPDATE tickets SET status='USED' WHERE ticket_id=?",
                    (ticket_id,)
                )
                conn.commit()

                details = {
                    "passenger": passenger,
                    "train": train,
                    "date": date
                }

            elif status == "USED":
                result = "⚠️ TICKET ALREADY USED"
                color = "orange"

            else:
                result = "❌ INVALID / EXPIRED"
                color = "red"

        conn.close()

    return render_template(
        "verify.html",
        result=result,
        color=color,
        details=details
    )

@app.route("/gate", methods=["GET", "POST"])
def entry_gate():

    status = None
    color = "black"
    details = None

    if request.method == "POST":
        ticket_id = request.form["ticket_id"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT passenger_id, train_id, date, status
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,))

        row = cur.fetchone()
        result_text = "DENIED"
        passenger_id = None
        train_id = None

        if not row:
            status = "❌ ACCESS DENIED – INVALID TICKET"
            color = "red"

        else:
            passenger, train, date, ticket_status = row
            passenger_id = passenger
            train_id = train


            if ticket_status == "VALID":
                result_text = "OPEN"
                status = "✅ GATE OPEN – WELCOME"
                color = "green"

                # mark ticket as USED
                cur.execute(
                    "UPDATE tickets SET status='USED' WHERE ticket_id=?",
                    (ticket_id,)
                )
                conn.commit()

                details = {
                    "passenger": passenger,
                    "train": train,
                    "date": date
                }

            elif ticket_status == "USED":
                result_text = "USED"
                status = "⚠️ ACCESS DENIED – TICKET ALREADY USED"
                color = "orange"

            else:
                status = "❌ ACCESS DENIED"
                color = "red"
            cur.execute("""
            INSERT INTO gate_logs (ticket_id, passenger_id, train_id, scan_time, result)
    VALUES (?, ?, ?, ?, ?)
""", (
    ticket_id,
    passenger_id,
    train_id,
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    result_text
            ))
        conn.commit()

        conn.close()

    return render_template(
        "gate.html",
        status=status,
        color=color,
        details=details
    )
@app.route("/download_ticket/<ticket_id>")
def download_ticket(ticket_id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT passenger_id, train_id, date, qr_code
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return "Ticket not found"

    passenger_id, train_id, date, qr_path = row
    print("QR PATH:", qr_path)

    pdf_path = generate_ticket_pdf(
        ticket_id,
        passenger_id,
        train_id,
        date,
        qr_path
    )
   

    return send_file(pdf_path, as_attachment=True)
@app.route("/scan_qr")
def scan_qr():
    return render_template("scan_qr.html")


import json

@app.route("/verify_scan", methods=["POST"])
def verify_scan():

    data = request.get_json()
    qr_data = data["qr_data"]

    ticket_id = qr_data.split("|")[0].split(":")[1]

    # 🚨 FRAUD CHECK
    if check_fraud(ticket_id):
        return {"message": "🚨 FRAUD ALERT — MULTIPLE SCANS DETECTED"}

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cur.fetchone()

    if not row:
        result = "❌ INVALID TICKET"

    elif row[0] == "VALID":
        result = "✅ VALID TICKET — ALLOW ENTRY"

        # mark as used
        cur.execute("UPDATE tickets SET status='USED' WHERE ticket_id=?", (ticket_id,))
        conn.commit()

    elif row[0] == "USED":
        result = "⚠️ TICKET ALREADY USED"

    else:
        result = "❌ ACCESS DENIED"

    # Save log
    cur.execute("""
        INSERT INTO gate_logs (ticket_id, passenger_id, train_id, scan_time, result)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, None, None,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          result))

    conn.commit()
    conn.close()

    return {"message": result}


from datetime import datetime, timedelta

def check_fraud(ticket_id):

    conn = connect_db()
    cur = conn.cursor()

    # Count scans in last 1 minute
    one_minute_ago = (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        SELECT COUNT(*) FROM gate_logs
        WHERE ticket_id = ? AND scan_time >= ?
    """, (ticket_id, one_minute_ago))

    count = cur.fetchone()[0]
    conn.close()

    if count >= 3:
        return True

    return False

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)