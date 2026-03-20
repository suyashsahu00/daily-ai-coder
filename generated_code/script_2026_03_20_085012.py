import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    Memoization stores the results of expensive function calls and returns the
    cached result when the same inputs occur again. This can significantly
    speed up functions that are called repeatedly with the same arguments.

    Constraints:
    1. The decorated function must be pure (i.e., given the same inputs, it
       always produces the same output and has no side effects).
    2. The arguments to the decorated function must be hashable, as they are
       used as dictionary keys for the cache.

    Usage:
        @memoize
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)

        print(fibonacci(10)) # Computes and caches
        print(fibonacci(10)) # Returns cached result immediately
        print(fibonacci(5))  # Computes and caches
    """
    cache = {} # This dictionary will store the results of func calls

    @functools.wraps(func) # Preserves the original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on the function arguments.
        # We need to handle both positional and keyword arguments.
        # For kwargs, convert them to a sorted tuple of (key, value) pairs to ensure
        # the key is hashable and order-independent.
        key = (args, tuple(sorted(kwargs.items())))

        if key not in cache:
            # If the result for this key is not in the cache, call the original function
            # and store its result.
            cache[key] = func(*args, **kwargs)
        
        # Return the cached result (either newly computed or previously stored).
        return cache[key]

    return wrapper

# Example usage:
if __name__ == '__main__':
    import time

    @memoize
    def expensive_fibonacci(n):
        """
        Calculates the nth Fibonacci number with a simulated delay.
        This function demonstrates the benefit of memoization.
        """
        time.sleep(0.01) # Simulate an expensive computation
        if n < 2:
            return n
        return expensive_fibonacci(n-1) + expensive_fibonacci(n-2)

    print("Calculating fib(10) for the first time...")
    start_time = time.time()
    result1 = expensive_fibonacci(10)
    end_time = time.time()
    print(f"fib(10) = {result1}, Time taken: {end_time - start_time:.4f} seconds")

    print("\nCalculating fib(10) again (should be fast due to memoization)...")
    start_time = time.time()
    result2 = expensive_fibonacci(10)
    end_time = time.time()
    print(f"fib(10) = {result2}, Time taken: {end_time - start_time:.4f} seconds")

    print("\nCalculating fib(5)...")
    start_time = time.time()
    result3 = expensive_fibonacci(5)
    end_time = time.time()
    print(f"fib(5) = {result3}, Time taken: {end_time - start_time:.4f} seconds")

    print("\nCalculating fib(5) again (should be fast)...")
    start_time = time.time()
    result4 = expensive_fibonacci(5)
    end_time = time.time()
    print(f"fib(5) = {result4}, Time taken: {end_time - start_time:.4f} seconds")

    # Python's built-in functools.lru_cache is often preferred for production use
    # as it offers more features (e.g., max size, thread safety).
    # This custom memoize decorator serves as a clear illustration of the concept.
    # from functools import lru_cache
    # @lru_cache(maxsize=None)
    # def fibonacci_lru(n):
    #     if n < 2:
    #         return n
    #     return fibonacci_lru(n-1) + fibonacci_lru(n-2)
    # print(f"\nFibonacci with lru_cache(10): {fibonacci_lru(10)}")