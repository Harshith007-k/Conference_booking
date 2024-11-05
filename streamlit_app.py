import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, time, timedelta

st.image("https://phoenixteam.com/wp-content/uploads/2024/02/Phoenix-Logo.png",width=15,use_column_width="always")

st.title("Conference Booking :calendar:")
# Database connection function
def create_connection():
    conn = sqlite3.connect("MY_DB.db")  # Connects to MY_DB.db file
    return conn

# Initialize the database and create the bookings table if it doesn't exist
def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    # SQL command to create the table with name, date, start time, end time, and booking_type columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            booking_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

st.image("https://bdk-wp-media.s3.amazonaws.com/wp-content/uploads/2020/01/13165647/About-icon.gif",use_column_width="always")

# Save a booking to the database
def save_booking(name, date, start_time, end_time, booking_type):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, date, start_time, end_time, booking_type) VALUES (?, ?, ?, ?, ?)
    ''', (name, date, start_time, end_time, booking_type))
    conn.commit()
    conn.close()

# Load bookings for a specific date
def load_bookings(date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, start_time, end_time, booking_type FROM bookings WHERE date = ?
    ''', (date,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

# Load all bookings and return as DataFrame
def load_all_bookings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, date, start_time, end_time, booking_type FROM bookings ORDER BY date, start_time
    ''')
    bookings = cursor.fetchall()
    conn.close()
    # Convert to DataFrame
    df = pd.DataFrame(bookings, columns=["Name", "Date", "Start Time", "End Time", "Booking Type"])
    return df

# Check for overlapping bookings
def is_time_slot_available(date, new_start, new_end):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT start_time, end_time FROM bookings WHERE date = ?
    ''', (date,))
    bookings = cursor.fetchall()
    conn.close()
    
    new_start = datetime.strptime(new_start, "%H:%M")
    new_end = datetime.strptime(new_end, "%H:%M")

    for start, end in bookings:
        booked_start = datetime.strptime(start, "%H:%M")
        booked_end = datetime.strptime(end, "%H:%M")
        # Check for overlap
        if (new_start < booked_end) and (new_end > booked_start):
            return False
    return True

# Initialize database
initialize_db()

# Define default time range
default_start_time = time(9, 0)
default_end_time = time(17, 0)

# Select a date for the booking
selected_date = st.date_input("Select a date")
date_str = selected_date.strftime("%Y-%m-%d")

# Display current bookings for the selected date in a table
st.subheader("Current Bookings")
booked_slots = load_bookings(date_str)
if booked_slots:
    df = pd.DataFrame(booked_slots, columns=["Name", "Start Time", "End Time", "Booking Type"])
    st.dataframe(df)
else:
    st.write("No bookings for this date")

# Time range selection (from and to)
st.image("https://fylfotservices.com/wp-content/uploads/2023/07/Untitled-design.jpg")
st.subheader("Book a Time Slot")
name = st.text_input("Enter your Name and Department")
booking_type = st.selectbox("Select Conference room", ["Big Conference room", "Discussion room1", "Discussion room2"])
start_time = st.time_input("Select start time", default_start_time)
end_time = st.time_input("Select end time", (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time())

# Ensure end time is after start time
if end_time <= start_time:
    st.error("End time must be after start time")
elif not name:
    st.error("Please enter your name")
else:
    # Book slot and check for availability
    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")
    
    if st.button("Book Slot"):
        # Check if the selected time slot is available
        if is_time_slot_available(date_str, start_time_str, end_time_str):
            save_booking(name, date_str, start_time_str, end_time_str, booking_type)
            st.success(f"Booked {start_time_str} - {end_time_str} for {name} as a {booking_type} on {selected_date.strftime('%Y-%m-%d')}")
        else:
            st.error(f"Time slot {start_time_str} - {end_time_str} on {selected_date.strftime('%Y-%m-%d')} is already booked.")

# Display all bookings in a DataFrame for a complete view
st.subheader("All Bookings")
all_bookings_df = load_all_bookings()
st.dataframe(all_bookings_df)
