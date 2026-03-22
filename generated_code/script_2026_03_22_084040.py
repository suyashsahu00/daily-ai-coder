import functools

def memoize(func):
    """
    A decorator that caches the results of a function call.

    This decorator is useful for optimizing functions that have expensive
    computations and are called multiple times with the same arguments.
    It stores the results of function calls in a dictionary, mapped to
    their arguments. When the function is called again with the same arguments,
    it returns the cached result instead of recomputing it.

    Limitations:
    - Works best for functions with hashable arguments (immutable types like
      numbers, strings, tuples). If arguments are unhashable (like lists,
      dictionaries, sets), it will raise a TypeError.
    - For simplicity, this version ignores keyword arguments for the cache key.
      It treats `func(1, 2)` and `func(1, y=2)` as different calls if `func`
      receives `kwargs`. A more robust memoization might include kwargs in the key
      (e.g., `key = (args, frozenset(kwargs.items()))`).
      `functools.lru_cache` (part of Python's standard library) offers
      a more comprehensive solution, handling kwargs and cache size limits.
    - Does not have a size limit; the cache grows indefinitely.

    Usage:
    @memoize
    def my_expensive_function(arg1, arg2):
        # ... perform expensive computation ...
        return result
    """
    cache = {}  # Initialize an empty dictionary to store cached results

    @functools.wraps(func)  # Preserves the original function's name, docstring, etc.
    def wrapper(*args, **kwargs):
        # Create a cache key from the function's positional arguments.
        # It's crucial that the key is hashable. Tuples are hashable,
        # so we convert `args` to a tuple.
        # This basic implementation does not include `kwargs` in the cache key.
        key = args

        if key not in cache:
            # If the result for these arguments is not in the cache,
            # call the original function and store its result.
            cache[key] = func(*args, **kwargs)
        
        # Return the cached result (either newly computed or previously stored).
        return cache[key]

    return wrapper