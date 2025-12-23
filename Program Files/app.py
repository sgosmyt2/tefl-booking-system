from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from database import init_db, get_connection


app = Flask(__name__)

# Creating the database within the application
init_db()

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT start, end FROM bookings")
    rows = cursor.fetchall()

    conn.close()

    return [{"start": row[0], "end": row[1]} for row in rows]

def insert_booking(start, end):
    conn = get_connection()
    cursor = conn.cursor()

    conn.execute("INSERT INTO bookings (start, end) VALUES (?, ?)", (start, end))

    conn.commit()
    conn.close()


def parse_iso(dt_str):
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

# Overlapping booking slot logic, if the start time of slot A is before the end time of slot B, 
# and the end time of A is greater than the start time of B then it must have a time overlap
def overlaps(slot_a, slot_b):
    start_a = parse_iso(slot_a["start"])
    end_a =  parse_iso(slot_a["end"])
    start_b = parse_iso(slot_b["start"])
    end_b = parse_iso(slot_b["end"])
    return start_a < end_b and start_b < end_a

# Creating the home page of website
@app.route('/')
def home():
    return "Booking System Initialised."

# Creates the availability page to show available timeslots
@app.route('/availability', methods=['GET'])
def availability():
    bookings = get_all_bookings()
    return jsonify(bookings)

# Booking page to select 
@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    current_bookings = get_all_bookings()

    if not data or "start" not in data or "end" not in data:
        return jsonify({"error": "Missing start or end time"}), 400
    
    requested_slot = {
        "start": data["start"],
        "end": data["end"]
    }

    for slot in current_bookings:
        if overlaps(slot, requested_slot):
            return jsonify({
                "error": "Requested slot overlaps with existing availability"
            }), 409
        
    insert_booking(requested_slot["start"], requested_slot["end"])

    return jsonify({
        "message": "Lesson successfully booked",
        "slot": requested_slot
    }), 200

# Main
if __name__ == "__main__":
    app.run(debug="True")
