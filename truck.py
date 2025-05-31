class Truck:
    def __init__(self, speed, mileage, location, package_ids, departure_time):
        """
        Initializes a new Truck instance.

        Args:
            speed (float): Speed in miles per hour (e.g., 18 mph).
            mileage (float): Initial mileage (typically 0.0).
            location (str): Current address of the truck (starts at the hub).
            package_ids (list): List of package IDs assigned to this truck.
            departure_time (datetime): Time the truck leaves the hub.
        """
        self.speed = speed  # Speed in mph
        self.mileage = mileage  # Total miles driven
        self.location = location  # Current address
        self.package_ids = package_ids  # Packages onboard
        self.departure_time = departure_time  # Departure datetime
        self.delivery_log = []  # Optional: track delivery events

    def __str__(self):
        """
        Returns a string representation of the truck's current state.
        """
        return (f"Truck at {self.location} | Speed: {self.speed} mph | "
                f"Mileage: {self.mileage:.2f} | Packages: {self.package_ids}")

    def add_miles(self, miles):
        """
        Adds miles to the truck's total mileage.

        Args:
            miles (float): Distance traveled in miles.
        """
        self.mileage += miles

    def set_location(self, new_location):
        """
        Updates the truck's current location.

        Args:
            new_location (str): The address to update the truck's location to.
        """
        self.location = new_location
