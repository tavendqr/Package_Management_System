import csv
import datetime
import Truck
from HashMap import HashMap
from Package import Package

with open("CSV/UPS_Distance_File.csv") as file:
    distanceCsv = csv.reader(file)
    distanceCsv = list(distanceCsv)

with open("CSV/UPS_Address.csv") as file2:
    addressCsv = csv.reader(file2)
    addressCsv = list(addressCsv)

with open("CSV/UPS_Package_File.csv") as file3:
    packageCsv = csv.reader(file3)
    packageCsv = list(packageCsv)

def package_loader(file, packageHash):
    with open(file) as info:
        data = csv.reader(info)
        for package in data:
            pid = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            status = "At Hub"

            p = Package(pid, address, city, state, zipcode, deadline, weight, status)

            packageHash.insert(pid, p)

def distance_location(x, y):
    distance = distanceCsv[x][y]
    if distance == '':
        distance = distanceCsv[y][x]

    return float(distance)


def get_address(address):
    for row in addressCsv:
        if address in row[2]:
            return int(row[0])



packageHash = HashMap()

package_loader("CSV/UPS_Package_File.csv", packageHash)

def package_delivery(truck, stop_time):
    # truck hasn't left yet
    if truck.depart_time > stop_time:
        return

    undelivered = [packageHash.get(pid) for pid in truck.packages.copy()]

    while len(undelivered) > 0:

        nextDistance = float("inf")
        nextPackage = None

        for package in undelivered:
            distance = distance_location(
                get_address(truck.address),
                get_address(package.address)
            )

            if distance < nextDistance:
                nextDistance = distance
                nextPackage = package

        travel_time = datetime.timedelta(hours=nextDistance / 18)

        # full delivery possible
        if truck.time + travel_time <= stop_time:

            undelivered.remove(nextPackage)

            truck.mileage += nextDistance
            truck.address = nextPackage.address
            truck.time += travel_time

            nextPackage.delivery = truck.time
            nextPackage.departure = truck.depart_time
            nextPackage.truck_number = truck.truck_number

            truck.delivered_count += 1
        # stop mid-route
        else:

            remaining_time = stop_time - truck.time
            fraction = remaining_time / travel_time

            truck.mileage += nextDistance * fraction
            truck.time = stop_time

            break


def reset_trucks():
    global truck1, truck2, truck3

    truck1 = Truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                         datetime.timedelta(hours=8), 1)
    truck1.delivered_count = 0
    truck1.mileage = 0


    truck2 = Truck.Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                         "4001 South 700 East", datetime.timedelta(hours=10, minutes=20), 2)
    truck2.delivered_count = 0
    truck2.mileage = 0
    truck3 = Truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                         datetime.timedelta(hours=9, minutes=5), 3)
    truck3.delivered_count = 0
    truck3.mileage = 0

def run_deliveries(slider_value):
    stop_time = get_user_time(slider_value)
    reset_trucks()


    package_delivery(truck1, stop_time)
    package_delivery(truck2, stop_time)

    truck3.depart_time = min(truck1.time, truck2.time)
    truck3.time = truck3.depart_time

    package_delivery(truck3, stop_time)

    packages_delivered = truck1.delivered_count + truck2.delivered_count + truck3.delivered_count
    total_packages = truck1.initial_package_count + truck2.initial_package_count + truck3.initial_package_count

    if total_packages == 0:
        delivery_rate = 0
    else:
        delivery_rate = round(packages_delivered / total_packages, 2) * 100

    addOne = truck1.address
    addTwo = truck2.address
    addThree = truck3.address

    boardOne = get_current_package_status(truck1, stop_time)
    boardTwo = get_current_package_status(truck2, stop_time)
    boardThree = get_current_package_status(truck3, stop_time)

    mileOne, mileTwo, mileThree = truck1.mileage, truck2.mileage, truck3.mileage


    return (truck1.mileage + truck2.mileage + truck3.mileage, packages_delivered, delivery_rate, addOne, addTwo,
            addThree, boardOne, boardTwo, boardThree, mileOne, mileTwo, mileThree)

def get_packages(slider_value):
    stop_time = get_user_time(slider_value)
    for package in packageHash.to_dict().values():
        package.update_status(stop_time)
    return  packageHash.to_dict()


def get_user_time(slider_value):
    base_time = datetime.timedelta(hours=0)
    return base_time + datetime.timedelta(hours=slider_value)


def get_current_package_status(truck, stop_time):
    for pid in truck.packages:
        pkg = packageHash.get(pid)
        pkg.update_status(stop_time)

        if pkg.status != "Delivered":
            return pkg.status

    return packageHash.get(truck.packages[-1]).status

