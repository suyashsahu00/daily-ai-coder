import collections

class LRUCache:
    """
    A simple Least Recently Used (LRU) Cache implementation.

    This cache stores key-value pairs and has a fixed capacity. When the cache
    exceeds its capacity, it evicts the least recently used item.
    It leverages Python's collections.OrderedDict, which maintains insertion
    order and allows efficient moving of items.

    Methods:
        __init__(capacity): Initializes the cache with a given capacity.
        get(key): Retrieves the value for a given key. Moves the key to the
                  most recently used position.
        put(key, value): Inserts or updates a key-value pair. If capacity is
                         exceeded, evicts the least recently used item.
    """
    def __init__(self, capacity: int):
        # Stores the maximum number of items the cache can hold.
        self.capacity = capacity
        # OrderedDict acts as a combination of a hash map and a doubly linked list.
        # It allows O(1) average time complexity for access/deletion by key,
        # and also maintains the order of insertion, which is crucial for LRU.
        self.cache = collections.OrderedDict()

    def get(self, key: int) -> int:
        """
        Retrieves an item from the cache.

        If the key exists, its value is returned. The key is then marked as
        "most recently used" by moving it to the end of the OrderedDict.
        If the key does not exist, -1 is returned.
        """
        if key not in self.cache:
            return -1

        # Retrieve the value.
        value = self.cache[key]
        # To mark it as most recently used, we pop it and then re-insert it
        # at the end of the OrderedDict. This operation is efficient.
        self.cache.move_to_end(key)
        return value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates an item in the cache.

        If the key already exists, its value is updated, and it's moved to
        the "most recently used" end.
        If the key is new, it's added. If this addition causes the cache to
        exceed its capacity, the least recently used item (at the beginning
        of the OrderedDict) is removed.
        """
        if key in self.cache:
            # If the key already exists, update its value.
            self.cache[key] = value
            # Move it to the end to mark it as most recently used.
            self.cache.move_to_end(key)
        else:
            # If the key is new, add it.
            self.cache[key] = value
            # If adding the new item exceeds the cache capacity,
            # remove the least recently used item.
            if len(self.cache) > self.capacity:
                # popitem(last=False) removes the first (oldest/LRU) item.
                self.cache.popitem(last=False)