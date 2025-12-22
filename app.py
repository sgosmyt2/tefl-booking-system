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

# Creating the home page of website
@app.route('/')
def home():
    return "Booking System Initialised."
    #"""return
    #<h1>Mi novia thalia es muy hermosa <3</h1>
    #<img src="/image" alt="mi corazón" style="max-width: 500px;">
    #"""

#@app.route('/image')
#def get_image():
#    image_path = os.path.join(os.path.dirname(__file__), 'images/micorazón.jpg')
#    return send_file(image_path, mimetype='image/jpeg')


# Creates the availability page to show available timeslots
@app.route('/availability', methods=['GET'])
def availability():
    return jsonify(available_slots)

# Booking page to select 
@app.route('/book', methods=['POST'])
def book():
    data = request.json

    if not data or "start" not in data or "end" not in data:
        return jsonify({"error": "Missing start or end time"}), 400
    
    requested_slot = {
        "start": data["start"],
        "end": data["end"]
    }

    if requested_slot not in available_slots:
        return jsonify({"error": "requested time slot is not available"}), 409
    
    available_slots.remove(requested_slot)

    return jsonify({
        "message": "Lesson successfully booked",
        "slot": requested_slot
    }), 200


if __name__ == "__main__":
    app.run(debug="True")
