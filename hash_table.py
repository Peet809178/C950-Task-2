class HashTable:
    def __init__(self, capacity=40):
        """
        Initializes the hash table with a fixed number of buckets.
        Each bucket is a list to handle collisions via chaining.
        """
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]  # List of lists (buckets)

    def _hash(self, key):
        """
        Computes the hash index for a given key using modulo.
        Ensures keys are distributed across available buckets.
        """
        return int(key) % self.capacity

    def insert(self, key, item):
        """
        Inserts an item into the hash table with the specified key.
        If the key already exists, it updates the existing item.
        """
        index = self._hash(key)
        bucket = self.table[index]

        # Update the item if the key already exists
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, item)
                return

        # Otherwise, append a new key-item pair
        bucket.append((key, item))

    def lookup(self, key):
        """
        Searches for and returns the item associated with the given key.
        Returns None if the key is not found.
        """
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        """
        Removes the item associated with the given key.
        Returns True if the item was found and removed, False otherwise.
        """
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False
