
class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time, truck_number):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time
        self.truck_number = truck_number
        self.delivered_count = 0
        self.initial_package_count = len(packages)

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.mileage,
                                               self.address, self.depart_time, self.truck_number, self.delivered_count)