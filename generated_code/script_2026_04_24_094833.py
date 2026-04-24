import functools

def memoize(func):
    """
    A simple memoization decorator for functions.
    It caches the results of function calls based on their arguments.
    This can significantly speed up functions that are called multiple times
    with the same arguments, especially recursive functions.

    Args:
        func (callable): The function to be memoized.

    Returns:
        callable: The decorated (memoized) function.
    """
    cache = {}  # Dictionary to store cached results

    @functools.wraps(func)  # Preserves the original function's metadata (name, docstring, etc.)
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on function arguments.
        # It's important that the arguments are hashable.
        # 'args' is already a tuple, which is hashable if its elements are.
        # For 'kwargs', convert them to a frozenset of (key, value) pairs.
        # frozenset is hashable and ignores insertion order, ensuring
        # {'a':1, 'b':2} produces the same key as {'b':2, 'a':1}.
        key = (args, frozenset(kwargs.items()))

        if key not in cache:
            # If the result for this specific set of arguments is not in cache,
            # call the original function and store its result.
            cache[key] = func(*args, **kwargs)
        return cache[key] # Return the cached result

    return wrapper