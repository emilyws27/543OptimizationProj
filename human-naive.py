def assign_tasks(junior_engineers, senior_engineers, tasks, cutoff):
    task_assignments = []

    sorted_tasks = sorted(tasks, reverse=True)
    junior_engineer_capacity = [0] * junior_engineers
    senior_engineer_capacity = [0] * senior_engineers

    for task in sorted_tasks:
        if task <= cutoff and junior_engineers:
            assigned_engineer = junior_engineer_capacity.index(min(junior_engineer_capacity))
            junior_engineer_capacity[assigned_engineer] += task
            task_assignments.append(('Junior', assigned_engineer, task))
        elif senior_engineers:
            assigned_engineer = senior_engineer_capacity.index(min(senior_engineer_capacity))
            senior_engineer_capacity[assigned_engineer] += task
            task_assignments.append(('Senior', assigned_engineer, task))
        else:
            assigned_engineer = junior_engineer_capacity.index(min(junior_engineer_capacity))
            junior_engineer_capacity[assigned_engineer] += task
            task_assignments.append(('Junior', assigned_engineer, task))

    return task_assignments, junior_engineer_capacity, senior_engineer_capacity

if __name__ == "__main__":
    tasks = [1] * 75 + [2] * 25 + [3] * 10 + [4] * 15 + [5] * 25 + [6] * 25 + [7] * 10 + [8] * 11 + [9] * 4
    junior_engineers = 15
    senior_engineers = 5

    cutoff_times = []
    for cutoff in range(1, 10):
        task_assignments, junior_engineer_time, senior_engineer_time = assign_tasks(junior_engineers, senior_engineers, tasks, cutoff)

        # for assignment in task_assignments:
            # print(f"{assignment[0]} Engineer {assignment[1]} assigned task with {assignment[2]} story points")

        max_time = max(max(junior_engineer_time), max(senior_engineer_time))
        print(f"All tasks will be completed in {max_time} hours with a point cuttoff of {cutoff}")
        cutoff_times.append(max_time)

    print(f"Minimum number of hours to complete all tasks is {min(cutoff_times)}")
