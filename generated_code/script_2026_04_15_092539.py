def deep_merge_dicts(d1, d2):
    """
    Recursively merges dictionary d2 into dictionary d1.

    This function modifies d1 in place by integrating all key-value pairs from d2.
    If a key exists in both dictionaries:
    - If both values are dictionaries, they are recursively merged.
    - Otherwise (e.g., one or both are not dicts), the value from d2 overwrites
      the value in d1.
    If a key only exists in d2, it is added to d1.

    Args:
        d1 (dict): The base dictionary to merge into. This dictionary will be modified.
        d2 (dict): The dictionary to merge from. Its contents will be merged into d1.

    Returns:
        dict: The modified d1 dictionary with contents of d2 merged in.

    Example:
        dict1 = {'a': 1, 'b': {'c': 2, 'd': 3}}
        dict2 = {'b': {'d': 4, 'e': 5}, 'f': 6}
        merged_dict = deep_merge_dicts(dict1, dict2)
        # merged_dict will be {'a': 1, 'b': {'c': 2, 'd': 4, 'e': 5}, 'f': 6}
    """
    # Iterate over each key-value pair in the second dictionary (d2)
    for key, value in d2.items():
        # Check if the current key from d2 also exists in d1
        # AND if both the value in d1 and the value in d2 for this key are dictionaries.
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            # If both are dictionaries, we need to recursively merge them.
            # This ensures nested dictionary structures are correctly combined.
            deep_merge_dicts(d1[key], value)
        else:
            # If the key doesn't exist in d1, or if the values are not both dictionaries
            # (meaning d2's value should simply overwrite d1's value or add a new key),
            # then update or add the key-value pair in d1 with d2's value.
            # This handles non-dict values and new keys.
            d1[key] = value
    return d1