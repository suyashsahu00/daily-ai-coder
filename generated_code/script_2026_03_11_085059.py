import time
from functools import wraps

def timer(func):
    """
    A decorator that measures the execution time of a function.

    This decorator wraps a function, records the time before and after its
    execution, and then prints the elapsed time. It's useful for profiling
    and understanding performance bottlenecks.

    Usage:
        @timer
        def my_function(arg1, arg2):
            # ... perform some operations ...
            return result

        # When my_function is called, its execution time will be printed
        # to the console.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Record the start time using a high-resolution performance counter.
        start_time = time.perf_counter()

        # Execute the original function with its arguments.
        result = func(*args, **kwargs)

        # Record the end time.
        end_time = time.perf_counter()

        # Calculate the elapsed time.
        execution_time = end_time - start_time

        # Print the function name and its execution time, formatted to 4 decimal places.
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds.")

        # Return the result of the original function so that its behavior
        # is otherwise unchanged.
        return result
    return wrapper