def get_nested_value(d: dict, keys: list, default=None):
    """
    Safely retrieves a value from a nested dictionary structure using a list of keys.

    This function prevents KeyError or TypeError exceptions that would normally occur
    when trying to access non-existent keys or non-dictionary intermediate values.

    Args:
        d (dict): The dictionary to search within.
        keys (list): A list of strings representing the path to the desired value.
                     For example, ["user", "profile", "name"] to get d["user"]["profile"]["name"].
        default: The value to return if any key in the path is not found
                 or if an intermediate value is not a dictionary.
                 Defaults to None.

    Returns:
        The value found at the specified path, or the 'default' value if the path
        does not exist or is invalid.
    """
    current_value = d
    # Iterate through each key in the provided path
    for key in keys:
        # Check if the current_value is a dictionary AND if it contains the current key
        if isinstance(current_value, dict) and key in current_value:
            # If both conditions are true, update current_value to the value associated with the key
            current_value = current_value[key]
        else:
            # If current_value is not a dict, or the key doesn't exist in it,
            # the path is broken. Return the default value.
            return default
    # If the loop completes, it means the entire path was successfully traversed,
    # and current_value holds the desired nested value.
    return current_value