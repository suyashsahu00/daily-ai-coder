import functools

def memoize(func):
    """
    Decorator that caches a function's results for given arguments.

    This can significantly speed up functions that are called repeatedly
    with the same arguments, especially pure functions or recursive ones.
    """
    cache = {} # Dictionary to store cached results. Keys are function arguments, values are results.

    @functools.wraps(func) # Preserves the original function's metadata (name, docstring, etc.)
    def wrapper(*args, **kwargs):
        # Create a unique, hashable key from the function arguments.
        # *args are converted to a tuple.
        # **kwargs are sorted by key and converted to a tuple of (key, value) pairs
        # to ensure consistent cache keys regardless of argument order.
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            # If the result for these arguments is already in the cache, return it directly.
            return cache[key]
        else:
            # If not in cache, call the original function with its arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning.
            cache[key] = result
            return result
    return wrapper

# Example usage (not part of the snippet, but demonstrates how it works):
# @memoize
# def fibonacci(n):
#     """Calculates the Nth Fibonacci number recursively."""
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)

# print(fibonacci(10)) # Computes and caches results
# print(fibonacci(10)) # Retrieves result from cache instantly
# print(fibonacci(30)) # Computes larger numbers efficiently due to caching sub-problems