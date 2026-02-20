from fine_management import generate_fine
from payment_system import process_payment, generate_receipt
from deferred_payment import mark_as_deferred

def verify_passenger(passenger_id, valid_tickets, boarding_station="STA001", destination="STA005", elder=False):

    if passenger_id in valid_tickets:
        print(f"Passenger {passenger_id} has a valid ticket.")
        return True

    else:
        print(f"\n❌ Passenger {passenger_id} has NO valid ticket!")

        fine_id, fine_amount = generate_fine(passenger_id, boarding_station, destination)

        if elder:
            mark_as_deferred(fine_id)
        else:
            process_payment(fine_id)
            generate_receipt(fine_id)

        return False
