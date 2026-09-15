# airport_manager.py

airport_info = ("OUL", "1", "14-09-2026")

allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}

restricted_destinations = {"Moscow", "Pyongyang"}

flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": [
            "Alice Wong",
            "David Kim",
            "Fatima Ali",
        ],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": [
            "Chen Wei",
            "George Smith",
        ],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": [
            "Hana Lee",
            "Maria Garcia",
            "Noah Wilson",
        ],
    },
}


def find_flight(flights, flight_number):
    """Return the stored flight key matching flight_number, or None."""
    if not isinstance(flight_number, str):
        return None

    target = flight_number.strip().lower()

    for key in flights:
        if key.strip().lower() == target:
            return key

    return None


def passenger_exists(passengers, name):
    """Return True if name exists in passengers, case-insensitively."""
    if not isinstance(name, str):
        return False

    target = name.strip().lower()

    for passenger in passengers:
        if isinstance(passenger, str) and passenger.strip().lower() == target:
            return True

    return False


def check_in_passenger(flights, flight_number, name, restricted_destinations):
    """Check in a passenger and return the appropriate status string."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if not isinstance(name, str):
        return "EMPTY_NAME"

    clean_name = " ".join(name.split()).title()

    if clean_name == "":
        return "EMPTY_NAME"

    flight = flights[flight_key]

    if passenger_exists(flight["passengers"], clean_name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    destination = flight["destination"]
    for restricted in restricted_destinations:
        if (
            isinstance(restricted, str)
            and destination.strip().lower() == restricted.strip().lower()
        ):
            return "RESTRICTED"

    flight["passengers"].append(clean_name)
    return "OK"


def remove_passenger(flights, flight_number, name):
    """Remove a passenger from a flight, case-insensitively."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if not isinstance(name, str):
        return "PASSENGER_NOT_FOUND"

    target = name.strip().lower()
    passengers = flights[flight_key]["passengers"]

    for index, passenger in enumerate(passengers):
        if isinstance(passenger, str) and passenger.strip().lower() == target:
            passengers.pop(index)
            return "OK"

    return "PASSENGER_NOT_FOUND"


def change_gate(flights, flight_number, new_gate, allowed_gates):
    """Change a flight's gate if the flight exists and the gate is allowed."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if not isinstance(new_gate, str):
        return "INVALID_GATE"

    normalized_gate = new_gate.strip().upper()
    normalized_allowed = {
        gate.strip().upper()
        for gate in allowed_gates
        if isinstance(gate, str)
    }

    if normalized_gate not in normalized_allowed:
        return "INVALID_GATE"

    flights[flight_key]["gate"] = normalized_gate
    return "OK"


def flight_status(flight):
    """Return AVAILABLE, ALMOST FULL, or FULL for a flight."""
    capacity = flight["capacity"]
    passenger_count = len(flight["passengers"])

    if capacity <= 0:
        return "FULL" if passenger_count > 0 else "AVAILABLE"

    if passenger_count >= capacity:
        return "FULL"

    if passenger_count / capacity >= 0.75:
        return "ALMOST FULL"

    return "AVAILABLE"


def sorted_manifest(flights, flight_number):
    """Return a sorted copy of the passenger list, or None if not found."""
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


def total_passengers(flights):
    """Return the total number of passengers across all flights."""
    return sum(len(flight["passengers"]) for flight in flights.values())


def any_full_flight(flights):
    """Return True if any flight is full."""
    return any(
        len(flight["passengers"]) >= flight["capacity"]
        for flight in flights.values()
    )


def all_flights_have_passengers(flights):
    """Return True if every flight has at least one passenger."""
    return all(
        len(flight["passengers"]) > 0
        for flight in flights.values()
    )

