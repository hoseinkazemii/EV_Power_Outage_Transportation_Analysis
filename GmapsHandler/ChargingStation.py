class ChargingStation:
    def __init__(self, name, location, plug_types_available):
        self.name = name
        self.location = location  # Tuple of (latitude, longitude)
        self.plug_types_available = plug_types_available  # List of plug types available at this station
        self.queue = []  # Queue to hold cars waiting to charge

    def has_plug_type(self, plug_type):
        # Check if the station has the specified plug type available
        return plug_type in self.plug_types_available

    def distance_to(self, location):
        # Calculate distance between the station and a location (like a car's location)
        # Implement distance calculation based on latitude and longitude
        pass

    def add_to_queue(self, car):
        # Add a car to the station's charging queue
        self.queue.append(car)

    def serve_next_car(self):
        # Serve the next car in the queue (simulate charging)
        if self.queue:
            car = self.queue.pop(0)
            # Determine suitable plug type for the car
            suitable_plug = None
            for plug_type in car.plug_types_supported:
                if self.has_plug_type(plug_type):
                    suitable_plug = plug_type
                    break
            if suitable_plug:
                car.charge(suitable_plug)
