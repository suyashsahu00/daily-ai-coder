import functools

def memoize(func):
    """
    A simple memoization decorator for functions.

    It caches the results of function calls and returns the cached result
    if the same arguments are passed again. This can significantly speed up
    functions that are called repeatedly with the same arguments, especially
    recursive functions with overlapping subproblems (e.g., Fibonacci sequence).

    How it works:
    1. A `cache` dictionary is created when the decorator is applied to a function.
    2. When the decorated function is called, a unique `key` is generated from
       its positional (`args`) and keyword (`kwargs`) arguments.
       - Positional arguments are converted to a tuple.
       - Keyword arguments are sorted by key and converted to a frozenset of
         (key, value) pairs to ensure the key is consistent regardless of
         the order keyword arguments are passed.
    3. It checks if this `key` already exists in the `cache`.
    4. If the key is in the cache, the stored result is returned immediately,
       avoiding the re-execution of the original function.
    5. If the key is not in the cache, the original function (`func`) is called
       with the provided arguments.
    6. The result of `func` is then stored in the `cache` with the generated `key`.
    7. Finally, the result is returned.

    Limitations:
    - All arguments (positional and keyword) to the decorated function must be hashable.
      This means arguments like lists, dictionaries, or custom objects without a
      `__hash__` method cannot be directly used as arguments.
    - The cache grows indefinitely; there are no built-in mechanisms for cache
      invalidation, size limits (like LRU), or expiration. For more advanced
      caching, consider `functools.lru_cache`.
    - Does not handle methods of objects if `self` is not hashable (though `self`
      is usually hashable by default).

    Usage:
    @memoize
    def my_function(arg1, arg2, kwarg1=default):
        # ... function logic ...
        return result
    """
    cache = {}  # Dictionary to store cached results

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique key for the cache based on arguments.
        # Positional arguments are converted to a tuple.
        # Keyword arguments are sorted by key and converted to a frozenset of items
        # to ensure the key is consistent regardless of kwarg order and is hashable.
        key = (tuple(args), frozenset(kwargs.items()))

        if key in cache:
            # If the result for these arguments is already in the cache, return it.
            return cache[key]
        else:
            # If not in cache, call the original function.
            result = func(*args, **kwargs)
            # Store the result in the cache for future use.
            cache[key] = result
            return result
    return wrapper