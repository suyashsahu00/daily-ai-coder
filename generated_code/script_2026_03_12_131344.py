def memoized_fibonacci(n, _cache=None):
    """
    Calculates the nth Fibonacci number using memoization to optimize performance.
    
    The Fibonacci sequence is defined as: F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1.
    A naive recursive implementation of Fibonacci is highly inefficient due to redundant calculations
    of the same subproblems (e.g., F(3) is calculated multiple times when computing F(5)).
    
    Memoization (a form of dynamic programming) stores the results of expensive function calls
    and returns the cached result when the same inputs occur again, avoiding re-computation.
    
    Args:
        n (int): The index of the Fibonacci number to compute (must be non-negative).
        _cache (dict, optional): A dictionary used internally to store previously computed
                                 Fibonacci numbers. This allows recursive calls to share
                                 the same cache instance. It should typically not be
                                 provided by the initial caller.
                                 
    Returns:
        int: The nth Fibonacci number.
        
    Raises:
        ValueError: If n is a negative integer.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Initialize the cache if it's the first call to the function (or a new independent call).
    # This ensures that each top-level call starts with an empty cache.
    if _cache is None:
        _cache = {}

    # Check if the result for the current 'n' is already in the cache.
    # If found, return the cached value directly, avoiding re-computation.
    if n in _cache:
        return _cache[n]

    # Handle the base cases of the Fibonacci sequence.
    if n == 0:
        result = 0
    elif n == 1:
        result = 1
    else:
        # Recursive step: F(n) = F(n-1) + F(n-2).
        # The recursive calls pass the same `_cache` dictionary, ensuring
        # all intermediate results are stored and retrieved from the shared cache.
        result = memoized_fibonacci(n - 1, _cache) + memoized_fibonacci(n - 2, _cache)
    
    # Store the newly computed result in the cache before returning it.
    _cache[n] = result
    return result