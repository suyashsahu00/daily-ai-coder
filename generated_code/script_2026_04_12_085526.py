import functools

def memoize(func):
    """
    A decorator that caches the results of a function call.

    It stores the function's output for specific input arguments,
    so that subsequent calls with the same arguments don't re-execute
    the function, but rather return the cached result. This is particularly
    useful for optimizing computationally expensive functions or recursive
    algorithms (like Fibonacci sequence calculations).
    """
    # The cache is a dictionary where keys are function arguments
    # and values are the corresponding return values.
    cache = {}

    @functools.wraps(func)  # Preserves the original function's metadata (name, docstring, etc.)
    def wrapper(*args, **kwargs):
        # Create a unique, hashable key from the function arguments.
        # Positional arguments (*args) are converted to a tuple.
        # Keyword arguments (**kwargs) are sorted by key to ensure
        # consistent ordering (e.g., f(a=1, b=2) has same key as f(b=2, a=1)),
        # then converted to a tuple of (key, value) pairs.
        key = (tuple(args), tuple(sorted(kwargs.items())))

        # Check if the result for these arguments is already in the cache.
        if key in cache:
            return cache[key]  # Return the cached result, avoiding re-computation.

        # If the result is not in the cache, execute the original function.
        result = func(*args, **kwargs)
        # Store the computed result in the cache for future calls with these arguments.
        cache[key] = result
        return result
    return wrapper