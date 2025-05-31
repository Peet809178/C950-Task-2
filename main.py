# main.py — Student ID: 012431169

import csv
from datetime import datetime, timedelta

# Import custom modules for data structures and models
from package import Package
from hash_table import HashTable
from truck import Truck

# ─── 1. LOAD DATA ───

# Load all package data from CSV and store in a hash table
def load_packages(csv_path):
    table = HashTable()
    with open(csv_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            pkg_id = int(row[0])
            address = row[1]
            city = row[2]
            zip_code = row[4]
            deadline = row[5]
            weight = float(row[6].split()[0])  # Extracts numeric weight
            pkg = Package(pkg_id, address, city, zip_code, deadline, weight)
            table.insert(pkg_id, pkg)
    return table

# Load distance matrix from CSV into a 2D list
def load_distances(csv_path):
    matrix = []
    with open(csv_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(cell) if cell else 0.0 for cell in row])  # Replace empty cells with 0.0
    return matrix

# Load addresses from CSV (assumes address is in column index 2)
def load_addresses(csv_path):
    addresses = []
    with open(csv_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            addresses.append(row[2].strip())
    return addresses

# ─── 2. ROUTING LOGIC ───

# Returns index of an address in the master address list
def get_address_index(address, address_list):
    for i in range(len(address_list)):
        if address.strip().lower() == address_list[i].strip().lower():
            return i
    print(f"⚠️ Address not found: {address}")
    return None

# Looks up the distance between two addresses by index
def get_distance(from_index, to_index, distance_matrix):
    distance = distance_matrix[from_index][to_index]
    if distance == 0.0:
        distance = distance_matrix[to_index][from_index]  # Use reverse if forward value is missing
    return distance

# Simulates the delivery process for one truck using a greedy approach
def deliver_packages(truck, pkg_table, dist_matrix, address_list):
    current_time = truck.departure_time  # Start at departure time
    visited = []  # Keep track of visited destination indices

    while truck.package_ids:  # While there are packages left to deliver
        current_location_index = get_address_index(truck.location, address_list)
        next_package = None
        min_distance = float('inf')  # Initialize minimum distance as infinite

        # Find the closest package to deliver next
        for pkg_id in truck.package_ids:
            pkg = pkg_table.lookup(pkg_id)

            destination_index = get_address_index(pkg.address, address_list)
            if destination_index is None or current_location_index is None:
                continue

            distance = get_distance(current_location_index, destination_index, dist_matrix)
            if distance < min_distance and destination_index not in visited:
                min_distance = distance
                next_package = pkg

        # Deliver the chosen package
        if next_package:
            destination_index = get_address_index(next_package.address, address_list)
            travel_time = timedelta(minutes=(min_distance / truck.speed) * 60)  # Convert distance to time
            current_time += travel_time

            truck.add_miles(min_distance)
            truck.set_location(next_package.address)

            next_package.delivery_time = current_time
            next_package.status = "Delivered"

            visited.append(destination_index)
            truck.package_ids.remove(next_package.package_id)

# ─── 3. MAIN ───

def main():
    # Load all necessary data from CSV files
    pkg_table = load_packages('CSV/packages.csv')
    dist_matrix = load_distances('CSV/distances.csv')
    address_list = load_addresses('CSV/addresses.csv')

    # Initialize trucks with packages and departure times
    hub = "4001 South 700 East"
    depart = datetime.strptime("08:00", "%H:%M")
    truck1 = Truck(18, 0.0, hub, [1, 3, 6, 13, 15], depart)
    truck2 = Truck(18, 0.0, hub, [2, 4, 7, 8, 14], depart)
    truck3_depart = datetime.strptime("10:20", "%H:%M")  # Delayed departure for package constraints
    truck3 = Truck(18, 0.0, hub, [5, 9, 10, 11, 12], truck3_depart)

    # Begin delivery simulation
    for truck in (truck1, truck2, truck3):
        deliver_packages(truck, pkg_table, dist_matrix, address_list)

    # Print total mileage after all deliveries
    total_miles = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"Total mileage for all trucks: {total_miles:.2f} miles")

    # CLI instructions for time-based package status lookup
    print("\nTo check package status at a specific time, follow this format:")
    print("Enter a time (HH:MM) — 24-hour format")
    print("Examples:")
    print("  08:45 for 8:45 AM")
    print("  09:35 for 9:35 AM")
    print("  12:03 for 12:03 PM")
    print("  13:12 for 1:12 PM")

    # Prompt user for a time to view package statuses
    user_time = input("\nEnter a time (HH:MM) to view statuses: ")
    t = datetime.strptime(user_time, "%H:%M")

    # Allow user to look up a single package or all
    choice = input("Lookup [1] single package or [2] all packages? ")
    if choice == '1':
        pkg_id = int(input("Enter package ID: "))
        pkg = pkg_table.lookup(pkg_id)
        if pkg:
            pkg.update_status(t)
            print(pkg)
        else:
            print("Package not found.")
    else:
        # Print status of all packages in the hash table
        for bucket in pkg_table.table:
            for (_, pkg) in bucket:
                pkg.update_status(t)
                print(pkg)

# Entry point for the program
if __name__ == "__main__":
    main()
