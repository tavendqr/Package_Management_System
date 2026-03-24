import datetime

class Package:
    def __init__(self, pid, address, city, state, zipcode, deadline, weight, status):
        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure = None
        self.delivery = None
        self.truck_number = None

    def __str__(self):

        return "ID: %s, %s, %s, %s, %s, Deadline: %s, Weight: %s, %s, Departure: %s, Delivery: %s, Truck # %s" % (
            self.pid, self.address, self.city, self.state, self.zipcode,
            self.deadline, self.weight, self.status, self.departure, self.delivery, self.truck_number)

    def update_status(self, convert_timedelta):

        if self.delivery is not None and convert_timedelta >= self.delivery:
            self.status = "Delivered"
        elif self.departure is not None and convert_timedelta >= self.departure:
            self.status = "En route"
        else:
            self.status = "At Hub"

        if self.pid == 9:
            if convert_timedelta > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 State St"
                self.zipcode = "84111"
        return self.status


