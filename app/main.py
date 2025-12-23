from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from .database import init_db, get_connection, get_all_bookings, insert_booking, delete_booking


app = Flask(__name__)

# Creating the database within the application
init_db()

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

    if not data or not all(k in data for k in ("start", "end", "student_name", "student_timezone")):
        return jsonify({"error": "Missing booking information"}), 400
    
    requested_slot = {
        "start": data["start"],
        "end": data["end"]
    }

    for slot in current_bookings:
        if overlaps(slot, requested_slot):
            return jsonify({
                "error": "Requested slot overlaps with existing availability"
            }), 409
        
    insert_booking(
        requested_slot["start"], 
        requested_slot["end"],
        data["student_name"],
        data["student_timezone"]
        )

    return jsonify({
        "message": "Lesson successfully booked",
        "slot": requested_slot
    }), 200

# Route for cancelling a booking that exists in the database
@app.route('/cancel', methods=['POST'])
def cancel():
    data = request.get_json()

    if not data or "start" not in data or "end" not in data:
        return jsonify({
            "error": "No valid start or end time slot"
            }), 400
    
    success = delete_booking(data["start"], data["end"])

    if not success:
        return jsonify({
            "error": "Booking not found"
        }), 404
    
    return jsonify({
        "message": "Booking successfully cancelled"
    }), 200


# Main
if __name__ == "__main__":
    app.run(debug="True")
