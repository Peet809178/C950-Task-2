class HashTable:
    def __init__(self, capacity=40):
        # Initialize the table with empty buckets
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # Array of lists

    def _hash(self, key):
        # Hash function using modulo
        return int(key) % self.capacity

    def insert(self, key, item):
        # Inserts or updates an item
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, item)
                return
        bucket.append((key, item))

    def lookup(self, key):
        # Retrieves an item by key
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        # Removes an item by key
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False