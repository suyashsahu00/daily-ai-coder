import functools

def memoize(func):
    """
    A simple decorator to memoize (cache) the results of a function.

    This decorator stores the results of function calls and returns the cached
    result when the same inputs occur again, instead of re-executing the function.
    It is particularly useful for optimizing recursive functions or functions
    with high computational cost that are frequently called with the same arguments.

    The cache is stored in a dictionary, mapping argument tuples to results.
    It assumes that all function arguments are hashable.

    Args:
        func (callable): The function to be memoized.

    Returns:
        callable: A wrapper function that provides memoization for the original function.
    """
    cache = {}  # Dictionary to store cached results

    @functools.wraps(func)  # Preserves the original function's metadata (name, docstring, etc.)
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function arguments.
        # Positional arguments (*args) are converted to a tuple.
        # Keyword arguments (**kwargs) are sorted by key and converted to a frozenset
        # of (key, value) pairs. This ensures consistency regardless of argument order
        # (e.g., func(a=1, b=2) and func(b=2, a=1) generate the same key).
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for these arguments is already in the cache, return it directly.
            return cache[key]
        else:
            # If not in cache, call the original function with the given arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it.
            cache[key] = result
            return result
    return wrapper