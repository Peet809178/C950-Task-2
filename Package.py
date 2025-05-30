class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, status="At hub"):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None  # Will be set when delivered

    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, {self.city} {self.zip_code}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}kg, "
                f"Status: {self.status}, Delivery Time: {self.delivery_time}")

    def update_status(self, current_time):
        """Optional method for CLI time-based lookup"""
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.delivery_time and current_time < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "At hub"
