import collections

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    This function modifies dict1 in-place.

    If a key exists in both dictionaries:
    - If both values are mappings (e.g., dictionaries), they are merged recursively.
    - Otherwise, the value from dict2 overwrites the value from dict1.
    If a key only exists in dict2, it's added to dict1.
    If a key only exists in dict1, it remains unchanged.

    Args:
        dict1 (dict): The target dictionary to merge into (will be modified).
        dict2 (dict): The source dictionary whose items will be merged into dict1.

    Returns:
        dict: The modified dict1, containing the merged result.
    """
    for key, value in dict2.items():
        # Check if the key exists in dict1 and both values are mappings.
        # collections.Mapping is used for broad compatibility with dict-like objects.
        if key in dict1 and isinstance(dict1[key], collections.Mapping) \
                         and isinstance(value, collections.Mapping):
            # If both values are mappings, recursively merge them.
            deep_merge_dicts(dict1[key], value)
        else:
            # Otherwise (key not in dict1, or one/both values are not mappings),
            # the value from dict2 overwrites or is added to dict1.
            dict1[key] = value
    return dict1