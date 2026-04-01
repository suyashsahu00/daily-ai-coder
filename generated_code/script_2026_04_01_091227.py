import functools

def memoize(func):
    """
    A simple memoization decorator for functions with hashable arguments.

    This decorator stores the results of function calls and returns the
    cached result when the same inputs occur again, avoiding redundant computations.
    It's particularly useful for pure functions (functions that always
    produce the same output for the same input and have no side effects)
    with expensive computations.

    Args:
        func (callable): The function to be memoized.

    Returns:
        callable: The wrapped, memoized function.
    """
    cache = {}  # Dictionary to store cached results

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on function arguments.
        # Arguments must be hashable. If kwargs are used, they are sorted
        # and converted to a frozenset to ensure the same key for different
        # argument order and to make the key hashable.
        key = (args, frozenset(kwargs.items()))

        if key not in cache:
            # If the result is not in the cache, call the original function
            # and store its result.
            cache[key] = func(*args, **kwargs)
        return cache[key]  # Return the cached result

    return wrapper

# Example Usage (uncomment to test):
# @memoize
# def fibonacci(n):
#     """Calculates the nth Fibonacci number recursively."""
#     if n < 2:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)

# print("Calculating fibonacci(10) for the first time...")
# print(f"fibonacci(10) = {fibonacci(10)}") # Computes and caches
# print("\nCalculating fibonacci(10) again (should be instant due to cache)...")
# print(f"fibonacci(10) = {fibonacci(10)}") # Returns cached result immediately

# @memoize
# def expensive_operation(a, b, c="default"):
#     """An example of an expensive operation."""
#     import time
#     time.sleep(1) # Simulate expensive computation
#     return f"Result for {a}, {b}, {c}"

# print("\nCalling expensive_operation(1, 2)...")
# print(expensive_operation(1, 2)) # Computes and caches
# print("\nCalling expensive_operation(1, 2) again...")
# print(expensive_operation(1, 2)) # Returns cached result
# print("\nCalling expensive_operation(1, 2, c='custom')...")
# print(expensive_operation(1, 2, c='custom')) # New key, computes