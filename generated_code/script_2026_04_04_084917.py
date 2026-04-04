import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    This decorator caches the results of function calls based on their arguments.
    If the function is called again with the same arguments, the cached result
    is returned instead of re-executing the function. This can significantly
    speed up functions that are called repeatedly with the same inputs,
    especially recursive functions (e.g., Fibonacci, factorial).

    It uses functools.wraps to preserve the original function's metadata
    (like its name and docstring), which is good practice for decorators.
    The cache is stored in a dictionary within the closure of the decorator.
    """
    cache = {}  # Initialize an empty dictionary to store cached results

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a hashable key for the cache.
        # Positional arguments `args` are already a tuple, which is hashable.
        # Keyword arguments `kwargs` are a dictionary, which is not hashable.
        # To make kwargs hashable, we convert them to a tuple of sorted (key, value) pairs.
        # Sorting ensures that {a=1, b=2} and {b=2, a=1} produce the same cache key.
        cache_key = (args, tuple(sorted(kwargs.items())))

        if cache_key in cache:
            # If the result for these arguments is already in the cache,
            # return the cached value directly.
            return cache[cache_key]
        else:
            # If the result is not in the cache, call the original function
            # with the provided arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it.
            cache[cache_key] = result
            return result
    return wrapper

# Example usage:
# import time
#
# @memoize
# def slow_fibonacci(n):
#     """Calculates the nth Fibonacci number slowly without memoization, fast with it."""
#     if n <= 1:
#         return n
#     return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)
#
# @memoize
# def compute_something_expensive(a, b, keyword_arg=0):
#     """Simulates an expensive computation."""
#     time.sleep(0.5) # Simulate work
#     return a + b + keyword_arg
#
# print("--- Fibonacci Example ---")
# start_time = time.time()
# print(f"fibonacci(10) = {slow_fibonacci(10)}")
# print(f"fibonacci(25) = {slow_fibonacci(25)}") # This call will be significantly faster due to caching
# print(f"Time taken for fibonacci: {time.time() - start_time:.4f} seconds\n")
#
# print("--- Expensive Computation Example ---")
# start_time = time.time()
# print(f"Compute(1, 2) = {compute_something_expensive(1, 2)}") # First call, will take ~0.5s
# print(f"Compute(1, 2) = {compute_something_expensive(1, 2)}") # Second call, instant from cache
# print(f"Compute(3, 4, keyword_arg=1) = {compute_something_expensive(3, 4, keyword_arg=1)}") # New args, ~0.5s
# print(f"Compute(3, 4, keyword_arg=1) = {compute_something_expensive(3, 4, keyword_arg=1)}") # Instant from cache
# print(f"Compute(3, 4, keyword_arg=0) = {compute_something_expensive(3, 4, keyword_arg=0)}") # Different kwarg, ~0.5s
# print(f"Time taken for expensive computation: {time.time() - start_time:.4f} seconds")