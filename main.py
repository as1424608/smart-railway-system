from station_entry import register_station_entry
from validation import is_within_booking_window
from ticket_booking import confirm_booking
from enforcement import verify_passenger

# Example flow
entry_record = register_station_entry('P123', 'STA001', '2026-01-21 14:30:00')
is_valid = is_within_booking_window(entry_record['entry_time'], '2026-01-21 14:35:00')
if is_valid:
    confirm_booking('P123', '2026-01-22')
verify_passenger('P999', {'P123', 'P124'})
verify_passenger('P888', {'P123','P124'}, elder=True)

