import functools

def memoize(func):
    """
    A decorator that caches the results of a function.
    Useful for optimizing recursive functions with overlapping subproblems (dynamic programming)
    or any function where the same inputs produce the same outputs and computation is expensive.

    The cache is stored in a dictionary associated with the function itself.
    It works for functions whose arguments are hashable (e.g., numbers, strings, tuples).
    """
    cache = {} # This dictionary will store the cached results.

    @functools.wraps(func) # Preserves the original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function arguments.
        # Positional arguments are stored as a tuple.
        # Keyword arguments are stored as a frozenset of (key, value) pairs.
        # Using frozenset ensures order-independence for keyword arguments and hashability.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for this specific set of arguments is already in the cache,
            # return it directly without re-computing.
            return cache[key]
        else:
            # If not in cache, call the original function to compute the result.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it,
            # so subsequent calls with the same arguments can use the cached value.
            cache[key] = result
            return result
    return wrapper

# Example Usage (uncomment to test):
#
# @memoize
# def fibonacci(n):
#     """Calculates the nth Fibonacci number."""
#     if n <= 1:
#         return n
#     # Without memoization, this would re-compute fibonacci(n-2) multiple times.
#     # With memoization, each fibonacci(k) is computed only once.
#     return fibonacci(n-1) + fibonacci(n-2)
#
# print("Calculating fibonacci(10):", fibonacci(10)) # Fast
# print("Calculating fibonacci(30):", fibonacci(30)) # Very fast due to memoization
# print("Calculating fibonacci(50):", fibonacci(50)) # Also very fast
#
# @memoize
# def expensive_calculation(a, b, operation="add"):
#     """Simulates a time-consuming calculation."""
#     import time
#     print(f"Actually performing {operation} on {a} and {b}...")
#     time.sleep(0.5) # Simulate a delay
#     if operation == "add":
#         return a + b
#     elif operation == "multiply":
#         return a * b
#     return None
#
# print(expensive_calculation(5, 3))                     # First call, computes
# print(expensive_calculation(5, 3))                     # Returns from cache instantly
# print(expensive_calculation(10, 2, operation="multiply")) # New arguments, computes
# print(expensive_calculation(5, 3, operation="add"))    # Same as first call, returns from cache
# print(expensive_calculation(10, 2, operation="multiply")) # Same as above, returns from cache
# print(expensive_calculation(10, 2))                    # Different operation (default "add"), computes