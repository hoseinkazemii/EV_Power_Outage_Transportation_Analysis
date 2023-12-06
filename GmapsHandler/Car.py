class Car:
    def __init__(self, make, model, plug_types_supported, current_location):
        self.make = make
        self.model = model
        self.plug_types_supported = plug_types_supported  # List of plug types supported by the car
        self.current_location = current_location  # Tuple of (latitude, longitude)
        self.needs_charging = True  # Flag to determine if the car needs charging

    def charge(self, plug_type):
        # Simulating charging process for a specific plug type
        if plug_type in self.plug_types_supported:
            if plug_type == 'J1772' or plug_type == 'TESLA':
                # Charging time for J1772 and TESLA plugs is 7 hours
                charging_time = 7 * 60  # Charging time in minutes
                # Simulate charging progress over time
                for minute in range(charging_time):
                    # Update charging status or progress
                    # For example:
                    charging_progress = (minute + 1) / charging_time * 100  # Charging progress percentage
                    print(f"Charging {plug_type}: {charging_progress:.2f}% complete")
                    # You might also update an attribute to track charging status
                    # Example: self.charging_progress = charging_progress
            elif plug_type == 'CHADEMO':
                # Charging time for CHADEMO plug is 40 minutes
                charging_time = 40  # Charging time in minutes
                # Simulate charging progress over time
                for minute in range(charging_time):
                    # Update charging status or progress
                    # For example:
                    charging_progress = (minute + 1) / charging_time * 100  # Charging progress percentage
                    print(f"Charging {plug_type}: {charging_progress:.2f}% complete")
                    # You might also update an attribute to track charging status
                    # Example: self.charging_progress = charging_progress
            self.needs_charging = False

    def find_next_nearest_station(self, charging_stations):
        # Find the next nearest charging station that can serve this car
        # Sort charging stations by distance and check if they support any of the car's plug types
        sorted_stations = sorted(charging_stations, key=lambda station: station.distance_to(self.current_location))
        for station in sorted_stations:
            for plug_type in self.plug_types_supported:
                if station.has_plug_type(plug_type):
                    return station
        return None  # No suitable station found

    def set_location(self, new_location):
        # Update car's current location
        self.current_location = new_location