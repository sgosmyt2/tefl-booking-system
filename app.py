from flask import Flask, jsonify
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

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

@app.route('/')
def home():
    return "Booking system initalised."

@app.route('/availability')
def availability():
    return jsonify(available_slots)

if __name__ == "__main__":
    app.run(debug="True")
