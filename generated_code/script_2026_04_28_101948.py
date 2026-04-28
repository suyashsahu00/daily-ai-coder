def memoize(func):
    """
    A simple memoization decorator for functions.

    This decorator stores the results of function calls in a cache,
    mapping function arguments to their return values. If the function
    is called again with the same arguments, the cached result is
    returned instead of re-executing the function, significantly
    speeding up computation for functions with repetitive inputs.

    Note: This memoizer assumes that all function arguments are hashable.
          It treats positional arguments as a tuple for the cache key.
          For more advanced caching, handling of unhashable arguments,
          or keyword arguments, consider `functools.lru_cache`.
    """
    cache = {} # The dictionary to store cached results

    def wrapper(*args):
        # Create a hashable key from the function's positional arguments.
        # This assumes all arguments in `args` are hashable (e.g., numbers, strings, tuples).
        # Lists or dictionaries as arguments would raise a TypeError.
        key = args

        if key in cache:
            # If the result for these specific arguments is already in the cache,
            # return the cached value directly without re-executing `func`.
            return cache[key]
        else:
            # If the result is not in the cache, call the original function with the arguments.
            result = func(*args)
            # Store the newly computed result in the cache before returning it.
            # This ensures that subsequent calls with the same `key` will use the cached value.
            cache[key] = result
            return result
    return wrapper

# --- Example Usage ---

# Define a recursive function, typically one that would benefit from memoization
@memoize
def fibonacci(n):
    """
    Computes the n-th Fibonacci number.
    Without memoization, this recursive implementation would be very slow for large n
    due to repeated calculations of the same sub-problems.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@memoize
def factorial(n):
    """
    Computes the factorial of n.
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)

if __name__ == '__main__':
    print("--- Testing Fibonacci with memoization ---")
    print(f"fibonacci(10) = {fibonacci(10)}") # Computes relatively fast
    print(f"fibonacci(30) = {fibonacci(30)}") # Should be very fast due to caching of intermediate results
    print(f"fibonacci(35) = {fibonacci(35)}") # Still fast due to caching

    print("\n--- Testing Factorial with memoization ---")
    print(f"factorial(5) = {factorial(5)}")   # Computes
    print(f"factorial(10) = {factorial(10)}") # Computes (likely reuses 5!)
    print(f"factorial(5) = {factorial(5)}")   # Instant, retrieved from cache