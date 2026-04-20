import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    This decorator caches the results of a function call based on its arguments.
    If the function is called again with the same arguments, the cached result
    is returned instead of re-executing the function. This is particularly
    useful for optimizing pure functions with expensive computations,
    especially recursive functions.

    The arguments to the decorated function must be hashable.
    """
    cache = {}  # This dictionary will store the cached results (argument tuple -> result)

    @functools.wraps(func) # Preserves the original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Create a hashable key from both positional and keyword arguments.
        # Positional arguments `args` are already a tuple.
        # Keyword arguments `kwargs` are a dict, so convert to frozenset of items to make it hashable.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for this specific set of arguments is already in the cache,
            # return the cached value directly.
            return cache[key]
        else:
            # If the result is not in the cache, call the original function
            # with the provided arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it,
            # so future calls with the same arguments can use the cached value.
            cache[key] = result
            return result
    return wrapper