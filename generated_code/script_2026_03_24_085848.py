def deep_merge_dicts(d1, d2):
    """
    Recursively merges dictionary d2 into dictionary d1.

    If a key exists in both dictionaries:
    - If both values are dictionaries, they are merged recursively.
    - Otherwise (e.g., lists, strings, numbers), the value from d2
      overwrites the value in d1.

    This function creates a new dictionary and does not modify the
    original dictionaries d1 and d2.

    Parameters:
        d1 (dict): The base dictionary to merge into.
        d2 (dict): The dictionary to merge from.

    Returns:
        dict: A new dictionary containing the merged result.
    """
    # Create a copy of d1 to avoid modifying the original dictionary directly.
    merged_dict = d1.copy()

    for key, value in d2.items():
        if key in merged_dict and \
           isinstance(merged_dict[key], dict) and \
           isinstance(value, dict):
            # If the key exists in both dictionaries and both values are
            # dictionaries, recursively merge them.
            merged_dict[key] = deep_merge_dicts(merged_dict[key], value)
        else:
            # In all other cases (key exists but values are not both dicts,
            # or key doesn't exist in d1), d2's value for the key
            # overwrites d1's value or adds the new key/value pair.
            merged_dict[key] = value

    return merged_dict