import functools

def memoize(func):
    """
    A simple memoization decorator that caches the results of a function
    call based on its arguments.

    This decorator is useful for optimizing functions that are called
    multiple times with the same arguments, especially recursive functions
    or computationally expensive ones. It prevents redundant computations
    by storing and retrieving previously computed results.

    Limitations:
    - All function arguments must be hashable (e.g., numbers, strings, tuples,
      frozensets). Lists, dictionaries, or custom objects that are not hashable
      cannot be directly used as arguments if they are intended to be part
      of the cache key, and will cause a TypeError.
    """
    cache = {} # Dictionary to store cached results. The keys will be tuples
               # representing the function arguments, and values will be the
               # computed results.

    @functools.wraps(func) # This decorator preserves the original function's
                           # metadata (like its name, docstring, and module),
                           # making the decorated function behave more like
                           # the original for introspection tools.
    def wrapper(*args, **kwargs):
        # Create a unique cache key from the function's arguments.
        # Positional arguments (*args) are already a tuple, which is hashable.
        # Keyword arguments (**kwargs) are a dictionary. To make them hashable
        # and ensure consistent keys regardless of keyword argument order,
        # we convert `kwargs.items()` to a frozenset. A frozenset is an
        # immutable (and thus hashable) version of a set.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for this specific set of arguments is already
            # in our cache, we return the cached value directly, avoiding
            # the execution of the original function.
            return cache[key]
        else:
            # If the result is not in the cache, we call the original function
            # with its arguments.
            result = func(*args, **kwargs)
            # After computing the result, we store it in the cache for future
            # calls with the same arguments.
            cache[key] = result
            # Finally, return the computed result.
            return result
    return wrapper