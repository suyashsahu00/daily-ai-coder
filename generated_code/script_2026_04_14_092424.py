import copy

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1, handling nested dictionaries.
    Values from dict2 will overwrite values from dict1 if keys are identical.
    If both values are dictionaries, they will be merged recursively.

    Args:
        dict1 (dict): The base dictionary to merge into.
        dict2 (dict): The dictionary to merge from.

    Returns:
        dict: A new dictionary containing the deep merge of dict1 and dict2.
              Neither dict1 nor dict2 are modified.
    """
    # Create a deep copy of dict1 to ensure the original dictionary is not modified.
    merged = copy.deepcopy(dict1)

    # Iterate over each key-value pair in dict2.
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            # If the key exists in both dictionaries and both values are dictionaries,
            # recursively merge them.
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            # Otherwise, simply update or add the value from dict2 to the merged dictionary.
            # This handles cases where:
            # 1. The key is new to merged.
            # 2. The key exists, but values are not both dictionaries (e.g., one is a list, int, string, etc.).
            #    In this case, dict2's value overwrites dict1's value.
            merged[key] = value

    return merged

# Example Usage (optional, for demonstration purposes - would remove for final raw output if strictly "snippet" meant just the function)
# if __name__ == "__main__":
#     dict_a = {
#         "name": "Alice",
#         "details": {
#             "age": 30,
#             "city": "New York",
#             "interests": ["reading", "hiking"]
#         },
#         "preferences": {
#             "color": "blue",
#             "food": "pizza"
#         }
#     }
#
#     dict_b = {
#         "name": "Bob",  # Overwrites Alice
#         "details": {
#             "age": 31,  # Overwrites 30
#             "country": "USA", # New key
#             "interests": ["coding"] # Overwrites original list
#         },
#         "preferences": {
#             "food": "sushi", # Overwrites pizza
#             "drink": "coffee" # New key
#         },
#         "status": "active" # New top-level key
#     }
#
#     merged_dict = deep_merge_dicts(dict_a, dict_b)
#     print("Dictionary A:", dict_a)
#     print("Dictionary B:", dict_b)
#     print("Merged Dictionary:", merged_dict)
#
#     # Expected output:
#     # Merged Dictionary: {
#     #     'name': 'Bob',
#     #     'details': {
#     #         'age': 31,
#     #         'city': 'New York',
#     #         'interests': ['coding'],
#     #         'country': 'USA'
#     #     },
#     #     'preferences': {
#     #         'color': 'blue',
#     #         'food': 'sushi',
#     #         'drink': 'coffee'
#     #     },
#     #     'status': 'active'
#     # }