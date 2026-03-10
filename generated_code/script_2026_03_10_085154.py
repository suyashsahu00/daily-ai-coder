import time
from functools import wraps

def timer(func):
    """
    A decorator that measures and prints the execution time of a function.

    Decorators are functions that take another function as an argument,
    extend its behavior without explicitly modifying it, and return the new function.
    This 'timer' decorator can be applied to any function to automatically log its execution time.

    Usage example:
    @timer
    def my_slow_function(duration):
        # Simulate a time-consuming operation
        time.sleep(duration)
        return f"Slept for {duration} seconds"

    result = my_slow_function(0.5)
    # Expected output in console:
    # 'my_slow_function' executed in 0.50XXs
    # And 'result' will contain "Slept for 0.5 seconds"
    """
    @wraps(func)
    # @wraps(func) is crucial here. It copies the original function's
    # metadata (like __name__, __doc__, __module__, __annotations__)
    # from 'func' to the 'wrapper' function. Without it, calling
    # my_slow_function.__name__ would return 'wrapper' instead of 'my_slow_function'.
    def wrapper(*args, **kwargs):
        # *args and **kwargs allow the 'wrapper' to accept any number
        # of positional and keyword arguments that the original function 'func' takes.
        # This makes the decorator generic and reusable for any function signature.

        start_time = time.perf_counter()
        # time.perf_counter() provides a high-resolution timer
        # suitable for measuring short durations. It's often preferred over
        # time.time() for benchmarking because it's not affected by system
        # clock changes (like daylight saving or manual adjustments).

        result = func(*args, **kwargs)
        # This line is where the original function 'func' is actually executed
        # with all its original arguments.

        end_time = time.perf_counter()
        # Record the time immediately after the original function has completed its execution.

        execution_time = end_time - start_time
        # Calculate the total time taken for the function's execution.

        print(f"'{func.__name__}' executed in {execution_time:.4f}s")
        # Print a formatted message showing the name of the executed function
        # and its duration, formatted to four decimal places for precision.

        return result
        # The 'wrapper' must return the result of the original function 'func'.
        # This ensures that decorated functions still produce and return their
        # expected output values to the caller.
    return wrapper
    # The decorator returns the 'wrapper' function. When '@timer' is used,
    # the original function name (e.g., 'my_slow_function') actually points
    # to this 'wrapper' function, which now encapsulates the original 'func'.