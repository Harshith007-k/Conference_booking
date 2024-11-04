import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

st.image("https://phoenixteam.com/wp-content/uploads/2024/02/Phoenix-Logo.png",width=15,use_column_width="always")

st.title("Conference Booking :calendar:")
# Database connection function

#st.title("Time Slot Booking App with In-Memory Storage")

# Initialize an empty list to hold booking data
if 'bookings' not in st.session_state:
    st.session_state['bookings'] = []

# Function to add a booking
def add_booking(name, date, start_time, end_time, booking_type):
    st.session_state['bookings'].append({
        "Name": name,
        "Date": date,
        "Start Time": start_time,
        "End Time": end_time,
        "Booking Type": booking_type
    })
st.image("https://fylfotservices.com/wp-content/uploads/2023/07/Untitled-design.jpg")

# Check for overlapping bookings
def is_time_slot_available(date, new_start, new_end):
    new_start = datetime.strptime(new_start, "%H:%M")
    new_end = datetime.strptime(new_end, "%H:%M")

    for booking in st.session_state['bookings']:
        if booking["Date"] == date:
            booked_start = datetime.strptime(booking["Start Time"], "%H:%M")
            booked_end = datetime.strptime(booking["End Time"], "%H:%M")
            # Check for overlap
            if (new_start < booked_end) and (new_end > booked_start):
                return False
    return True
    

# Define default time range
default_start_time = time(9, 0)
default_end_time = time(17, 0)

# Select a date for the booking
selected_date = st.date_input("Select a date")
date_str = selected_date.strftime("%Y-%m-%d")

# Display current bookings for the selected date in a table
st.subheader("Current Bookings")
current_bookings = [
    booking for booking in st.session_state['bookings'] if booking["Date"] == date_str
]
if current_bookings:
    df = pd.DataFrame(current_bookings)
    st.dataframe(df)
else:
    st.write("No bookings for this date")

st.image("https://bdk-wp-media.s3.amazonaws.com/wp-content/uploads/2020/01/13165647/About-icon.gif",use_column_width="always")
# Time range selection (from and to)
st.subheader("Book a Time Slot")
name = st.text_input("Enter your name")
booking_type = st.selectbox("Select Booking Type", ["Meeting", "Workshop", "Consultation"])
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
            add_booking(name, date_str, start_time_str, end_time_str, booking_type)
            st.success(f"Booked {start_time_str} - {end_time_str} for {name} as a {booking_type} on {selected_date.strftime('%Y-%m-%d')}")
        else:
            st.error(f"Time slot {start_time_str} - {end_time_str} on {selected_date.strftime('%Y-%m-%d')} is already booked.")

# Display all bookings in a DataFrame for a complete view
st.subheader("All Bookings")
all_bookings_df = pd.DataFrame(st.session_state['bookings'])
st.dataframe(all_bookings_df)
