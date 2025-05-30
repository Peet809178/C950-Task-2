# main.py — Student ID: YOUR-STUDENT-ID-HERE

import csv
from datetime import datetime, timedelta

from Package import Package
from CreateHashTable import HashTable
from Truck import Truck

# ─── 1. LOAD DATA ───

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
            weight = float(row[6].split()[0])
            pkg = Package(pkg_id, address, city, zip_code, deadline, weight)
            table.insert(pkg_id, pkg)
    return table

def load_distances(csv_path):
    matrix = []
    with open(csv_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(cell) if cell else 0.0 for cell in row])
    return matrix

def load_addresses(csv_path):
    addresses = []
    with open(csv_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            addresses.append(row[2].strip())
    return addresses

# ─── 2. ROUTING LOGIC ───

def get_address_index(address, address_list):
    for i in range(len(address_list)):
        if address.strip().lower() == address_list[i].strip().lower():
            return i
    print(f"⚠️ Address not found: {address}")
    return None

def get_distance(from_index, to_index, distance_matrix):
    distance = distance_matrix[from_index][to_index]
    if distance == 0.0:
        distance = distance_matrix[to_index][from_index]
    return distance

def deliver_packages(truck, pkg_table, dist_matrix, address_list):
    current_time = truck.departure_time
    visited = []

    while truck.package_ids:
        current_location_index = get_address_index(truck.location, address_list)
        next_package = None
        min_distance = float('inf')

        for pkg_id in truck.package_ids:
            pkg = pkg_table.lookup(pkg_id)

            if pkg.package_id == 9 and current_time < datetime.strptime("10:20", "%H:%M"):
                continue

            destination_index = get_address_index(pkg.address, address_list)
            if destination_index is None or current_location_index is None:
                continue

            distance = get_distance(current_location_index, destination_index, dist_matrix)
            if distance < min_distance and destination_index not in visited:
                min_distance = distance
                next_package = pkg

        if next_package:
            destination_index = get_address_index(next_package.address, address_list)
            travel_time = timedelta(minutes=(min_distance / truck.speed) * 60)
            current_time += travel_time

            truck.add_miles(min_distance)
            truck.set_location(next_package.address)

            next_package.delivery_time = current_time
            next_package.status = "Delivered"

            visited.append(destination_index)
            truck.package_ids.remove(next_package.package_id)

# ─── 3. MAIN ───

def main():
    pkg_table = load_packages('CSV/Package_File.csv')
    dist_matrix = load_distances('CSV/Distance_File.csv')
    address_list = load_addresses('CSV/Address_File.csv')

    hub = "4001 South 700 East"
    depart = datetime.strptime("08:00", "%H:%M")

    truck1 = Truck(18, 0.0, hub, [1, 3, 6, 13, 15], depart)
    truck2 = Truck(18, 0.0, hub, [2, 4, 7, 8, 14], depart)
    truck3 = Truck(18, 0.0, hub, [5, 9, 10, 11, 12], depart)

    for truck in (truck1, truck2, truck3):
        deliver_packages(truck, pkg_table, dist_matrix, address_list)

    total_miles = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"Total mileage for all trucks: {total_miles:.2f} miles")

    print("\nTo check package status at a specific time, follow this format:")
    print("Enter a time (HH:MM) — 24-hour format")
    print("Examples:")
    print("  08:45 for 8:45 AM")
    print("  09:35 for 9:35 AM")
    print("  12:03 for 12:03 PM")
    print("  13:12 for 1:12 PM")

    user_time = input("\nEnter a time (HH:MM) to view statuses: ")
    t = datetime.strptime(user_time, "%H:%M")

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
        for bucket in pkg_table.table:
            for (_, pkg) in bucket:
                pkg.update_status(t)
                print(pkg)

if __name__ == "__main__":
    main()