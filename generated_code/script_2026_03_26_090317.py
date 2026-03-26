import functools

def memoize(func):
    """
    A decorator that caches the results of a function's execution.

    This is particularly useful for optimizing functions that might be called
    multiple times with the same arguments, such as recursive algorithms
    (e.g., dynamic programming problems) or functions performing expensive I/O
    or computations.

    The cache stores results mapped to the function's arguments. Subsequent calls
    with identical arguments retrieve the result from the cache instead of
    re-executing the function.

    Args:
        func (callable): The function to be memoized.

    Returns:
        callable: A wrapped version of the input function with caching enabled.

    Raises:
        TypeError: If any of the function's arguments are unhashable
                   (e.g., lists, dictionaries, or other mutable objects used as arguments).
    """
    cache = {}  # Stores the cached results. Key: (args_tuple, kwargs_tuple), Value: function result.

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function's arguments.
        # Positional arguments are converted to a tuple.
        args_key = tuple(args)

        # Keyword arguments are sorted by key and then converted to a tuple of (key, value) pairs.
        # Sorting ensures that the order of keyword arguments does not affect the cache key
        # (e.g., func(a=1, b=2) and func(b=2, a=1) will have the same cache key).
        kwargs_key = tuple(sorted(kwargs.items()))

        # Combine both into a single, hashable cache key.
        cache_key = (args_key, kwargs_key)

        if cache_key in cache:
            # If the result for these arguments is already in the cache, return it directly.
            return cache[cache_key]
        else:
            # If not in cache, execute the original function.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it.
            cache[cache_key] = result
            return result
    return wrapper