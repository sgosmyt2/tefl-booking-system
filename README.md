# TEFL Booking System

This project is a personal learning portfolio project exploring backend dev with Flask through designing a lesson booking system for TEFL (Teaching English as a Foreign Language) lessons. The aim of this system is to manage availability and lesson bookings so that it is robust regardless of time zones and scheduling conflicts, reflecting the real world constraints when teaching students across regions.

## Methods

- Language: Python
- Framework: Flask
- Data Storage: SQLite
- Environment: Conda, VSCode
- Other tools: pytest

## Current Functionality

- View available slots through a REST API
- Prevent double booking and overlapping time slots
- Persistent storage using SQLite
- Booking cancellation support
- Unit tests for core scheduling logic

## Project Structure

- `app/` — application code
  - `main.py` — Flask routes and business logic
  - `database.py` — database access and SQL queries
- `tests/` — unit tests
- `bookings.db` — SQLite database (generated at runtime)

## Running Program

conda activate bookingapp
python -m app.main

### Running Tests

pytest

## Planned extensions

- Time zone handling 
- Cancellation of bookings
- Comparative scheduling views
- Authentication
- Frontend interface