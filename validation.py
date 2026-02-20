from datetime import datetime, timedelta

def is_within_booking_window(entry_time, current_time, window_minutes=15):
    entry = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
    current = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    return current <= entry + timedelta(minutes=window_minutes)

# Example usage:
# Assume entry time is when the user entered the station.
entry_time = "2026-01-21 14:30:00"
current_time = "2026-01-21 14:40:00"
print(is_within_booking_window(entry_time, current_time))  # True if within 15 minutes
