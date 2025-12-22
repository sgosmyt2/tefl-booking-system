from flask import Flask, jsonify, request, send_file
from datetime import datetime, timedelta, timezone
import os

app = Flask(__name__)

#Hardcoded availability calendar for testing
available_slots = [
    {
        "start": "2025-12-23T14:00:00Z",
        "end": "2025-12-23T15:00:00Z"
    },
    {
        "start": "2025-12-23T15:30:00Z",
        "end": "2025-12-23T16:30:00Z"
    },
]

def parse_iso(dt_str):
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

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

# Ignore all this its just something silly and messing around with html and css in Flask
@app.route('/beautifulgirlfriend')
def gf():
    return """
    <h1>Mi novia thalia es muy hermosa <3</h1>
    
    <div style="display: flex; gap: 20px;">
        <div>
            <h2>su cara perfecta</h2>
            <img src="/image/micorazón.jpg" alt="mi corazón" style="max-width: 400px;">
        </div>
        <div>
            <h2>su cara despues viendo este</h2>
            <img src="/image/lacarademiamor.jpg" alt="another image" style="max-width: 400px;">
        </div>
    </div>
    """

@app.route('/image/<filename>')
def get_image(filename):
    image_path = os.path.join(os.path.dirname(__file__), f'images/{filename}')
    return send_file(image_path, mimetype='image/jpeg')


# Creates the availability page to show available timeslots
@app.route('/availability', methods=['GET'])
def availability():
    return jsonify(available_slots)

# Booking page to select 
@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()

    if not data or "start" not in data or "end" not in data:
        return jsonify({"error": "Missing start or end time"}), 400
    
    requested_slot = {
        "start": data["start"],
        "end": data["end"]
    }

    for slot in available_slots:
        if overlaps(slot, requested_slot):
            return jsonify({
                "error": "Requested slot overlaps with existing availability"
            }), 409
        
    available_slots.append(requested_slot)

    return jsonify({
        "message": "Lesson successfully booked",
        "slot": requested_slot
    }), 200

# Main
if __name__ == "__main__":
    app.run(debug="True")
