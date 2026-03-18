import collections

class LRUCache:
    """
    Implements a Least Recently Used (LRU) cache.

    An LRU cache evicts the least recently used items when the cache reaches its capacity.
    This implementation uses Python's `collections.OrderedDict`, which provides
    O(1) average time complexity for insertion, deletion, lookup, and moving items
    to the end (marking them as recently used).
    """

    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a specified capacity.

        Args:
            capacity: The maximum number of key-value pairs the cache can hold.
        """
        if capacity <= 0:
            raise ValueError("Cache capacity must be a positive integer.")
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with a key from the cache.

        If the key exists, its corresponding item is marked as "most recently used"
        by moving it to the end of the OrderedDict.

        Args:
            key: The key to retrieve.

        Returns:
            The value associated with the key if found, otherwise -1.
        """
        if key not in self.cache:
            return -1
        
        # If the key exists, retrieve its value.
        value = self.cache.pop(key)
        # Move the item to the end to mark it as most recently used.
        self.cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        """
        Adds or updates a key-value pair in the cache.

        If the key already exists, its value is updated, and the item is
        marked as "most recently used".
        If the key does not exist and the cache is full, the least recently
        used item (at the beginning of the OrderedDict) is evicted to make space.
        The new item is then added as "most recently used".

        Args:
            key: The key to add or update.
            value: The value to associate with the key.
        """
        if key in self.cache:
            # If the key already exists, remove it first so it can be re-added
            # at the end (most recently used position).
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # If the cache is full and it's a new key,
            # remove the least recently used item (the first item in OrderedDict).
            # popitem(last=False) removes from the beginning.
            self.cache.popitem(last=False)
        
        # Add the new or updated key-value pair to the end,
        # marking it as most recently used.
        self.cache[key] = value

# Example Usage:
# # cache = LRUCache(2)
# # cache.put(1, 1) # cache is {1: 1}
# # cache.put(2, 2) # cache is {1: 1, 2: 2}
# # cache.get(1)    # returns 1; cache is {2: 2, 1: 1} (1 is now MRU)
# # cache.put(3, 3) # evicts key 2 (LRU); cache is {1: 1, 3: 3}
# # cache.get(2)    # returns -1 (not found)
# # cache.put(4, 4) # evicts key 1 (LRU); cache is {3: 3, 4: 4}
# # cache.get(1)    # returns -1 (not found)
# # cache.get(3)    # returns 3; cache is {4: 4, 3: 3}
# # cache.get(4)    # returns 4; cache is {3: 3, 4: 4}