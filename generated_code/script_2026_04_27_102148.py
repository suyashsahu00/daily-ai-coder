import functools

def memoize(func):
    """
    A simple memoization decorator for functions with hashable arguments.

    Memoization is an optimization technique where the results of expensive
    function calls are stored (cached) and returned directly when the same
    inputs occur again, avoiding redundant computations.

    This decorator creates a cache for each decorated function. It assumes
    that all arguments (positional and keyword) to the decorated function
    are hashable, as they will be used as keys in a dictionary.

    Args:
        func (callable): The function to be memoized. Its arguments must be hashable.

    Returns:
        callable: A wrapper function that caches the results of `func`.
    """
    cache = {} # This dictionary stores the cached results.
               # Keys are tuples representing the function arguments, values are the computed results.

    @functools.wraps(func) # This decorator from functools preserves the original
                           # function's name, docstring, and other metadata.
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on the function's arguments.
        # Positional arguments are straightforwardly used as a tuple.
        # Keyword arguments are converted to a frozenset of (key, value) pairs
        # to ensure the key is hashable and independent of keyword argument order.
        if kwargs:
            # If keyword arguments are present, combine positional and sorted keyword args for the key.
            # frozenset is used because it's hashable, unlike a regular set, and ignores order.
            key = (args, frozenset(kwargs.items()))
        else:
            # If no keyword arguments, the tuple of positional arguments serves as the key.
            key = args

        # Check if the result for the current arguments is already in the cache.
        if key in cache:
            return cache[key] # If cached, return the stored result immediately.
        else:
            # If not cached, call the original function to compute the result.
            result = func(*args, **kwargs)
            # Store the newly computed result in the cache before returning it.
            cache[key] = result
            return result

    return wrapper # Return the wrapper function, which now has memoization capabilities.