import functools

def memoize(func):
    """
    A decorator that caches the results of a function call.

    This decorator is useful for optimizing functions that are called
    multiple times with the same arguments, especially recursive functions
    or functions with expensive computations.

    The cache stores results in a dictionary where keys are the function's
    arguments (as a tuple) and values are the computed results.

    Limitations:
    - The function's arguments must be hashable (e.g., numbers, strings, tuples).
      Mutable arguments like lists or dictionaries cannot be used directly.
    - The cache grows indefinitely. For large numbers of unique arguments,
      consider a cache with a size limit (e.g., `functools.lru_cache`).
    - Does not handle keyword arguments differently from positional arguments
      unless normalized. For simplicity, this version treats `(1, 2)` and `(a=1, b=2)`
      as distinct if passed directly, or requires consistent calling style.
      `functools.lru_cache` handles this more robustly.
    """
    cache = {}  # The dictionary to store cached results

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Convert positional arguments to a tuple to use as a dictionary key.
        # This assumes keyword arguments are not used or are consistent,
        # otherwise `kwargs` would also need to be made hashable and included in the key.
        # For this simple memoize, we'll only cache based on positional args.
        # If kwargs are present, we skip caching to avoid complexity, or raise an error.
        if kwargs:
            # For simplicity, if keyword arguments are used, we don't cache
            # or could raise an error if strict caching is desired.
            # `functools.lru_cache` handles this by normalizing args and kwargs.
            return func(*args, **kwargs)

        if args in cache:
            # If the arguments are in the cache, return the stored result.
            return cache[args]
        else:
            # If not in cache, call the original function.
            result = func(*args, **kwargs)
            # Store the result in the cache for future calls with the same arguments.
            cache[args] = result
            # Return the newly computed result.
            return result
    return wrapper

# Example Usage:
# @memoize
# def fibonacci(n):
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)

# # Without memoization, fibonacci(30) would be very slow due to redundant calculations.
# # With memoization, each fibonacci(k) is calculated only once.
# print(fibonacci(10)) # Output: 55
# print(fibonacci(30)) # Output: 832040

# # Example with a non-recursive function:
# @memoize
# def expensive_calculation(a, b):
#     import time
#     time.sleep(1) # Simulate an expensive operation
#     return a * b

# print("First call (will take 1 second):")
# print(expensive_calculation(2, 3))
# print("Second call (instant due to cache):")
# print(expensive_calculation(2, 3))
# print("Third call (will take 1 second for new arguments):")
# print(expensive_calculation(4, 5))