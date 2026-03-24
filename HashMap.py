import datetime
class HashMap:
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    def insert(self, key, item):

        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:  # O(N) CPU time

            if kv[0] == key:
                kv[1] = item
                return True


        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def get(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None

    def remove_hash(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]

        # If key is found remove it
        if key in destination:
            destination.remove(key)

    def to_dict(self):
        result = {}

        for bucket in self.list:
            if bucket:
                for key, value in bucket:
                    result[key] = serialize(value)

        return result

def serialize(obj):
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(v) for v in obj]
    elif isinstance(obj, datetime.timedelta):
        return str(obj)
    elif hasattr(obj, "__dict__"):
        return serialize(obj.__dict__)
    else:
        return obj

