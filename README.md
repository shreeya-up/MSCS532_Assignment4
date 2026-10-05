# MSCS532_Assignment4
Heap Data Structures

Implementation and analysis of Heapsort and a heap-based priority queue, including an
Earliest-Deadline-First (EDF) task scheduler simulation.

## Files

`heap_sort.py` contains the Heapsort implementation (`build_max_heap`, `heapify`, `heap_sort`).
`benchmark.py` compares Heapsort, Quicksort, and Merge Sort across input sizes and
distributions, and outputs `results.png`. `priority_queue.py` holds the array-based
min-heap priority queue (`Task` and `PriorityQueue` classes), while `demo_operations.py`
provides a simple walkthrough of all four priority queue operations. `scheduler.py`
contains the EDF scheduler simulation built on top of the priority queue. Finally,
`Priority_Queue_Report.docx` is the written report covering design choices, complexity
analysis, and scheduling results.

## How to Run

Requires Python 3 and `matplotlib`.

```bash
pip install matplotlib

# Sort comparison (saves results.png)
python benchmark.py

# Priority queue operations demo
python demo_operations.py

# EDF scheduler simulation
python scheduler.py
```

## Summary of Findings

**Heapsort vs. Quicksort vs. Merge Sort**
- All three run at O(n log n) in practice, but constant factors differ: Quicksort is
  fastest on typical inputs, Merge Sort is in between, and Heapsort is slowest due to
  weaker cache locality.
- On inputs with many repeated values, Quicksort's performance degrades and it becomes
  the *slowest* of the three, which is a practical demonstration of its O(n²) worst case.
- Memory usage matches theory: Merge Sort grows linearly with input size (O(n)),
  Heapsort stays constant (O(1)), and Quicksort stays small and roughly constant (O(log n)).

**Priority Queue**
- Implemented as an array-based min-heap with a `position` map, giving O(log n) time
  for `insert`, `extract_min`, `increase_key`, and `decrease_key`, and O(1) for `is_empty`.

**EDF Scheduler**
- When task arrivals are light, the scheduler meets all deadlines easily.
- Under heavier load, deadline misses cascade: once the processor falls behind, later
  tasks miss their deadlines even if those deadlines were individually reasonable. This
  reflects a property of scheduling under overload, not a flaw in the implementation.
