import functools

def memoize(func):
    """
    A simple memoization decorator that caches the results of a function call.
    This is useful for optimizing functions, especially recursive ones,
    where the same arguments might be passed multiple times.

    The cache stores results in a dictionary where keys are tuples of
    the function arguments and values are the computed results.
    It works for functions with hashable arguments.

    Example Usage:
    @memoize
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    # Calling fibonacci(100) will be significantly faster than an unmemoized version.
    # The first call will compute and cache, subsequent calls with the same 'n' will
    # retrieve from cache.
    # print(fibonacci(100))
    """
    cache = {} # Initialize a dictionary to store cached results

    @functools.wraps(func) # Preserves the original function's metadata (like name, docstring)
    def wrapper(*args, **kwargs):
        # Create a cache key from the arguments.
        # Positional arguments `args` are already a tuple, which is hashable.
        cache_key_args = args

        # Handle keyword arguments `kwargs`. Since dictionary order is not guaranteed
        # (before Python 3.7) and for consistency, we sort them by key
        # and convert them into a tuple of (key, value) pairs.
        cache_key_kwargs = tuple(sorted(kwargs.items())) if kwargs else ()

        # Combine both sets of arguments into a single, hashable key for the cache.
        full_cache_key = (cache_key_args, cache_key_kwargs)

        # Check if the result for these specific arguments is already in the cache.
        if full_cache_key in cache:
            return cache[full_cache_key] # If found, return the cached result immediately.

        # If not in cache, call the original function to compute the result.
        result = func(*args, **kwargs)

        # Store the computed result in the cache before returning it.
        cache[full_cache_key] = result
        return result
    return wrapper