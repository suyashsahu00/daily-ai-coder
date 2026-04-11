import time

class Timer:
    """
    A context manager for measuring the execution time of a block of code.

    Usage:
        import time

        with Timer("My Operation"):
            # Code to be timed
            time.sleep(1) # Simulate some work

    Output will be:
        My Operation took 1.0012 seconds.
    """
    def __init__(self, name=None):
        """
        Initializes the Timer context manager.
        :param name: An optional string identifier for the operation being timed.
                     If provided, it will be included in the output message.
        """
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        """
        Called when entering the 'with' statement block.
        Records the precise start time using time.perf_counter().
        time.perf_counter() is preferred for benchmarking as it returns
        the value of a high-resolution performance counter for timing
        short durations, with no relation to wall-clock time.
        """
        self.start_time = time.perf_counter()
        return self # Allows 'as timer_instance' if needed, though not strictly for this use case.

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' statement block (either normally or due to an exception).
        Records the end time, calculates the duration, and prints the result.

        :param exc_type: The type of exception that occurred (if any).
        :param exc_val: The exception instance that occurred (if any).
        :param exc_tb: A traceback object that occurred (if any).
        """
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

        if self.name:
            print(f"{self.name} took {self.duration:.4f} seconds.")
        else:
            print(f"Code block took {self.duration:.4f} seconds.")

        # Returning False (or implicitly None) propagates any exceptions
        # that occurred within the 'with' block. If True were returned,
        # any exceptions would be suppressed.
        return False
<ctrl63>