import itertools

def chunk_iterable(iterable, chunk_size):
    """
    Yields successive chunks from an iterable.

    This generator function takes any iterable (like a list, tuple, or even another generator)
    and breaks it down into smaller lists (chunks) of a specified size.
    It's particularly useful when processing large datasets, making API calls in batches,
    or when you need to process data in manageable segments.

    Args:
        iterable (iterable): The input iterable to be chunked.
        chunk_size (int): The desired size of each chunk. Must be a positive integer.

    Yields:
        list: A list representing a chunk of the original iterable.
              The last chunk might be smaller than `chunk_size` if the total
              number of items is not perfectly divisible by `chunk_size`.

    Raises:
        ValueError: If chunk_size is not a positive integer.

    Example:
        >>> data = range(10)
        >>> list(chunk_iterable(data, 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        >>> data = ['a', 'b', 'c', 'd', 'e']
        >>> list(chunk_iterable(data, 2))
        [['a', 'b'], ['c', 'd'], ['e']]

        >>> list(chunk_iterable([], 5))
        []
    """
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    # Obtain an iterator from the input iterable.
    # This is crucial because it ensures that the iterable is consumed sequentially
    # and only once, regardless of its original type (list, generator, etc.).
    it = iter(iterable) 

    while True:
        # Use itertools.islice to take 'chunk_size' elements from the iterator 'it'.
        # `islice` returns an iterator that yields up to 'chunk_size' items.
        # We convert this slice iterator into a list to form our chunk.
        chunk = list(itertools.islice(it, chunk_size))

        # If the `chunk` list is empty after attempting to get items,
        # it means the original iterable `it` has been fully exhausted.
        # In this case, we break out of the loop as there are no more items to process.
        if not chunk:
            break
        
        # If the chunk is not empty, it contains items from the iterable.
        # We yield this chunk, making `chunk_iterable` a generator.
        yield chunk