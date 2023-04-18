def identical_machines(tasks, rate, n):
    schedule = [[] for _ in range(n)]
    processor_loads = [0 for _ in range(n)]

    # assign each task to the processor with the least amount of scheduled work
    for task_id, task_duration in tasks:
        min_workload = float('inf')
        min_processor = 0
        for i in range(n):
            if processor_loads[i] < min_workload:
                min_workload = processor_loads[i]
                min_processor = i
        schedule[min_processor].append((task_id, task_duration))
        processor_loads[min_processor] += task_duration

    makespan = max([processor_loads[i] / rate for i in range(n)])
    return schedule, makespan


def uniform_machines(tasks, processors):
    rates = [processor.rate for processor in processors]
    n = len(rates)
    schedule = [[] for _ in range(n)]
    processor_loads = [0 for _ in range(n)]

    # Assign each task to the machine that will finish it first
    for task_id, task_duration in tasks:
        min_finish = float('inf')
        min_processor = 0
        for i in range(n):
            finish = (processor_loads[i] + task_duration) / rates[i]
            if finish < min_finish:
                min_finish = finish
                min_processor = i
        schedule[min_processor].append((task_id, task_duration))
        processor_loads[min_processor] += task_duration

    makespan = max([processor_loads[i] / rates[i] for i in range(n)])
    return schedule, makespan


def remove_dependency_from_dag(dag, id):
    for task_id in dag.keys():
        dag[task_id] = [j for j in dag[task_id] if j != id]


def take_one_step_in_time(processors, time_step, dag):
    for processor in processors:
        if len(processor.current_work) > 0:
            task_id_0, task_points_0 = processor.current_work[0]
            t = task_points_0 / processor.rate
            if t < time_step + 1e-3:
                remove_dependency_from_dag(dag, task_id_0)
                processor.current_work = processor.current_work[1:]
            else:
                new_task_points = task_points_0 - time_step * processor.rate
                processor.current_work[0] = (task_id_0, new_task_points)


def get_min_timestep(processors):
    min_timestep = float('inf')
    for processor in processors:
        time = 1 / processor.rate
        if time < min_timestep:
            min_timestep = time
    return min_timestep


def get_available_task(tasks, dag):
    picked_task = None
    for task_id, task_points in tasks:
        if len(dag[task_id]) == 0:
            picked_task = (task_id, task_points)
            break
    return picked_task


def collapse_idles(schedule):
    collapsed = [[] for _ in schedule]

    for i, lst in enumerate(schedule):
        if len(lst) == 0:
            continue

        prev_id, prev_points = lst[0]
        for id, points in lst[1:]:
            if id != prev_id:
                collapsed[i].append((prev_id, prev_points))
                prev_id = id
                prev_points = points
            else:
                prev_points += points

        collapsed[i].append((prev_id, prev_points))

        if collapsed[i][len(collapsed[i]) - 1][0] == -1: #remove end idles
            collapsed[i] = collapsed[i][:-1]

    return collapsed



def schedule_with_dependencies(tasks, processors, dag):
    n = len(processors)
    schedule = [[] for _ in range(n)]

    timestep_size = get_min_timestep(processors)

    while True:
        for i, processor in enumerate(processors):
            if len(processor.current_work) == 0:
                picked_task = get_available_task(tasks, dag)

                if picked_task is not None:
                    a, _ = picked_task
                    processor.current_work.append(picked_task)
                    tasks = [(_id, _duration) for _id, _duration in tasks if _id != a]
                    schedule[i].append(picked_task)
                elif len(tasks) > 0:
                    schedule[i].append((-1, timestep_size * processor.rate))

        take_one_step_in_time(processors, timestep_size, dag)
        if len(tasks) == 0:
            break

    makespan = -1
    for i, lst in enumerate(schedule):
        rate = processors[i].rate
        total = 0
        for _, duration in lst:
            total += duration / rate
        if total > makespan:
            makespan = total

    return collapse_idles(schedule), makespan


class Processor:
    def __init__(self, rate):
        self.current_work = []
        self.rate = rate


def print_makespan_schedule(makespan, schedule):
    print(f'makespan: {makespan}')
    for i, lst in enumerate(schedule):
        print()
        print(f'{i}: ', end='')
        for a, b in lst:
            if a == -1:
                print(f'(IDLE, {b}), ', end='')
            else:
                print(f'({a}, {b}), ', end='')


if __name__ == '__main__':

    processors = []
    for i in range(20):
        if i < 5:
            processors.append(Processor(4))
        else:
            processors.append(Processor(1))

    tasks = []
    for i in range(1, 200 + 1):
        if i <= 75:
            tasks.append((i, 1))
        elif i <= 100:
            tasks.append((i, 2))
        elif i <= 110:
            tasks.append((i, 3))
        elif i <= 125:
            tasks.append((i, 4))
        elif i <= 150:
            tasks.append((i, 5))
        elif i <= 175:
            tasks.append((i, 6))
        elif i <= 185:
            tasks.append((i, 7))
        elif i <= 196:
            tasks.append((i, 8))
        elif i <= 200:
            tasks.append((i, 9))

    dag = dict()
    for id, _ in tasks:
        dag[id] = []

    for comes_later in range(76, 80 + 1):
        for comes_before in range(1, 20 + 1):
            dag[comes_later].append(comes_before)

    for comes_later in range(111, 117 + 1):
        for comes_before in range(125, 133 + 1):
            dag[comes_later].append(comes_before)

    for comes_later in range(53, 69 + 1):
        for comes_before in range(111, 117 + 1):
            dag[comes_later].append(comes_before)

    for comes_later in range(123, 125 + 1):
        dag[comes_later].append(101)

    for comes_later in range(170, 175 + 1):
        dag[comes_later].append(101)

    print()
    print('############### Identical #########################')

    schedule, makespan = identical_machines(tasks, 1, 20)
    print_makespan_schedule(makespan, schedule)

    print()
    print('#################### Uniform ######################')

    schedule, makespan = uniform_machines(tasks, processors)
    print_makespan_schedule(makespan, schedule)

    print()
    print('################## Dependencies #######################')

    schedule, makespan = schedule_with_dependencies(tasks, processors, dag)
    print_makespan_schedule(makespan, schedule)
