class Task:
    """
    Represents a single task to be scheduled.
    priority: lower value = higher urgency (min-heap usage).
    task_ids are unique, since they are used as the key in the position map.
    """
    def __init__(self, task_id, priority, arrival_time=None, deadline=None):
        self.task_id = task_id              # Unique identifier for this task
        self.priority = priority            # Lower value = more urgent (min-heap)
        self.arrival_time = arrival_time    # When the task entered the system
        self.deadline = deadline            # When the task needs to be completed

    def __repr__(self):
        return (f"Task(id={self.task_id}, priority={self.priority}, "
                f"arrival={self.arrival_time}, deadline={self.deadline})")   #Defines how a Task prints
    
class PriorityQueue:
    """
    Array-based binary min-heap priority queue.
     self.heap: list of Task objects, stored in heap order.
    self.position: dict mapping task_id -> current index in self.heap.
                    
    """
 
    def __init__(self):
        self.heap = []        # The heap itself, stored as a flat list of Task objects
        self.position = {}    # task_id -> index in self.heap, kept in sync on every swap
 
    def is_empty(self):
        """O(1) check for whether the queue has any tasks."""
        return len(self.heap) == 0   # True if the list has zero elements
 
 
    def e_swap(self, i, j):
        """Swaps two heap elements and keeps the position map in sync."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]   # Swap the two Task objects
        self.position[self.heap[i].task_id] = i                   # Update position map for the task now at index i
        self.position[self.heap[j].task_id] = j                   # Update position map for the task now at index j
 
    def parent(self, i):
        return (i - 1) // 2   # Integer division maps child index to its parent index
 
    def c_left(self, i):
        return 2 * i + 1      # Array-heap formula for the left child
 
    def c_right(self, i):
        return 2 * i + 2      # Array-heap formula for the right child
 
    def sift_up(self, i):
        """
        Moves the task at index i upward until the min-heap property
        is restored (parent's priority <= child's priority).
        """
    
        while i > 0 and self.heap[i].priority < self.heap[self.parent(i)].priority:
            parent_idx = self.parent(i)        # Compute the parent's index once
            self.e_swap(i, parent_idx)           # Swap the out-of-place node with its parent
            i = parent_idx                      # Continue checking from the new position
 
    def sift_down(self, i):
        """
        Moves the task at index i downward until the min-heap property
        is restored. Runs at most O(log n) times.
        """
        n = len(self.heap)          # Cache the heap size for comparisons below
        while True:                 # Loop until no more swaps are needed
            smallest = i                    # Assume current node is the smallest to start
            left = self.c_left(i)            # Index of left child
            right = self.c_right(i)          # Index of right child
 
            if left < n and self.heap[left].priority < self.heap[smallest].priority: 
                smallest = left         # If the left child exists and is smaller than current smallest, update smallest
            
            if right < n and self.heap[right].priority < self.heap[smallest].priority:
                smallest = right        # If the right child exists and is smaller than current smallest, update smallest
 
            if smallest == i:
                break  # Heap property satisfied
 
            self.e_swap(i, smallest)   # Swap current node with its smaller child
            i = smallest               # Continue checking from the new position
 
 
    def insert(self, task):
        """
        Inserts a new task into the heap.
        """
        self.heap.append(task)              # Add the new task at the end of the array
        i = len(self.heap) - 1              # Index of the newly inserted task
        self.position[task.task_id] = i     # Record position in the map
        self.sift_up(i)                    # Restore heap property by moving it upward if needed
 
    def extract_min(self):
        """
        Removes and returns the task with the lowest priority value
        (i.e., the most urgent task).
        """
        if self.is_empty():
            # Guard against calling this on an empty queue
            raise IndexError("extract_min() called on empty priority queue")
 
        min_task = self.heap[0]             # The root always holds the minimum-priority task
        last_task = self.heap.pop()         # Remove the last element in the array, O(1)
        del self.position[min_task.task_id] # Remove the extracted task from the position map
 
        if self.heap:                       # Only continue if there's at least one task left
            self.heap[0] = last_task        # Move the former last element to the root
            self.position[last_task.task_id] = 0   # Update its position in the map
            self.sift_down(0)              # Restore heap property by moving it downward if needed
 
        return min_task                     # Return the task that was removed
 
    def decrease_key(self, task_id, new_priority):
        """
        Lowers the priority value of an existing task (making it MORE
        urgent, since this is a min-heap) and moves it up if needed.
        """
        if task_id not in self.position:
            # Guard against referencing a task that isn't in the queue
            raise KeyError(f"Task {task_id} not found in priority queue")
 
        i = self.position[task_id]          # O(1) lookup of the task's current index
        if new_priority > self.heap[i].priority:
            # This method is only for making priority smaller/more urgent
            raise ValueError("New priority is greater than current priority; "
                              "use increase_key instead")
 
        self.heap[i].priority = new_priority   # Update the stored priority value
        self.sift_up(i)   # Priority got smaller, so it may need to move toward the root
 
    def increase_key(self, task_id, new_priority):
        """
        Raises the priority value of an existing task (making it LESS
        urgent) and moves it down if needed.
        """
        if task_id not in self.position:
            # Guard against referencing a task that isn't in the queue
            raise KeyError(f"Task {task_id} not found in priority queue")
 
        i = self.position[task_id]          # O(1) lookup of the task's current index
        if new_priority < self.heap[i].priority:
            # This method is only for making priority larger/less urgent
            raise ValueError("New priority is less than current priority; "
                              "use decrease_key instead")
 
        self.heap[i].priority = new_priority   # Update the stored priority value
        self.sift_down(i)   # Priority got larger, so it may need to move away from the root
 
 
if __name__ == "__main__":
    pq = PriorityQueue()   # Create a new, empty priority queue
 
    # Insert four tasks with different priorities (lower = more urgent)
    pq.insert(Task(task_id=1, priority=5, arrival_time=0, deadline=10))
    pq.insert(Task(task_id=2, priority=2, arrival_time=1, deadline=5))
    pq.insert(Task(task_id=3, priority=8, arrival_time=2, deadline=20))
    pq.insert(Task(task_id=4, priority=1, arrival_time=3, deadline=4))
 
    print("Is empty?", pq.is_empty())   # Should print False, since we just inserted tasks
 
    # Make task 3 suddenly urgent (e.g., its deadline just moved up)
    pq.decrease_key(task_id=3, new_priority=0)
 
    # Process tasks in priority order, removing the most urgent each time
    while not pq.is_empty():
        print("Processing:", pq.extract_min())
    
