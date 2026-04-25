import functools

def memoize(func):
    """
    A simple memoization decorator for functions with hashable arguments.

    Memoization is an optimization technique that speeds up programs by storing
    the results of expensive function calls and returning the cached result
    when the same inputs occur again.

    This decorator stores the results of `func` calls in a dictionary `cache`.
    The cache key is a tuple containing the positional arguments and a frozenset
    of keyword argument items. This approach ensures that:
    1. The cache key is hashable (required for dictionary keys).
    2. The order of positional arguments is preserved.
    3. The order of keyword arguments does not affect the cache key
       (e.g., `func(a=1, b=2)` is treated the same as `func(b=2, a=1)`).

    Limitations:
    - All positional and keyword arguments passed to the decorated function
      must be hashable (e.g., numbers, strings, tuples, frozensets).
      It will not work directly with mutable arguments like lists, dictionaries,
      or custom objects unless they implement a custom `__hash__` method.
    - It does not have a cache expiration mechanism (LRU, LFU, etc.).
      The cache grows indefinitely with unique argument combinations.

    Usage:
    @memoize
    def expensive_computation(a, b):
        # Simulate an expensive operation
        import time
        time.sleep(1)
        print(f"Actually computing {a} + {b}")
        return a + b

    print(expensive_computation(1, 2))  # Computes and caches
    print(expensive_computation(1, 2))  # Returns cached result instantly
    print(expensive_computation(b=4, a=3)) # Computes and caches
    print(expensive_computation(3, 4))  # Returns cached result instantly (due to kwarg handling)
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a consistent cache key from both positional and keyword arguments.
        # `args` is already a tuple. `kwargs.items()` gives (key, value) pairs.
        # `frozenset` is used for kwargs to ensure hashability and order independence.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result is in the cache, return it directly.
            return cache[key]
        else:
            # If not in cache, call the original function, store the result, and then return it.
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    return wrapper

# Example usage (uncomment to test):
# @memoize
# def fibonacci(n):
#     if n <= 1:
#         return n
#     return fibonacci(n-1) + fibonacci(n-2)

# print("Calculating fibonacci(10)...")
# print(fibonacci(10)) # This will compute fibonacci(10) and all its sub-problems once
# print("Calculating fibonacci(10) again...")
# print(fibonacci(10)) # This will return instantly from cache

# @memoize
# def greet(name, greeting="Hello"):
#     import time
#     time.sleep(0.5)
#     print(f"Actually computing greet for {name} with '{greeting}'")
#     return f"{greeting}, {name}!"

# print(greet("Alice"))
# print(greet("Alice")) # Cached
# print(greet("Bob", greeting="Hi"))
# print(greet(name="Bob", greeting="Hi")) # Cached, handles kwargs order
# print(greet("Alice", greeting="Hey")) # New key, computes