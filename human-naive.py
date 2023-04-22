def assign_tasks(junior_engineers, senior_engineers, tasks, cutoff):
    task_assignments = []

    # Capacity is the number of hours worked by an engineer based on the tasks they've been assigned
    sorted_tasks = sorted(tasks, reverse=True)
    junior_engineer_capacity = [0] * junior_engineers
    senior_engineer_capacity = [0] * senior_engineers

    # General idea:
    # - For each task, based on the cutoff assign the task to the engineer with the least capacity
    for task in sorted_tasks:
        if task <= cutoff and junior_engineers:
            assigned_engineer = junior_engineer_capacity.index(min(junior_engineer_capacity))
            junior_engineer_capacity[assigned_engineer] += task
            task_assignments.append(('Junior', assigned_engineer, task))
        else:
            assigned_engineer = senior_engineer_capacity.index(min(senior_engineer_capacity))
            senior_engineer_capacity[assigned_engineer] += task
            task_assignments.append(('Senior', assigned_engineer, task))

    return task_assignments, junior_engineer_capacity, senior_engineer_capacity

if __name__ == "__main__":
    # Create array of tasks, set number of junior and senior engineers
    tasks = [1] * 75 + [2] * 25 + [3] * 10 + [4] * 15 + [5] * 25 + [6] * 25 + [7] * 10 + [8] * 11 + [9] * 4
    junior_engineers = 15
    senior_engineers = 5

    # We always need at least one engineer
    assert(junior_engineers != 0 or senior_engineers != 0)

    cutoff_times = []
    for cutoff in range(1, 10):
        task_assignments, junior_engineer_time, senior_engineer_time = assign_tasks(junior_engineers, senior_engineers, tasks, cutoff)

        max_time = max(max(junior_engineer_time), max(senior_engineer_time))
        print(f"All tasks will be completed in {max_time} hours with a point cuttoff of {cutoff}")
        cutoff_times.append(max_time)

    print(f"Minimum number of hours to complete all tasks is {min(cutoff_times)} (cutoff {cutoff_times.index(min(cutoff_times)) + 1})")
