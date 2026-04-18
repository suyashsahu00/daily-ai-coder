import functools

def memoize(func):
    """
    A simple memoization decorator to cache results of expensive function calls.

    This decorator works by storing the results of function calls in a dictionary
    (the 'cache'). When the function is called with a specific set of inputs,
    it first checks if those inputs have been seen before and if their result
    is already in the cache.

    - If the result is found, it returns the cached value directly,
      avoiding re-executing the original function.
    - If the result is not found, it calls the original function to compute it,
      stores this new result in the cache, and then returns it.

    This is most effective for "pure functions" – functions that always return
    the same output for the same input and have no side effects.
    Function arguments must be hashable (e.g., numbers, strings, tuples; not lists or dictionaries directly)
    because they are used as keys in the internal cache dictionary.
    """
    cache = {} # Initialize an empty dictionary to store cached results

    @functools.wraps(func) # Preserves the original function's metadata (like name, docstring)
    def wrapper(*args, **kwargs):
        # Create a unique, hashable key from the function's arguments.
        # Positional arguments are stored as a tuple.
        key_args = tuple(args)
        
        # Keyword arguments are converted to a sorted tuple of (key, value) pairs.
        # Sorting ensures that the key is consistent regardless of the order
        # in which keyword arguments were passed.
        key_kwargs = tuple(sorted(kwargs.items()))
        
        # Combine both sets of arguments into a single, comprehensive cache key.
        cache_key = (key_args, key_kwargs)

        if cache_key in cache:
            # If the result for this specific set of arguments is already in the cache,
            # return the cached value directly without re-executing the function.
            return cache[cache_key]
        else:
            # If the result is not in the cache, call the original function
            # to compute the result using the provided arguments.
            result = func(*args, **kwargs)
            
            # Store the newly computed result in the cache for future use,
            # associated with the unique cache key.
            cache[cache_key] = result
            
            # Return the computed result.
            return result
            
    return wrapper