import random
import time
import tracemalloc
import matplotlib.pyplot as plt

from heap_sort import heap_sort


# Code written referencing visualization pipelines and Quicksort/Mergesort implementations from previous assignments

# Quicksort
def partition(a, lo, hi, p_index):
    """Decides on the pivot index based on the p_index parameter and partitions the array."""
    if p_index == "random":
        m = random.randint(lo, hi)
    elif p_index == "first":
        m = lo
    elif p_index == "median3":
        mid = (lo + hi) // 2
        m = sorted((lo, mid, hi), key=lambda i: a[i])[1]
    else:
        m = hi
    a[m], a[hi] = a[hi], a[m]        # Moving chosen pivot to the end
    x = a[hi]
    i = lo - 1                       # boundary index
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]   # placing pivot in its final position
    return i + 1


def quick_sort(a, p_index):
    """Sorts the array in place using the quicksort algorithm."""
    def sort(lo, hi):
        while lo < hi:
            q = partition(a, lo, hi, p_index)
            if q - lo < hi - q:
                sort(lo, q - 1)
                lo = q + 1
            else:
                sort(q + 1, hi)
                hi = q - 1
    sort(0, len(a) - 1)


def ran_quick_sort(a):
    """Sorts the array in place using the randomized quicksort algorithm."""
    quick_sort(a, "random")


# MergeSort
def merge(a, lo, mid, hi):
    """
    Merges two adjacent sorted subarrays a[lo:mid+1] and a[mid+1:hi+1]
    into a single sorted subarray a[lo:hi+1].
    This step requires O(n) auxiliary space for the temporary copies.
    """
    left = a[lo:mid + 1]
    right = a[mid + 1:hi + 1]

    i = 0
    j = 0
    k = lo

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:      # '<=' keeps the sort stable
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        a[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        a[k] = right[j]
        j += 1
        k += 1


def _merge_sort(a, lo, hi):
    """Recursively sorts a[lo:hi+1] by splitting, sorting, and merging."""
    if lo < hi:
        mid = (lo + hi) // 2
        _merge_sort(a, lo, mid)
        _merge_sort(a, mid + 1, hi)
        merge(a, lo, mid, hi)


def merge_sort(a):
    """Sorts the list 'a' in place using Merge Sort."""
    _merge_sort(a, 0, len(a) - 1)



# Benchmarking and visualization
"""This script compares the performance of randomized quicksort, merge sort, and heap sort 
algorithms across different input sizes and distributions, and visualizes the results.
AI has been used to write some of the code for this script, but it has been reviewed and 
modified to ensure accuracy and clarity."""

size = [500, 1000, 1500, 2000]
types = ["random", "sorted", "reverse", "repeated"]
algorithms = {
    "Randomized quick sort": ran_quick_sort,
    "Merge sort": merge_sort,
    "Heap sort": heap_sort,
}


# Building the input data
def build_data(type, n):
    if type == "random":
        return random.sample(range(n), n)
    if type == "sorted":
        return list(range(n))
    if type == "reverse":
        return list(range(n, 0, -1))
    if type == "repeated":
        return [random.randint(0, 20) for _ in range(n)]


# Measure the time taken by a sorting algorithm to sort an array
def measure_time(sort_func, data):
    best = float("inf")
    for _ in range(3):
        copy = data[:]
        start = time.perf_counter()
        sort_func(copy)
        best = min(best, time.perf_counter() - start)
    return best


def measure_memory(sort_func, data):
    copy = data[:]
    tracemalloc.start()
    sort_func(copy)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return peak / 1024        # Conversion to kB


# Run and visualize the results

times = {}
memory = {}
for type in types:
    for name, sort_func in algorithms.items():
        times[(type, name)] = []
        memory[(type, name)] = []
        for n in size:
            data = build_data(type, n)
            times[(type, name)].append(measure_time(sort_func, data))
            memory[(type, name)].append(measure_memory(sort_func, data))
            print(type, name, n, "done")


# Plotting the results
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for col, type in enumerate(types):
    for name in algorithms:
        axes[0][col].plot(size, times[(type, name)], marker="o", label=name)
        axes[1][col].plot(size, memory[(type, name)], marker="o", label=name)
    axes[0][col].set_title(type)
    axes[0][col].set_ylabel("time (seconds)")
    axes[1][col].set_ylabel("peak extra memory (KiB)")
    axes[1][col].set_xlabel("n (number of elements)")
axes[0][0].legend()
plt.tight_layout()
plt.savefig("results.png", dpi=150)
plt.show()