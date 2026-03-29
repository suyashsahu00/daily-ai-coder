import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    This decorator caches the results of function calls based on their arguments.
    If the function is called again with the same arguments, the cached result
    is returned instead of re-executing the function. This is highly useful for
    optimizing recursive functions (like Fibonacci) or functions with expensive
    computations that might be called multiple times with identical inputs.

    Note: This memoizer assumes all function arguments are hashable (e.g., numbers,
    strings, tuples, frozensets). If arguments include unhashable types like lists
    or dictionaries directly, it will raise a TypeError.

    Usage Example:
        @memoize
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        # The first call computes and caches results for fibonacci(0) through fibonacci(10)
        print(f"Fibonacci(10): {fibonacci(10)}")

        # Subsequent calls with the same argument return instantly from cache
        print(f"Fibonacci(10) again: {fibonacci(10)}")

        @memoize
        def expensive_calculation(x, y=0):
            import time
            print(f"Calculating {x}, {y}...")
            time.sleep(0.5) # Simulate a delay
            return x * x + y

        print(f"Result 1: {expensive_calculation(5)}") # Calculates
        print(f"Result 2: {expensive_calculation(5)}") # Cached
        print(f"Result 3: {expensive_calculation(3, y=1)}") # Calculates
        print(f"Result 4: {expensive_calculation(3, y=1)}") # Cached
    """
    cache = {}  # Dictionary to store cached results (argument tuple -> result)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique, hashable key for the current function call.
        # This key must represent all arguments (positional and keyword)
        # consistently, regardless of keyword argument order.
        # We use a tuple for positional args and a frozenset of (key, value)
        # pairs for keyword args to ensure hashability and order independence.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for these arguments is already in the cache,
            # return the cached value immediately.
            return cache[key]
        else:
            # If the result is not in the cache, execute the original function.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it.
            cache[key] = result
            return result
    return wrapper