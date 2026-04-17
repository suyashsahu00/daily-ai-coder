import collections

class LRUCache:
    """
    Implements a Least Recently Used (LRU) Cache.

    An LRU cache evicts the least recently used item when the cache
    reaches its capacity and a new item needs to be added.
    This implementation uses collections.OrderedDict for efficient
    tracking of item order and O(1) operations for get, put, and eviction.
    """

    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.

        Args:
            capacity: The maximum number of items the cache can hold.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        # OrderedDict stores items in the order they were inserted.
        # It also supports efficient reordering (moving to end) and
        # popping the first (least recently used) item.
        self.cache = collections.OrderedDict()

    def get(self, key: int) -> int:
        """
        Retrieves an item from the cache.

        If the key exists, its value is returned, and the item is
        marked as most recently used (moved to the end of the order).
        If the key does not exist, -1 is returned.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value associated with the key, or -1 if not found.
        """
        if key not in self.cache:
            return -1
        
        # Get the value
        value = self.cache[key]
        
        # Mark as most recently used by moving to the end of the OrderedDict.
        # The 'last=True' argument to move_to_end ensures it goes to the end.
        self.cache.move_to_end(key)
        return value

    def put(self, key: int, value: int) -> None:
        """
        Adds or updates an item in the cache.

        If the key already exists, its value is updated, and the item is
        marked as most recently used.
        If the key does not exist and the cache is at capacity, the
        least recently used item (the first item in OrderedDict) is
        evicted before the new item is added.

        Args:
            key: The key of the item to add/update.
            value: The value of the item to add/update.
        """
        if key in self.cache:
            # If key already exists, update its value and mark as most recently used.
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            # If key does not exist
            if len(self.cache) >= self.capacity:
                # If cache is full, evict the least recently used item.
                # popitem(last=False) removes and returns the first (LRU) item.
                self.cache.popitem(last=False)
            
            # Add the new item. It will automatically be at the end (MRU).
            self.cache[key] = value