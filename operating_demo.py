from priority_queue import Task, PriorityQueue

"""This script demonstrates the usage of the priority queue implementation,
using the Task and PriorityQueue classes """

def print_heap(pq):
    """ Print the contents of the heap """
    print("Heap contents:")
    for i, task in enumerate(pq.heap):
        print(f"  {i}: Task ID={task.task_id}, Priority={task.priority}")

pq = PriorityQueue()
print("01: Check if empty before adding a task")
print("is_empty():", pq.is_empty())         # Should print True
print()

print("02: Add tasks to the priority queue")
pq.insert(Task(task_id=1, priority=5, arrival_time=0, deadline=10))
pq.insert(Task(task_id=2, priority=2, arrival_time=1, deadline=5))
pq.insert(Task(task_id=3, priority=8, arrival_time=2, deadline=20))
pq.insert(Task(task_id=4, priority=1, arrival_time=3, deadline=4))
print_heap(pq)

print("is_empty():", pq.is_empty())         # Should print False
print()

print("03: Decrease priority of task 3")
pq.decrease_key(task_id=3, new_priority=0)   # Make task 3 more urgent
print_heap(pq)
print()

print("04: Task 2's deadline got pushed back")
pq.increase_key(task_id=2, new_priority=15)  # Push back task 2's deadline
print_heap(pq)
print()

print("05: Remove tasks from the priority queue")
while not pq.is_empty():
    task = pq.extract_min()                    # Extract the task with the highest priority
    print(f"Extracted task: ID={task.task_id}")
print()

print("06: Check if empty after removing all tasks")
print("is_empty():", pq.is_empty())         # Should print True
print()
