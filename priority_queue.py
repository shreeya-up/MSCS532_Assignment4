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


