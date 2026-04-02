import collections

def deep_merge_dicts(target: dict, source: dict) -> dict:
    """
    Recursively merges dictionary `source` into dictionary `target`.

    This function iterates through key-value pairs in the `source` dictionary.
    - If a key exists in both `target` and `source`, and both corresponding
      values are dictionaries (or more generally, mappings), the function
      recursively calls itself to merge these sub-dictionaries.
    - If a key exists in both `target` and `source`, but the values are not
      both mappings (e.g., one is a dict and the other is an int, or both are
      non-dict types), the value from `source` overwrites the value in `target`.
    - If a key exists in `source` but not in `target`, the key-value pair
      is simply added to `target`.

    This function modifies the `target` dictionary in-place and returns it.

    Args:
        target: The dictionary to merge into (will be modified).
        source: The dictionary to merge from.

    Returns:
        The modified target dictionary, reflecting the merged content.
    """
    # Iterate over each key-value pair present in the source dictionary.
    for key, value in source.items():
        # Check if the current key also exists in the target dictionary.
        if key in target:
            # If the key exists in both and both corresponding values are mappings (like dicts),
            # we need to perform a deep (recursive) merge on these sub-dictionaries.
            # Using collections.abc.Mapping is robust for any dict-like object (e.g., dict, OrderedDict).
            if isinstance(target[key], collections.abc.Mapping) and \
               isinstance(value, collections.abc.Mapping):
                deep_merge_dicts(target[key], value)
            # If the key exists but the values are not both mappings (e.g., one is a dict
            # and the other is a list, or both are simple types like int/str),
            # the value from the source dictionary overwrites the value in the target dictionary.
            else:
                target[key] = value
        else:
            # If the key does not exist in the target dictionary, simply add the
            # key-value pair from the source dictionary to the target.
            target[key] = value
    return target