import collections

class LRUCache:
    """
    Implements a Least Recently Used (LRU) cache.

    An LRU cache evicts the least recently used item when the cache
    reaches its capacity. This implementation leverages Python's
    `collections.OrderedDict` which provides a hash map (dictionary)
    functionality combined with a doubly linked list to maintain insertion
    order. This allows for O(1) average time complexity for `get` and `put`
    operations, as it efficiently handles key lookups, item access/update
    (moving to end), and item eviction (removing from front).

    Methods:
        get(key): Retrieves an item from the cache.
        put(key, value): Adds or updates an item in the cache.
    """

    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.

        Args:
            capacity: The maximum number of items the cache can hold.
                      Must be a positive integer.
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        # _cache stores key-value pairs. OrderedDict maintains the order
        # of items. The end of the dict represents the most recently used (MRU)
        # item, and the beginning represents the least recently used (LRU) item.
        self._cache = collections.OrderedDict()

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with the given key.

        If the key exists, its corresponding item is marked as most recently used
        by moving it to the end of the `OrderedDict`.
        If the key does not exist, returns -1.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not found.
        """
        if key not in self._cache:
            return -1

        # Move the accessed item to the end to mark it as most recently used.
        # This operation is efficient for OrderedDict.
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key: int, value: int) -> None:
        """
        Adds a new item to the cache or updates an existing item.

        If the key already exists:
            Its value is updated, and it's marked as most recently used
            by moving it to the end of the `OrderedDict`.
        If the key does not exist:
            If the cache is already at capacity, the least recently used item
            (the one at the front of the `OrderedDict`) is removed.
            Then, the new item is added to the cache (which places it at the
            end, marking it as most recently used).

        Args:
            key: The key of the item to add or update.
            value: The value associated with the key.
        """
        if key in self._cache:
            # If key exists, update its value and move it to the end
            # (most recently used).
            self._cache[key] = value
            self._cache.move_to_end(key)
        else:
            # If key does not exist.
            if len(self._cache) >= self.capacity:
                # Cache is full, remove the least recently used item.
                # popitem(last=False) removes the first (oldest/LRU) item.
                self._cache.popitem(last=False)
            
            # Add the new item. It's automatically placed at the end,
            # making it the most recently used.
            self._cache[key] = value

    def __len__(self):
        """Returns the current number of items in the cache."""
        return len(self._cache)

    def __repr__(self):
        """Returns a string representation of the cache."""
        return f"LRUCache({dict(self._cache)}, capacity={self.capacity})"

# Example Usage (optional, not part of the snippet but useful for testing):
# if __name__ == '__main__':
#     cache = LRUCache(2)
#
#     cache.put(1, 1) # cache: {1: 1}
#     cache.put(2, 2) # cache: {1: 1, 2: 2}
#     print(cache.get(1)) # returns 1; cache: {2: 2, 1: 1} (1 is now MRU)
#
#     cache.put(3, 3) # evicts key 2 (LRU); cache: {1: 1, 3: 3}
#     print(cache.get(2)) # returns -1 (not found)
#
#     cache.put(4, 4) # evicts key 1 (LRU); cache: {3: 3, 4: 4}
#     print(cache.get(1)) # returns -1 (not found)
#     print(cache.get(3)) # returns 3; cache: {4: 4, 3: 3}
#     print(cache.get(4)) # returns 4; cache: {3: 3, 4: 4}
#
#     print(cache) # Example: LRUCache({3: 3, 4: 4}, capacity=2)