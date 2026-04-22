import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    Memoization is an optimization technique that stores the results of
    expensive function calls and returns the cached result when the same
    inputs occur again. This avoids redundant computations.

    This decorator works by maintaining a dictionary (cache) where keys
    are created from the arguments passed to the function, and values
    are the function's computed results.

    Assumptions:
    1.  The decorated function should be 'pure': given the same inputs,
        it must always produce the same output and have no side effects.
    2.  All function arguments (both positional and keyword) must be hashable.
        This is necessary because they are used as dictionary keys.
        (e.g., numbers, strings, tuples are hashable; lists, dictionaries are not).
    """
    _cache = {}  # Initialize a dictionary to store cached results

    # @functools.wraps preserves the original function's name, docstring,
    # and other metadata, which is good practice for decorators.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique, hashable key for the cache based on function arguments.
        # `args` is already a tuple, which is hashable.
        # `kwargs` is a dictionary, which is not hashable. We convert its items
        # into a frozenset of (key, value) tuples to make it hashable and
        # ensure that the order of keyword arguments doesn't affect the cache key.
        key = (args, frozenset(kwargs.items()))

        # Check if the result for these specific arguments is already in the cache.
        if key in _cache:
            # If found, return the cached result immediately.
            return _cache[key]
        else:
            # If not in cache, call the original function to compute the result.
            result = func(*args, **kwargs)
            # Store the newly computed result in the cache before returning it.
            _cache[key] = result
            return result
    return wrapper

# --- Example Usage ---

if __name__ == "__main__":
    @memoize
    def fibonacci(n):
        """
        Computes the nth Fibonacci number recursively.
        This function has overlapping subproblems, making it a classic
        candidate for memoization to drastically improve performance.
        """
        print(f"Calculating fibonacci({n})...") # Only prints if not cached
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    @memoize
    def expensive_square_sum(a, b=0, c=0):
        """
        An example of a function with keyword arguments that simulates
        an expensive computation.
        """
        import time
        print(f"Performing expensive calculation for a={a}, b={b}, c={c}...")
        time.sleep(0.5) # Simulate a long computation
        return a**2 + b**2 + c**2

    print("--- Fibonacci Example ---")
    print(f"fibonacci(5) = {fibonacci(5)}") # This will calculate and cache subproblems
    print(f"fibonacci(5) = {fibonacci(5)}") # This will be instant, using cache
    print(f"fibonacci(8) = {fibonacci(8)}") # Calculates missing subproblems, uses existing cache
    print(f"fibonacci(8) = {fibonacci(8)}") # Instant, fully cached

    print("\n--- Expensive Square Sum Example ---")
    print(f"expensive_square_sum(1, b=2, c=3) = {expensive_square_sum(1, b=2, c=3)}")
    print(f"expensive_square_sum(1, c=3, b=2) = {expensive_square_sum(1, c=3, b=2)}") # Keyword order doesn't matter, cached!
    print(f"expensive_square_sum(5) = {expensive_square_sum(5)}") # Uses default b=0, c=0
    print(f"expensive_square_sum(5, b=0) = {expensive_square_sum(5, b=0)}") # Same as above, cached!
    print(f"expensive_square_sum(5, c=0, b=0) = {expensive_square_sum(5, c=0, b=0)}") # Still same, cached!
    print(f"expensive_square_sum(10, b=1) = {expensive_square_sum(10, b=1)}") # New arguments, calculates
    print(f"expensive_square_sum(10, b=1) = {expensive_square_sum(10, b=1)}") # Cached