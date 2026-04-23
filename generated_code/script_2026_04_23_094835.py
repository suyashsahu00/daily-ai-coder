import functools

def memoize(func):
    """
    A simple memoization decorator that caches the results of a function.

    It stores the function's output for given input parameters in a dictionary.
    Subsequent calls with the exact same parameters will return the cached result
    instead of re-executing the function, saving computation time.

    This decorator is most effective for:
    1.  Pure functions: Functions that always return the same output for the
        same input and have no side effects (like modifying global state or I/O).
    2.  Functions with expensive computations: Where recalculating is costly.
    3.  Functions where arguments are hashable: The decorator uses arguments
        as keys in a dictionary, so they must be hashable (e.g., numbers, strings,
        tuples, frozensets, but not lists or dictionaries directly).

    Usage:
        @memoize
        def fibonacci(n):
            if n <= 1:
                return n
            return fibonacci(n-1) + fibonacci(n-2)

        # First call computes and caches:
        # print(fibonacci(10))

        # Subsequent calls with the same argument return cached result instantly:
        # print(fibonacci(10))
    """
    cache = {} # Dictionary to store results, mapping (args, kwargs) to return value

    @functools.wraps(func) # Preserves the original function's metadata (name, docstring)
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function arguments.
        # Positional arguments `args` are already a tuple, which is hashable.
        # Keyword arguments `kwargs` are a dict; convert them to a frozenset
        # of (key, value) pairs to make them hashable and order-independent.
        key = (args, frozenset(kwargs.items()))

        if key not in cache:
            # If the result for this set of arguments is not in cache,
            # call the original function and store its result.
            cache[key] = func(*args, **kwargs)
        
        # Return the cached result.
        return cache[key]

    return wrapper