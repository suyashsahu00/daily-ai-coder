import functools

def memoize(func):
    """
    A decorator that caches the results of a function call.

    This decorator stores the return value of a function for specific arguments.
    If the function is called again with the same arguments, the cached result
    is returned instead of re-executing the function. This is useful for
    optimizing functions that are called frequently with the same inputs,
    especially recursive functions like Fibonacci.

    The cache key is formed by combining the positional and keyword arguments
    into a hashable tuple. This means that all arguments passed to the
    decorated function must be hashable (e.g., numbers, strings, tuples,
    frozensets, but not lists or dictionaries directly unless converted).

    Example Usage:
        @memoize
        def fibonacci(n):
            # A classic example where memoization drastically improves performance.
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)

        # The first call for fibonacci(10) will compute and cache intermediate results.
        # print(fibonacci(10)) # Output: 55

        # Subsequent calls with the same argument will return the cached result instantly.
        # print(fibonacci(10)) # Returns 55 from cache without re-computation.

        @memoize
        def expensive_operation(a, b=0):
            # Simulates a time-consuming computation.
            import time
            time.sleep(0.1) # Simulate work
            return a + b

        # print(expensive_operation(1, b=2)) # Takes ~0.1s
        # print(expensive_operation(1, b=2)) # Instant, result from cache
    """
    cache = {} # Dictionary to store cached results, maps (args_tuple, kwargs_frozenset) -> result

    @functools.wraps(func) # Preserves metadata of the original function (e.g., name, docstring)
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function arguments.
        # Positional arguments (*args) are already a tuple.
        # Keyword arguments (**kwargs) are a dictionary. Since dictionary order
        # is not guaranteed (in older Python versions) and dictionaries are
        # not hashable, we convert them to a frozenset of (key, value) pairs.
        # frozenset ensures hashability and treats `{'a':1, 'b':2}` the same
        # as `{'b':2, 'a':1}`.
        key = (args, frozenset(kwargs.items()))

        if key in cache:
            # If the result for these specific arguments is already in the cache,
            # return the cached value directly, avoiding re-execution of 'func'.
            return cache[key]
        else:
            # If the result is not in the cache, call the original function
            # to compute it with the given arguments.
            result = func(*args, **kwargs)
            # Store the computed result in the cache before returning it.
            # This makes it available for any future calls with the same 'key'.
            cache[key] = result
            return result
    return wrapper