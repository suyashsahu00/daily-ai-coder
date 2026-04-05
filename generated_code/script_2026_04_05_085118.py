import functools

def memoize(func):
    """
    A simple decorator to memoize (cache) the results of a function.
    This can significantly speed up functions that are called repeatedly
    with the same arguments, especially recursive functions like Fibonacci
    or functions with expensive computations.

    How it works:
    1.  A `cache` dictionary is created when the decorator is applied to
        store the results of function calls. This cache is unique to each
        decorated function.
    2.  When the decorated function is called, a unique `key` is generated
        from its positional (`args`) and keyword (`kwargs`) arguments.
        -   Positional arguments are directly used in the key.
        -   Keyword arguments are sorted by key to ensure a consistent
            representation regardless of their call order, making them hashable
            and comparable.
    3.  Before executing the original function, the `wrapper` checks if this
        `key` already exists in the `cache`.
    4.  If the `key` is found, it means the function was called with these
        exact arguments before, and its result is already stored. The cached
        result is returned immediately.
    5.  If the `key` is not found, the original `func` is executed with the
        given arguments. Its computed `result` is then stored in the `cache`
        under the generated `key` before being returned.

    Note:
    -   This memoization works best for functions with hashable arguments
        (e.g., numbers, strings, tuples, frozen sets). It will fail if
        arguments are unhashable types like lists or dictionaries directly,
        unless they are explicitly converted or handled within the function.
    -   For a more feature-rich caching solution (e.g., with size limits
        and eviction policies like LRU - Least Recently Used), Python's
        standard library `functools.lru_cache` is often a better choice.
        This snippet provides a basic, easy-to-understand implementation.
    """
    cache = {}

    @functools.wraps(func) # Preserves the original function's metadata (name, docstring, etc.)
    def wrapper(*args, **kwargs):
        # Create a hashable key from both positional and keyword arguments.
        # Keyword arguments are sorted by key to ensure consistent hash generation
        # regardless of the order they were passed in.
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            return cache[key]
        else:
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    return wrapper