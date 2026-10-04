def heapify(arr, n, i):
    """ Restores max-heap property for the subtree with index i as the root."""
    large = i                               # Initialize largest as root    
    left = 2*i + 1                             # Left child index
    right = 2*i + 2                            # Right child index

    if left < n and arr[left] > arr[large]:
        large = left                           # Update largest if left child is larger

    if right < n and arr[right] > arr[large]:
        large = right                          # Update largest if right child is larger

    if large != i:
        arr[i], arr[large] = arr[large], arr[i]  # Swap root with largest element
        heapify(arr, n, large)                      # Recursively heapify the subtree


def heap_sort(arr):
    """ Sorts an array in ascending order using the heap sort algorithm.
    Operates in place and has a time complexity of O(n log n)."""
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):         # Start from the last non-leaf node (n // 2 - 1) and heapify each node
        heapify(arr, n, i)                      # Build a max heap

    for i in range(n - 1, 0, -1):               # Extract elements from the heap one by one
        arr[0], arr[i] = arr[i], arr[0]         # Move current root to end
        heapify(arr, i, 0)                      # Call heapify on the reduced heap