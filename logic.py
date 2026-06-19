import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def run_non_preemptive(self, data, name, criteria_idx=None):
        ready_pool = list(data)
        arrival_times = {p[0]: p[1] for p in ready_pool}
        burst_times = {p[0]: p[2] for p in ready_pool}
        time = 0
        gantt = []

        while ready_pool:
            available = [p for p in ready_pool if p[1] <= time]
            if not available:
                time = min(p[1] for p in ready_pool)
                available = [p for p in ready_pool if p[1] <= time]

            if criteria_idx is not None:
                chosen = min(available, key=lambda x: (x[criteria_idx], x[1]))
            else:
                chosen = min(available, key=lambda x: x[1])

            pid, at, bt, pr = chosen
            start = time
            end = start + bt
            gantt.append((pid, start, end))
            time = end
            ready_pool.remove(chosen)

        self.calculate_and_display_metrics(gantt, arrival_times, burst_times, name)

def run_preemptive(self, name, criteria_func):
        pool = sorted(self.processes, key=lambda x: x[1])
        arrival_times = {p[0]: p[1] for p in pool}
        burst_times = {p[0]: p[2] for p in pool}
        remaining = {p[0]: p[2] for p in pool}
        
        gantt = []
        time = 0
        last_pid = None
        block_start = 0

        while True:
            available = [p for p in pool if p[1] <= time and remaining[p[0]] > 0]
            
            if not available:
                unfinished = [p for p in pool if remaining[p[0]] > 0]
                if not unfinished:
                    break
                time = min(p[1] for p in unfinished)
                available = [p for p in pool if p[1] <= time and remaining[p[0]] > 0]

            chosen = min(available, key=lambda x: criteria_func(x, remaining))
            pid = chosen[0]

            if last_pid is not None and last_pid != pid:
                gantt.append((last_pid, block_start, time))
                block_start = time
            elif last_pid is None:
                block_start = time

            remaining[pid] -= 1
            time += 1
            last_pid = pid

            if remaining[pid] == 0:
                gantt.append((pid, block_start, time))
                last_pid = None

        compressed_gantt = []
        for pid, s, e in gantt:
            if compressed_gantt and compressed_gantt[-1][0] == pid and compressed_gantt[-1][2] == s:
                compressed_gantt[-1] = (pid, compressed_gantt[-1][1], e)
            else:
                compressed_gantt.append((pid, s, e))

        self.calculate_and_display_metrics(compressed_gantt, arrival_times, burst_times, name)

def calculate_and_display_metrics(self, gantt, arrival_times, burst_times, name):
        end_times = {pid: end for pid, start, end in gantt}

        wt = []
        tat = []
        for pid in arrival_times:
            ft = end_times.get(pid, 0)
            t_at = ft - arrival_times[pid]
            w_t = t_at - burst_times[pid]
            wt.append(max(0, w_t))
            tat.append(max(0, t_at))

        avg_wt = sum(wt) / len(wt) if wt else 0
        avg_tat = sum(tat) / len(tat) if tat else 0

        self.result_title_label.configure(text=f"ACTIVE ALGORITHM: {name.upper()}")
        self.center_metrics_label.configure(
            text=f"Avg Waiting Time: {avg_wt:.2f} ms  |  Avg Turnaround Time: {avg_tat:.2f} ms"
        )
        
        self.metric_cards["avg_wt"]["val_lbl"].configure(text=f"{avg_wt:.2f} ms")
        self.metric_cards["avg_tat"]["val_lbl"].configure(text=f"{avg_tat:.2f} ms")

        self.draw_chart(gantt)
        self.update_metrics(gantt)

def draw_chart(self, gantt):
        if not gantt:
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        unique_pids = sorted(list(set(p[0] for p in gantt)))
        pid_to_row = {pid: i for i, pid in enumerate(unique_pids)}
        total_rows = len(unique_pids)

        fig, ax = plt.subplots(figsize=(10, max(4, total_rows * 0.7)), facecolor="#1e1e1e")
        ax.set_facecolor("#1e1e1e")

        neon_colors = ["#00E676", "#00B0FF", "#FFD700", "#FF3D00", "#D500F9", "#1DE9B6", "#FF9100", "#FF4081"]
        pid_color_map = {pid: neon_colors[i % len(neon_colors)] for i, pid in enumerate(unique_pids)}

        box_height = 0.55
        last_end_time = 0

        for pid, start, end in gantt:
            duration = end - start
            if duration <= 0:
                continue

            row_idx = pid_to_row[pid]
            color = pid_color_map[pid]

            if start > last_end_time:
                for r in range(total_rows):
                    idle_box = patches.FancyBboxPatch(
                        (last_end_time, r - box_height/2), start - last_end_time, box_height,
                        boxstyle="round,pad=0.03,rounding_size=0.1",
                        facecolor="#2d2d2d", edgecolor="#444444", linestyle="--", hatch="///", alpha=0.4
                    )
                    ax.add_patch(idle_box)
                
                ax.text(
                    last_end_time + (start - last_end_time)/2, total_rows / 2 - 0.5,
                    "CPU IDLE", color="#666666", fontsize=9, fontweight="bold", ha="center", va="center", alpha=0.7
                )

            fancy_box = patches.FancyBboxPatch(
                (start, row_idx - box_height/2), duration, box_height,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor=color, edgecolor=color, linewidth=1, alpha=0.85
            )
            ax.add_patch(fancy_box)

            text_color = "#000000" if color in ["#FFD700", "#00E676", "#1DE9B6"] else "#FFFFFF"
            ax.text(
                start + (duration / 2), row_idx, f"{pid}\n({duration}ms)",
                ha="center", va="center", color=text_color, fontweight="bold", fontsize=9
            )
            last_end_time = max(last_end_time, end)

        max_time = max(p[2] for p in gantt)
        ax.set_xlim(-0.5, max_time + 0.5)
        ax.set_ylim(-0.75, total_rows - 0.25)

        tick_step = 1 if max_time <= 20 else (2 if max_time <= 50 else 5)
        ax.set_xticks(range(0, int(max_time) + 1, tick_step))
        ax.set_yticks(range(total_rows))
        ax.set_yticklabels(unique_pids, fontsize=11, fontweight="bold", color="#FFFFFF")

        ax.tick_params(axis='x', colors="#A0A0A0", labelsize=10)
        ax.tick_params(axis='y', colors="#FFFFFF", length=0)
        ax.set_xlabel("TIME UNITS (ms)", fontsize=11, fontweight="bold", color="#A0A0A0", labelpad=12)
        ax.grid(axis="x", linestyle=":", color="#FFFFFF", alpha=0.1)

        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

def update_metrics(self, gantt):
        if not gantt:
            return
        total_time = max(p[2] for p in gantt)

        self.metric_cards["exec_time"]["val_lbl"].configure(text=f"{total_time} ms")
        self.metric_cards["proc_count"]["val_lbl"].configure(text=str(len(self.processes)))
        
        self.metric_cards["cpu_status"]["val_lbl"].configure(text="ACTIVE", text_color="#2ECC71")
        self.metric_cards["cpu_status"]["accent"].configure(fg_color="#2ECC71")
        self.metric_cards["sched_status"]["val_lbl"].configure(text="SUCCESS")