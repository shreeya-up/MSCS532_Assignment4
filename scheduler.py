import random

from priority_queue import Task, PriorityQueue

"""AI has been used to write some of the code for this script, but it has been reviewed and 
modified to ensure accuracy and clarity."""

def generate_tasks(n, max_arrival=10, max_duration=2, max_deadline_offset=15, seed=None):
    """
    Generates a list of random tasks for the simulation.
    """
    if seed is not None:
        random.seed(seed) 

    tasks = []
    for task_id in range(1, n + 1):
        arrival_time = random.randint(0, max_arrival)        # When the task shows up
        duration = random.randint(1, max_duration)            #How long it takes to run
        deadline = arrival_time + random.randint(2, max_deadline_offset)  # Must finish by this time

        task = Task(task_id=task_id, priority=deadline,
                    arrival_time=arrival_time, deadline=deadline)
        task.duration = duration   # Extra attribute, not part of the base Task class
        tasks.append(task)

    return tasks


def run_edf_simulation(tasks, verbose=True):
    """
    Simulates a single-processor Earliest-Deadline-First scheduler.

    At each unit of simulated time:
      1. Any tasks that have arrived by now are inserted into the queue.
      2. If the processor is idle, it picks up the task with the
         earliest deadline (extract_min) and runs it for its duration.
      3. We record whether each task finished before or after its deadline.

    Returns a list of result dicts for reporting/analysis.
    """
    pq = PriorityQueue()
    tasks_by_arrival = sorted(tasks, key=lambda t: t.arrival_time)
    pending = list(tasks_by_arrival)   # Tasks not yet arrived, in arrival order

    current_time = 0
    busy_until = 0          # Time at which the processor becomes free again
    running_task = None     #The task currently being executed, if any
    results = []             # Completion records for each task

    max_deadline = max(t.deadline for t in tasks)
    #Run the simulation until all tasks have arrived, been queued, and finished
    while pending or not pq.is_empty() or running_task is not None:

        #Step 1: move any tasks that have now arrived into the priority queue
        while pending and pending[0].arrival_time <= current_time:
            arrived_task = pending.pop(0)
            pq.insert(arrived_task)
            if verbose:
                print(f"t={current_time}: Task {arrived_task.task_id} arrived "
                      f"(deadline={arrived_task.deadline})")

        #Step 2: if the processor just became free, pick up the next task
        if running_task is None and not pq.is_empty() and current_time >= busy_until:
            running_task = pq.extract_min()
            busy_until = current_time + running_task.duration
            if verbose:
                print(f"t={current_time}: Processor starts Task {running_task.task_id} "
                      f"(runs until t={busy_until})")

        #Step 3: check if the running task has just finished
        if running_task is not None and current_time >= busy_until:
            finished_on_time = busy_until <= running_task.deadline
            results.append({
                "task_id": running_task.task_id,
                "arrival_time": running_task.arrival_time,
                "deadline": running_task.deadline,
                "finish_time": busy_until,
                "met_deadline": finished_on_time,
            })
            if verbose:
                status = "MET deadline" if finished_on_time else "MISSED deadline"
                print(f"t={busy_until}: Task {running_task.task_id} finished -> {status}")
            running_task = None   # Processor becomes free

        current_time += 1   # Advance simulated time by one unit

        # Safety valve in case of an unexpected infinite loop during testing
        if current_time > max_deadline + 100:
            break

    return results


def summarize_results(results):
    """Prints a short summary of how many tasks met or missed their deadlines."""
    total = len(results)
    met = sum(1 for r in results if r["met_deadline"])
    missed = total - met

    print("\n--- Scheduling Summary ---")
    print(f"Total tasks completed: {total}")
    print(f"Deadlines met:         {met}")
    print(f"Deadlines missed:      {missed}")
    if total > 0:
        print(f"On-time rate:          {met / total:.1%}")


if __name__ == "__main__":
    tasks = generate_tasks(n=10, seed=42)
    results = run_edf_simulation(tasks, verbose=True)
    summarize_results(results)