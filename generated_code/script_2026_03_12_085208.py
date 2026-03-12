import threading
import time

def debounce(delay_seconds):
    """
    Decorator that will postpone a function's execution until after `delay_seconds`
    have elapsed since the last time it was invoked. If the function is called
    again within this delay, the previous pending execution is cancelled, and
    a new delay period begins.

    This is useful for events that might fire very rapidly (e.g., typing into a search box,
    resizing a window, continuous sensor readings) where you only want to perform
    an action once the user has paused their activity, or once a stream of events
    has temporarily stopped.

    Example Usage (illustrative, not part of the returned code):
        @debounce(0.5)
        def search_items(query):
            print(f"Searching for: {query}")

        search_items("apple") # This call is debounced. A 0.5s timer starts.
        time.sleep(0.1)
        search_items("app")   # This call cancels the previous timer and starts a new 0.5s timer.
        time.sleep(0.1)
        search_items("appl")  # This call cancels the previous timer and starts another 0.5s timer.
        time.sleep(0.6)       # After 0.6 seconds (i.e., > 0.5s since last call), "Searching for: appl" will be printed.
                              # The calls for "apple" and "app" were never executed.
    """
    def decorator(func):
        # `timer` will hold the threading.Timer object for the delayed execution.
        # It's initialized to None, meaning no pending execution.
        timer = None
        # A lock is used to ensure thread-safe access to the 'timer' variable.
        # This is crucial if the debounced function can be called from multiple threads
        # simultaneously, preventing race conditions when cancelling or starting timers.
        lock = threading.Lock()

        def wrapper(*args, **kwargs):
            # The 'nonlocal' keyword allows us to modify the 'timer' variable
            # from the enclosing 'decorator' function's scope, rather than creating
            # a new local variable within 'wrapper' or modifying a global one.
            nonlocal timer

            # Acquire the lock to safely manipulate the `timer` variable.
            with lock:
                # If there's an existing timer from a previous call that hasn't fired yet, cancel it.
                # This is the core logic of debouncing: a new call resets the delay.
                if timer is not None:
                    timer.cancel()

                # Define the actual action that will be performed after the delay.
                # This nested function encapsulates the call to the original function `func`.
                def call_func():
                    # It's good practice to re-acquire the lock before executing the debounced function
                    # and updating `timer` to None. This prevents race conditions if a new call
                    # comes in just as this timer is about to execute, or if `func` itself
                    # takes a long time and `timer` needs to be consistently managed.
                    with lock:
                        # Call the original decorated function with its arguments.
                        func(*args, **kwargs)
                        # After the function has executed, reset the timer to None.
                        # This indicates that there is no longer a pending execution.
                        nonlocal timer
                        timer = None

                # Create a new `threading.Timer` object. It will call `call_func`
                # after `delay_seconds`. Timers run in separate threads.
                timer = threading.Timer(delay_seconds, call_func)
                # Start the timer.
                timer.start()
        return wrapper
    return decorator