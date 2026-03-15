import functools
import threading
import time # Included for conceptual understanding of timing, though not directly used in the final debouncing logic.

def debounce(delay_seconds):
    """
    A decorator that debounces a function.

    Debouncing ensures that a function is not called too frequently.
    It postpones the function's execution until `delay_seconds` have passed
    since the last time it was invoked. If the function is called again
    within this `delay_seconds` window, the previous pending execution
    is cancelled and a new one is scheduled.

    This is extremely useful for events that can fire rapidly, such as:
    - User typing in a search input (only search after typing stops for a moment).
    - Window resizing events (only update layout after resizing stops).
    - Auto-saving mechanisms, where changes might come in bursts.

    Args:
        delay_seconds (float): The number of seconds to wait after the last call
                               before executing the decorated function.

    Returns:
        Callable: A decorator that can be applied to a function.

    Example Usage:
        @debounce(0.5) # Wait 0.5 seconds after the last call
        def search(query):
            print(f"Searching for: {query}")

        print("Simulating rapid typing:")
        search("a")   # Schedules search("a") for 0.5s later
        time.sleep(0.1)
        search("ab")  # Cancels previous, schedules search("ab") for 0.5s later
        time.sleep(0.1)
        search("abc") # Cancels previous, schedules search("abc") for 0.5s later
        time.sleep(0.6) # Now, 0.6s have passed since the last call to search.
                        # The timer for search("abc") will expire, printing the result.
        # Expected output after 0.6s:
        # Searching for: abc

        print("\nSimulating a single call:")
        search("single query") # Schedules search("single query") for 0.5s later
        time.sleep(0.6)
        # Expected output after 0.6s:
        # Searching for: single query
    """
    def decorator(func):
        # `_timer` is a list containing a single threading.Timer object.
        # This design pattern is used to allow the inner `debounced` function
        # to modify the timer from the outer scope (closure).
        # Python's scope rules for closures mean that if `timer` was just a
        # simple variable, assigning `timer = ...` within `debounced` would
        # create a new local variable, not modify the one from the outer scope.
        # Using a mutable object like a list (or a `nonlocal` keyword with Python 3)
        # allows shared state modification.
        _timer = [None]

        @functools.wraps(func)
        def debounced(*args, **kwargs):
            """
            The debounced version of the original function.
            When called, it manages the scheduling and cancellation of the
            actual function execution.
            """
            # Define the task that will eventually execute the original function.
            # This inner function (a closure) captures the `args` and `kwargs`
            # from the *latest* call to `debounced`. This ensures that when the
            # function finally runs, it uses the most recent input.
            def call_it():
                func(*args, **kwargs)

            # If there's an existing timer from a previous call to `debounced`,
            # it means the `delay_seconds` haven't passed yet for that call.
            # We cancel it to prevent that older execution from happening.
            if _timer[0] is not None:
                _timer[0].cancel()

            # Schedule a new timer to execute `call_it` after `delay_seconds`.
            # This new timer replaces any previously cancelled one, ensuring
            # that the function only executes after a pause of `delay_seconds`
            # following the *very last* invocation.
            _timer[0] = threading.Timer(delay_seconds, call_it)
            _timer[0].start()

        return debounced
    return decorator

# If this file is run directly, demonstrate the example usage.
if __name__ == "__main__":
    @debounce(0.5)
    def search(query):
        print(f"Searching for: {query}")

    print("--- Debounce Example ---")
    print("Simulating rapid typing:")
    search("a")
    time.sleep(0.1)
    search("ab")
    time.sleep(0.1)
    search("abc")
    time.sleep(0.6) # Wait for the last call to debounce and execute

    print("\nSimulating a single call:")
    search("single query")
    time.sleep(0.6) # Wait for the single call to debounce and execute

    print("\nSimulating calls that are far apart (each should execute):")
    search("first call")
    time.sleep(0.7) # Enough time for "first call" to execute
    search("second call")
    time.sleep(0.7) # Enough time for "second call" to execute