import time

def time_function(func):
    """
    A decorator that measures the execution time of a function.

    This decorator can be applied to any function to automatically log
    how long that function takes to execute. It's useful for profiling
    and understanding performance bottlenecks.

    Usage:
    @time_function
    def my_slow_function():
        # ... function code ...

    How it works:
    1. `time_function` takes the original function (`func`) as an argument.
    2. It returns a new function called `wrapper`. This `wrapper` function
       is what actually replaces the original function when the decorator is used.
    3. When `wrapper` is called, it first records the current time (`start_time`).
    4. Then, it calls the original function (`func`) with all the arguments
       (`*args`, `**kwargs`) that were passed to `wrapper`.
    5. After `func` completes, `wrapper` records the end time (`end_time`).
    6. It calculates the difference (`duration`) and prints a formatted message
       showing the function's name and its execution time.
    7. Finally, it returns the result obtained from the original function call.
    """
    def wrapper(*args, **kwargs):
        # Record the start time using time.perf_counter() for high-resolution timing
        start_time = time.perf_counter()

        # Call the original function with its arguments and keyword arguments
        result = func(*args, **kwargs)

        # Record the end time after the function has completed
        end_time = time.perf_counter()

        # Calculate the duration of the function's execution
        duration = end_time - start_time

        # Print the execution time to the console
        print(f"Function '{func.__name__}' executed in {duration:.4f} seconds.")

        # Return the result of the original function
        return result
    return wrapper

# --- Example Usage ---

@time_function
def simulate_work(seconds):
    """
    A dummy function that simulates a task taking a certain number of seconds.
    """
    print(f"Starting simulated work for {seconds} seconds...")
    time.sleep(seconds) # Pause execution for 'seconds'
    print(f"Finished simulated work for {seconds} seconds.")
    return f"Work completed after {seconds}s"

@time_function
def calculate_fibonacci(n):
    """
    Calculates the nth Fibonacci number recursively. (Inefficient for large n)
    """
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

if __name__ == '__main__':
    print("--- Testing simulate_work ---")
    work_result = simulate_work(1.5) # This call will be timed by the decorator
    print(f"Result: {work_result}\n")

    print("--- Testing calculate_fibonacci ---")
    fib_result = calculate_fibonacci(30) # This call will also be timed
    print(f"Fibonacci(30) = {fib_result}")
<ctrl63>