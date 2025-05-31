class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, status="At hub"):
        """
        Initializes a new Package instance.

        Args:
            package_id (int): Unique identifier for the package.
            address (str): Delivery address.
            city (str): City for delivery.
            zip_code (str): ZIP code for delivery.
            deadline (str): Delivery deadline as a string (e.g., "10:30 AM" or "EOD").
            weight (float): Package weight in kilograms.
            status (str): Initial status of the package ("At hub" by default).
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None  # Time the package was delivered (set during routing)

    def __str__(self):
        """
        Returns a user-friendly string representation of the package,
        showing delivery time as HH:MM or 'None' if not delivered.
        """
        delivery_time_str = self.delivery_time.strftime("%H:%M") if self.delivery_time else "None"
        return (f"Package {self.package_id}: {self.address}, {self.city} {self.zip_code}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}kg, "
                f"Status: {self.status}, Delivery Time: {delivery_time_str}")

    def update_status(self, current_time):
        """
        Updates the status of the package based on the provided current time.

        Args:
            current_time (datetime): The time to compare with the delivery time.
        """
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.delivery_time and current_time < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "At hub"
