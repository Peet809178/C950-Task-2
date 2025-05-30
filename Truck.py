class Truck:
    def __init__(self, speed, mileage, location, package_ids, departure_time):
        self.speed = speed  # in miles per hour (e.g., 18 mph)
        self.mileage = mileage  # total miles driven
        self.location = location  # current address (string)
        self.package_ids = package_ids  # list of package IDs on the truck
        self.departure_time = departure_time  # datetime object
        self.delivery_log = []  # optional: to track delivery history

    def __str__(self):
        return (f"Truck at {self.location} | Speed: {self.speed} mph | "
                f"Mileage: {self.mileage:.2f} | Packages: {self.package_ids}")

    def add_miles(self, miles):
        self.mileage += miles

    def set_location(self, new_location):
        self.location = new_location
