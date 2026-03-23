import threading
import time

def debounce(wait_time):
    """
    Decorator that will postpone a function's execution until after `wait_time`
    seconds have elapsed since the last time it was invoked. This is useful
    for limiting the rate at which a function is called, e.g., for event
    handlers that fire rapidly (like window resizing, scroll events, or
    typing in a search box).

    Args:
        wait_time (float): The number of seconds to wait after the last call
                           before executing the function.

    Returns:
        Callable: A decorated function that is debounced.
    """
    def decorator(func):
        timer = None
        last_args = None
        last_kwargs = None
        result = [None] # Use a list to store the result across calls (mutable)

        def debounced(*args, **kwargs):
            nonlocal timer, last_args, last_kwargs, result

            last_args = args
            last_kwargs = kwargs

            def call_func():
                """Internal function to actually execute the decorated function."""
                result[0] = func(*last_args, **last_kwargs)

            if timer is not None:
                timer.cancel() # Cancel the previous scheduled call if one exists

            # Schedule a new call after wait_time
            timer = threading.Timer(wait_time, call_func)
            timer.start()

            # Note: For functions that return a value, a debounced function
            # typically doesn't return the *actual* result immediately because
            # it's executed in the future. If you need the result, you might
            # need a callback mechanism or future-like object.
            # This implementation will return the result of the *last*
            # successfully debounced call *if* it has completed, but primarily
            # it's designed for side-effect functions.
            return result[0] # Returns the last known result or None initially

        return debounced
    return decorator

# --- Example Usage ---

if __name__ == "__main__":
    # Create a simple function to debounce
    def search_input(query):
        print(f"Searching for: '{query}'...")
        # Simulate some work
        time.sleep(0.1)
        return f"Results for '{query}'"

    # Apply the debounce decorator with a 0.5-second wait time
    debounced_search = debounce(0.5)(search_input)

    print("--- Simulating rapid typing ---")
    debounced_search("a")
    time.sleep(0.1) # Simulate quick keypress
    debounced_search("ap")
    time.sleep(0.1)
    debounced_search("app")
    time.sleep(0.1)
    debounced_search("appl")
    time.sleep(0.1)
    debounced_search("apple") # This will be the one that eventually executes

    print("\n(Waiting for debounced function to trigger...)\n")
    time.sleep(1.0) # Wait long enough for the debounce to trigger

    print("\n--- Simulating a pause, then more typing ---")
    debounced_search("banana")
    time.sleep(0.2)
    debounced_search("bananas")
    time.sleep(0.8) # This pause is long enough for "bananas" to execute

    print("\n(Waiting for the last debounced function to trigger...)\n")
    time.sleep(1.0) # Ensure the very last one has time to execute

    # Example with return value (will return the result of the *last* successful call)
    print("\n--- Example with return value ---")
    @debounce(0.3)
    def calculate_sum(a, b):
        print(f"Calculating sum of {a} + {b}")
        time.sleep(0.05)
        return a + b

    res1 = calculate_sum(1, 2)
    time.sleep(0.1)
    res2 = calculate_sum(3, 4) # This will cancel the (1,2) calculation
    time.sleep(0.1)
    res3 = calculate_sum(5, 6) # This will cancel the (3,4) calculation

    print(f"Initial return from calls (usually None or old result): {res1}, {res2}, {res3}")
    time.sleep(0.5) # Wait for the last call (5,6) to execute
    # To get the actual result, you'd need to re-call or use a future/callback.
    # For demonstration, let's call it again, this time waiting for result if needed
    final_res = calculate_sum(7, 8)
    time.sleep(0.4) # Wait for it to complete
    print(f"Result after last debounce for (7,8) (might be the old value, or none): {final_res}")
    # This demonstrates the common pattern where debounced functions are primarily for side-effects,
    # and their return values are typically not captured immediately.
    # To get the 'real' final value, you would need to store it in a shared variable or pass a callback.
    # The current `result[0]` only captures the last value when `call_func` completes.
    print("Example finished.")