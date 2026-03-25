import functools

def memoize(func):
    """
    A decorator that caches the results of a function call.

    This decorator stores the result of `func(*args, **kwargs)` in an internal
    dictionary (`_cache`) and returns the cached result immediately if the
    function is called again with the same arguments. This can significantly
    speed up functions that are called frequently with identical inputs,
    especially if those functions are computationally expensive.

    The cache key is created from the function's positional and keyword arguments.
    It assumes that all arguments passed to the decorated function are hashable
    (e.g., numbers, strings, tuples, frozensets). If non-hashable arguments
    (like lists or dictionaries) are used, this memoization will fail.
    """
    _cache = {}  # Dictionary to store cached results, mapping (args, kwargs) to result.

    @functools.wraps(func)  # Preserves the original function's metadata (e.g., name, docstring).
    def wrapper(*args, **kwargs):
        # Create a unique cache key from the function's arguments.
        # Positional arguments are stored as a tuple.
        # Keyword arguments are stored as a frozenset of (key, value) pairs
        # to ensure the key is hashable and order-independent for kwargs.
        key = (args, frozenset(kwargs.items()))

        # Check if the result for these specific arguments is already in the cache.
        if key not in _cache:
            # If the result is not cached, call the original function.
            result = func(*args, **kwargs)
            # Store the computed result in the cache for future use.
            _cache[key] = result
        else:
            # If the result is cached, retrieve it directly.
            result = _cache[key]
        
        return result

    # Attach a method to the wrapper function to allow clearing the cache.
    # This is useful for testing, when inputs change, or for memory management.
    wrapper.cache_clear = _cache.clear
    
    return wrapper

# --- Example Usage (commented out to return ONLY the raw python code) ---
# import time
#
# @memoize
# def expensive_calculation(a, b, operation='add'):
#     """Simulates a slow, expensive function."""
#     time.sleep(1) # Simulate a 1-second delay
#     if operation == 'add':
#         return a + b
#     elif operation == 'multiply':
#         return a * b
#     else:
#         raise ValueError("Unsupported operation")
#
# print("First call to expensive_calculation(10, 5, 'add')... (should take time)")
# start_time = time.time()
# result1 = expensive_calculation(10, 5, 'add')
# end_time = time.time()
# print(f"Result: {result1}, Time taken: {end_time - start_time:.2f}s\n")
#
# print("Second call to expensive_calculation(10, 5, 'add')... (should be instant)")
# start_time = time.time()
# result2 = expensive_calculation(10, 5, 'add')
# end_time = time.time()
# print(f"Result: {result2}, Time taken: {end_time - start_time:.2f}s\n")
#
# print("Third call to expensive_calculation with keyword args (a=10, b=5)... (should be instant)")
# start_time = time.time()
# result3 = expensive_calculation(a=10, b=5, operation='add')
# end_time = time.time()
# print(f"Result: {result3}, Time taken: {end_time - start_time:.2f}s\n")
#
# print("Fourth call with different operation (10, 5, 'multiply')... (should take time)")
# start_time = time.time()
# result4 = expensive_calculation(10, 5, 'multiply')
# end_time = time.time()
# print(f"Result: {result4}, Time taken: {end_time - start_time:.2f}s\n")
#
# print("Clearing the cache...")
# expensive_calculation.cache_clear()
#
# print("Fifth call to expensive_calculation(10, 5, 'add') after clearing cache... (should take time again)")
# start_time = time.time()
# result5 = expensive_calculation(10, 5, 'add')
# end_time = time.time()
# print(f"Result: {result5}, Time taken: {end_time - start_time:.2f}s\n")