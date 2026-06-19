from collections import deque


class Scheduler:
    def fcfs(self):
        if not self.processes:
            return
        data = sorted(self.processes, key=lambda x: x[1])
        self.run_non_preemptive(data, "FCFS", None)

    def sjf(self):
        if not self.processes:
            return
        if self.mode_var.get() == "Preemptive":
            self.run_preemptive("SJF (SRTF)", criteria_func=lambda x, rem: rem[x[0]])
        else:
            data = sorted(self.processes, key=lambda x: x[1])
            self.run_non_preemptive(data, "SJF Non-Preemptive", criteria_idx=2)

    def priority_sched(self):
        if not self.processes:
            return
        if self.mode_var.get() == "Preemptive":
            self.run_preemptive("Preemptive Priority", criteria_func=lambda x, rem: x[3])
        else:
            data = sorted(self.processes, key=lambda x: x[1])
            self.run_non_preemptive(data, "Non-Preemptive Priority", criteria_idx=3)

    def round_robin(self):
        if not self.processes:
            return
        try:
            q = int(self.quantum.get())
        except ValueError:
            q = 2

        pool = sorted(self.processes, key=lambda x: x[1])
        queue = deque()
        remaining_bt = {p[0]: p[2] for p in pool}
        arrival_times = {p[0]: p[1] for p in pool}
        burst_times = {p[0]: p[2] for p in pool}
        
        gantt = []
        time = 0
        pool_idx = 0

        while pool_idx < len(pool) and pool[pool_idx][1] <= time:
            queue.append(pool[pool_idx])
            pool_idx += 1

        while queue or pool_idx < len(pool):
            if not queue and pool_idx < len(pool):
                time = pool[pool_idx][1]
                queue.append(pool[pool_idx])
                pool_idx += 1

            pid, at, bt, pr = queue.popleft()
            execute = min(q, remaining_bt[pid])
            start = time
            time += execute
            remaining_bt[pid] -= execute
            gantt.append((pid, start, time))

            while pool_idx < len(pool) and pool[pool_idx][1] <= time:
                queue.append(pool[pool_idx])
                pool_idx += 1

            if remaining_bt[pid] > 0:
                queue.append((pid, at, bt, pr))

        self.calculate_and_display_metrics(gantt, arrival_times, burst_times, f"Round Robin (q={q})")