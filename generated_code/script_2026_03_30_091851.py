import functools

# A simple memoization decorator for functions with hashable arguments.
# This decorator enhances a function by caching its results based on its input
# arguments. If the function is called again with the same arguments, it
# returns the stored result instead of re-executing the function, which can
# significantly improve performance for expensive computations.
def memoize(func):
    """
    Decorator that caches a function's results for given arguments.

    The cache is stored in a dictionary where keys are created from the
    function's arguments and values are the corresponding return values.
    This works for functions where all positional and keyword arguments must
    be hashable (e.g., numbers, strings, tuples, frozensets).
    """
    cache = {}  # The dictionary to store cached results.

    @functools.wraps(func)  # Preserves the original function's metadata (name, docstring, etc.).
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function's arguments.
        # Positional arguments (`args`) are already a tuple, which is hashable.
        # Keyword arguments (`kwargs`) are a dictionary, which is not hashable.
        # We convert `kwargs` to a `frozenset` of `(key, value)` pairs to make
        # it hashable and ensure that the order of keyword arguments does not
        # affect the cache key.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for this specific set of arguments (key) is
            # already present in the cache, return the stored result immediately.
            return cache[key]
        else:
            # If the result is not in the cache, execute the original function,
            # store its computed result in the cache, and then return the result.
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    return wrapper