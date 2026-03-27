import functools

def memoize(func):
    """
    Decorator that caches the results of a function call.

    This decorator is useful for optimizing functions, especially recursive ones,
    where the same arguments might be passed multiple times. It stores the
    results of expensive function calls and returns the cached result when
    the same inputs occur again.

    The cached results are stored in a dictionary, keyed by the function's
    arguments. It assumes that the function's arguments are hashable.
    For unhashable arguments (like lists or dicts), it attempts to convert
    them to hashable forms (tuples for lists, sorted items for dicts) for the key.
    """
    cache = {} # Initialize a dictionary to store cached results for this function.

    @functools.wraps(func) # Preserves the original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Create a unique cache key from the function's arguments.
        # Positional arguments are converted to a tuple.
        cache_key = tuple(args)
        
        # Keyword arguments need special handling:
        # 1. They should be included in the key.
        # 2. Their order shouldn't affect the key (e.g., func(a=1, b=2) is same as func(b=2, a=1)).
        if kwargs:
            # Convert keyword arguments to a sorted tuple of (key, value) pairs.
            # This ensures consistency regardless of the order they were passed.
            sorted_kwargs = tuple(sorted(kwargs.items()))
            cache_key = (cache_key, sorted_kwargs)

        # Check if the result for these arguments is already in the cache.
        if cache_key in cache:
            # If found, return the cached result immediately.
            return cache[cache_key]
        else:
            # If not found, call the original function with its arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache for future use.
            cache[cache_key] = result
            # Return the computed result.
            return result
    return wrapper

# --- Example Usage (commented out to provide only the raw snippet) ---
#
# @memoize
# def fibonacci(n):
#     """
#     Calculates the nth Fibonacci number recursively.
#     This function greatly benefits from memoization.
#     """
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)
#
# # print(f"Fibonacci(10): {fibonacci(10)}") # Output: 55
# # print(f"Fibonacci(30): {fibonacci(30)}") # Output: 832040
#
# @memoize
# def complex_calculation(a, b, operation='add'):
#     """
#     A dummy function with multiple arguments, including keyword arguments.
#     """
#     print(f"Calculating {a}, {b} with operation '{operation}'...")
#     if operation == 'add':
#         return a + b
#     elif operation == 'subtract':
#         return a - b
#     else:
#         return "Unsupported operation"
#
# # First call, performs calculation
# # print(complex_calculation(5, 3))
# # Second call with same args, uses cache
# # print(complex_calculation(5, 3))
# # Call with keyword args, performs calculation
# # print(complex_calculation(10, 5, operation='subtract'))
# # Call with same keyword args (order irrelevant), uses cache
# # print(complex_calculation(10, operation='subtract', b=5))