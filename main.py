import customtkinter as ctk
from tkinter import ttk, messagebox
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SchedulerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1600x900")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.processes = []
        self.metric_cards = {}
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        self._setup_top_bar()

        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self._setup_left_panel(container)
        self._setup_right_panel(container)
        self._setup_center_panel(container)

    def _setup_top_bar(self):

        top = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        top.pack(fill="x")

        title = ctk.CTkLabel(
            top,
            text="CPU SCHEDULING SIMULATOR",
            font=("Arial", 35, "bold")
        )
        title.pack(side="left", padx=30, pady=20)

        self.theme_btn = ctk.CTkButton(
            top,
            text=" DARK/LIGHT",
            width=150,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", padx=20)

    def _setup_left_panel(self, parent):

        left = ctk.CTkFrame(parent, width=350)
        left.pack(side="left", fill="y", padx=10, pady=10)

        content_frame = ctk.CTkFrame(left, fg_color="transparent")
        content_frame.pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(
            content_frame,
            text="ADD PROCESS",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        self.pid = ctk.CTkEntry(content_frame, placeholder_text="Process ID")
        self.pid.pack(pady=8, padx=20)

        self.at = ctk.CTkEntry(content_frame, placeholder_text="Arrival Time")
        self.at.pack(pady=8, padx=20)

        self.bt = ctk.CTkEntry(content_frame, placeholder_text="Burst Time")
        self.bt.pack(pady=8, padx=20)

        self.pr = ctk.CTkEntry(content_frame, placeholder_text="Priority")
        self.pr.pack(pady=8, padx=20)

        self.quantum = ctk.CTkEntry(content_frame, placeholder_text="Quantum (RR)")
        self.quantum.pack(pady=8, padx=20)

        ctk.CTkButton(
            content_frame,
            text="ADD PROCESS",
            height=40,
            font=("Arial", 15, "bold"),
            command=self.add_process
        ).pack(pady=15)

        ctk.CTkLabel(
            content_frame,
            text="ALGORITHM MODE",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 5))

        self.mode_var = ctk.StringVar(value="Non-Preemptive")
        
        preempt_rb = ctk.CTkRadioButton(
            content_frame, 
            text="Preemptive (SRTF / P-Prio)", 
            variable=self.mode_var, 
            value="Preemptive"
        )
        preempt_rb.pack(anchor="w", padx=40, pady=5)
        
        non_preempt_rb = ctk.CTkRadioButton(
            content_frame, 
            text="Non-Preemptive", 
            variable=self.mode_var, 
            value="Non-Preemptive"
        )
        non_preempt_rb.pack(anchor="w", padx=40, pady=5)

        bottom_left_frame = ctk.CTkFrame(left, fg_color="transparent")
        bottom_left_frame.pack(side="bottom", fill="x", pady=(10, 20), padx=20)

        self.end_btn = ctk.CTkButton(
            bottom_left_frame,
            text="🛑 END SIMULATION",
            height=40,
            fg_color="#D32F2F",
            hover_color="#C62828",
            font=("Arial", 13, "bold"),
            command=self.reset_to_main_ui
        )
        self.end_btn.pack(fill="x")

    def _setup_center_panel(self, parent):

        center = ctk.CTkFrame(parent)
        center.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        table_frame = ctk.CTkFrame(center)
        table_frame.pack(fill="x", padx=20, pady=15)

        columns = ("PID", "AT", "BT", "PR")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            rowheight=35,
            fieldbackground="#1e1e1e",
            font=("Arial", 11)
        )
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")
        self.tree.pack(fill="x")

        algo_frame = ctk.CTkFrame(center)
        algo_frame.pack(pady=10)

        ctk.CTkButton(algo_frame, text="FCFS", width=110, command=self.fcfs).pack(side="left", padx=5)
        ctk.CTkButton(algo_frame, text="SJF", width=110, command=self.sjf).pack(side="left", padx=5)
        ctk.CTkButton(algo_frame, text="PRIORITY", width=110, command=self.priority_sched).pack(side="left", padx=5)
        ctk.CTkButton(algo_frame, text="ROUND ROBIN", width=130, command=self.round_robin).pack(side="left", padx=5)

        self.advisor_btn = ctk.CTkButton(
            algo_frame,
            text="💡 SMART ADVISOR",
            width=150,
            fg_color="#A334FA",
            hover_color="#7B1FA2",
            font=("Arial", 12, "bold"),
            command=self.smart_advisor
        )
        self.advisor_btn.pack(side="left", padx=10)

        self.result_title_label = ctk.CTkLabel(
            center,
            text="ACTIVE ALGORITHM: NONE",
            font=("Arial", 16, "bold"),
            text_color="#3498DB"
        )
        self.result_title_label.pack(pady=(10, 5))

        
        self.center_metrics_container = ctk.CTkFrame(center, fg_color="transparent")
        self.center_metrics_container.pack(fill="x", padx=40, pady=(5, 15))
        self.center_metrics_container.columnconfigure((0, 1), weight=1, uniform="equal")


        self.wt_hero_card = ctk.CTkFrame(self.center_metrics_container, height=90, corner_radius=12, border_width=1, border_color="#3A3A3A")
        self.wt_hero_card.grid(row=0, column=0, padx=15, sticky="nsew")
        self.wt_hero_card.pack_propagate(False)
        
        wt_accent = ctk.CTkFrame(self.wt_hero_card, width=6, fg_color="#F39C12", corner_radius=0)
        wt_accent.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.wt_hero_card, text="AVERAGE WAITING TIME", font=("Arial", 11, "bold"), text_color="#A0A0A0").pack(anchor="w", padx=20, pady=(12, 0))
        self.wt_hero_val = ctk.CTkLabel(self.wt_hero_card, text="0.00 ms", font=("Arial", 26, "bold"), text_color="#F39C12")
        self.wt_hero_val.pack(side="left", anchor="w", padx=20, pady=(0, 10))
        self.wt_hero_status = ctk.CTkLabel(self.wt_hero_card, text="— No Workload", font=("Arial", 11, "italic"), text_color="#666666")
        self.wt_hero_status.pack(side="right", anchor="e", padx=20, pady=(0, 15))


        self.tat_hero_card = ctk.CTkFrame(self.center_metrics_container, height=90, corner_radius=12, border_width=1, border_color="#3A3A3A")
        self.tat_hero_card.grid(row=0, column=1, padx=15, sticky="nsew")
        self.tat_hero_card.pack_propagate(False)
        
        tat_accent = ctk.CTkFrame(self.tat_hero_card, width=6, fg_color="#16A085", corner_radius=0)
        tat_accent.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.tat_hero_card, text="AVERAGE TURNAROUND TIME", font=("Arial", 11, "bold"), text_color="#A0A0A0").pack(anchor="w", padx=20, pady=(12, 0))
        self.tat_hero_val = ctk.CTkLabel(self.tat_hero_card, text="0.00 ms", font=("Arial", 26, "bold"), text_color="#16A085")
        self.tat_hero_val.pack(side="left", anchor="w", padx=20, pady=(0, 10))
        self.tat_hero_status = ctk.CTkLabel(self.tat_hero_card, text="— No Workload", font=("Arial", 11, "italic"), text_color="#666666")
        self.tat_hero_status.pack(side="right", anchor="e", padx=20, pady=(0, 15))


        self.chart_frame = ctk.CTkFrame(center)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=15)

    def _setup_right_panel(self, parent):

        right = ctk.CTkFrame(parent, width=340, fg_color="#1a1a1a")
        right.pack(side="right", fill="y", padx=10, pady=10)
        right.pack_propagate(False)

        ctk.CTkLabel(
            right,
            text="LIVE DASHBOARD",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 15))

        self.metrics_scroll = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.metrics_scroll.pack(fill="both", expand=True, padx=15, pady=5)

        self.create_dashboard_cards()

        ctk.CTkButton(
            right,
            text="ABOUT US",
            height=40,
            command=self.about_us
        ).pack(side="bottom", pady=20, padx=20, fill="x")

    def create_dashboard_cards(self):

        metrics_meta = [
            ("exec_time", "TOTAL EXECUTION", "0ms", "#3498DB"),
            ("proc_count", "TOTAL PROCESSES", "0", "#9B59B6"),
            ("avg_wt", "AVG WAITING TIME", "0.00 ms", "#F39C12"),      
            ("avg_tat", "AVG TURNAROUND TIME", "0.00 ms", "#16A085"),   
            ("cpu_status", "CPU STATUS", "IDLE", "#E74C3C"),
            ("sched_status", "SCHEDULER STATUS", "READY", "#2ECC71")
        ]
        
        for key, label, default, accent_color in metrics_meta:
            card = ctk.CTkFrame(self.metrics_scroll, height=85, corner_radius=10)
            card.pack(fill="x", pady=8, padx=5)
            card.pack_propagate(False)
            
            accent = ctk.CTkFrame(card, width=5, fg_color=accent_color, corner_radius=0)
            accent.pack(side="left", fill="y")
            
            lbl = ctk.CTkLabel(card, text=label, font=("Arial", 11, "bold"), text_color="#A0A0A0")
            lbl.pack(anchor="w", padx=15, pady=(10, 2))
            
            val = ctk.CTkLabel(card, text=default, font=("Arial", 20, "bold"))
            val.pack(anchor="w", padx=15, pady=(0, 5))
            
            self.metric_cards[key] = {"val_lbl": val, "frame": card, "accent": accent}

    def toggle_theme(self):

        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "Dark" else "dark")

    def add_process(self):

        try:
            p = (
                self.pid.get(),
                int(self.at.get()),
                int(self.bt.get()),
                int(self.pr.get())
            )
            if not p[0] or p[1] < 0 or p[2] <= 0:
                raise ValueError
            self.processes.append(p)
            self.tree.insert("", "end", values=p)

            self.pid.delete(0, "end")
            self.at.delete(0, "end")
            self.bt.delete(0, "end")
            self.pr.delete(0, "end")
            
            self.metric_cards["proc_count"]["val_lbl"].configure(text=str(len(self.processes)))
        except ValueError:
            messagebox.showerror("Error", "Invalid Input. Ensure metrics are positive numbers and ID is filled.")

    def reset_to_main_ui(self):
 
        self.processes.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.result_title_label.configure(text="ACTIVE ALGORITHM: NONE")
        

        self.wt_hero_val.configure(text="0.00 ms")
        self.tat_hero_val.configure(text="0.00 ms")
        self.wt_hero_status.configure(text="— No Workload", text_color="#666666")
        self.tat_hero_status.configure(text="— No Workload", text_color="#666666")
        
        self.metric_cards["exec_time"]["val_lbl"].configure(text="0ms")
        self.metric_cards["proc_count"]["val_lbl"].configure(text="0")
        self.metric_cards["avg_wt"]["val_lbl"].configure(text="0.00 ms")
        self.metric_cards["avg_tat"]["val_lbl"].configure(text="0.00 ms")
        
        self.metric_cards["cpu_status"]["val_lbl"].configure(text="IDLE", text_color="#FFFFFF")
        self.metric_cards["cpu_status"]["accent"].configure(fg_color="#E74C3C")
        self.metric_cards["sched_status"]["val_lbl"].configure(text="READY")
        
        messagebox.showinfo("Simulation Status", "Simulation data has been fully cleared.")

    def smart_advisor(self):

        if not self.processes:
            messagebox.showwarning("Smart Advisor", "Please add some processes first before consulting the advisor!")
            return

        sim_results = {}
        
        #algo simulation
        fcfs_gantt = self._sim_non_preemptive(sorted(self.processes, key=lambda x: x[1]), criteria_idx=None)
        sim_results["FCFS"] = self._get_sim_metrics(fcfs_gantt)
        
        sjf_gantt = self._sim_non_preemptive(sorted(self.processes, key=lambda x: x[1]), criteria_idx=2)
        sim_results["SJF (Non-Preemptive)"] = self._get_sim_metrics(sjf_gantt)

        srtf_gantt = self._sim_preemptive(criteria_func=lambda x, rem: rem[x[0]])
        sim_results["SRTF (Preemptive SJF)"] = self._get_sim_metrics(srtf_gantt)
        
        try: q_val = int(self.quantum.get())
        except ValueError: q_val = 2
        rr_gantt = self._sim_round_robin(q_val)
        sim_results[f"Round Robin (q={q_val})"] = self._get_sim_metrics(rr_gantt)

        best_algo = min(sim_results.keys(), key=lambda k: sim_results[k]["avg_wt"])
        
        burst_times = [p[2] for p in self.processes]
        priorities = [p[3] for p in self.processes]
        avg_burst = sum(burst_times) / len(burst_times)
        max_burst = max(burst_times)
        burst_disparity = max_burst - min(burst_times)
        
        warnings = []
        if burst_disparity > 15 and best_algo.startswith("FCFS"):
            warnings.append("⚠️ Potential Convoy Effect identified due to high burst time variation.")
        if len(set(priorities)) > 1 and not best_algo.startswith("Priority"):
            warnings.append("💡 Manual Priority parameters detected, but other scheduling offers better processing metrics.")

        advisor_win = ctk.CTkToplevel(self.root)
        advisor_win.title("Smart Advisor Insights")
        advisor_win.geometry("580x620")
        advisor_win.transient(self.root)
        advisor_win.grab_set()
        
        ctk.CTkLabel(advisor_win, text="💡 SMART ADVISOR ANALYSIS", font=("Arial", 22, "bold"), text_color="#A334FA").pack(pady=15)
        
        stats_frame = ctk.CTkFrame(advisor_win)
        stats_frame.pack(fill="x", padx=25, pady=5)
        
        ctk.CTkLabel(stats_frame, text=f"• Total Process Count: {len(self.processes)}", font=("Arial", 13)).pack(anchor="w", padx=15, pady=3)
        ctk.CTkLabel(stats_frame, text=f"• Average Process Burst Time: {avg_burst:.2f} ms", font=("Arial", 13)).pack(anchor="w", padx=15, pady=3)
        ctk.CTkLabel(stats_frame, text=f"• Workload Disparity Index: {burst_disparity} ms", font=("Arial", 13)).pack(anchor="w", padx=15, pady=3)

        comp_frame = ctk.CTkLabel(advisor_win, text="SIMULATED BENCHMARKS (Sorted by efficiency):", font=("Arial", 12, "bold"))
        comp_frame.pack(anchor="w", padx=25, pady=(15, 5))
        
        table_container = ctk.CTkFrame(advisor_win, fg_color="#1E1E1E")
        table_container.pack(fill="x", padx=25, pady=5)
        
        sorted_variants = sorted(sim_results.items(), key=lambda x: x[1]["avg_wt"])
        for idx, (name, metrics) in enumerate(sorted_variants):
            row = ctk.CTkFrame(table_container, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=4)
            
            medal = "🏆 [Best]" if idx == 0 else "• "
            lbl_color = "#2ECC71" if idx == 0 else "#FFFFFF"
            
            ctk.CTkLabel(row, text=f"{medal} {name}", font=("Arial", 12, "bold"), text_color=lbl_color, width=200, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"Avg WT: {metrics['avg_wt']:.2f} ms", font=("Arial", 11), text_color="#A0A0A0", width=140, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"Avg TAT: {metrics['avg_tat']:.2f} ms", font=("Arial", 11), text_color="#A0A0A0", width=140, anchor="w").pack(side="left")

        rec_box = ctk.CTkFrame(advisor_win, border_width=2, border_color="#A334FA", fg_color="#251833")
        rec_box.pack(fill="both", expand=True, padx=25, pady=15)
        
        ctk.CTkLabel(rec_box, text=f"RECOMMENDED ALGORITHM: {best_algo.upper()}", font=("Arial", 14, "bold"), text_color="#A334FA").pack(pady=(10, 5))
        
        if "SRTF" in best_algo or "SJF" in best_algo:
            rationale = "Processing tasks by their shortest burst requirement minimizes queued waiting loops, mathematically minimizing overall average delay patterns."
        elif "Round Robin" in best_algo:
            rationale = "Time slicing prevents massive batch payloads from causing long execution bottlenecks (Convoy Effect), which treats mixed task systems equally."
        else:
            rationale = "Your processing units are uniformly structural. Sequential processing minimizes structural analytical overhead for scheduling management safely."
            
        if warnings:
            rationale += f"\n\n" + "\n".join(warnings)

        rat_lbl = ctk.CTkLabel(rec_box, text=rationale, font=("Arial", 12, "italic"), wraplength=480, justify="center")
        rat_lbl.pack(padx=15, pady=5)

        def apply_recommendation():
            advisor_win.destroy()
            if "FCFS" in best_algo: self.fcfs()
            elif "Non-Preemptive" in best_algo and "SJF" in best_algo: 
                self.mode_var.set("Non-Preemptive")
                self.sjf()
            elif "SRTF" in best_algo:
                self.mode_var.set("Preemptive")
                self.sjf()
            elif "Round Robin" in best_algo: self.round_robin()
            else: self.priority_sched()

        btn_apply = ctk.CTkButton(advisor_win, text=f"🚀 RUN {best_algo.upper()}", font=("Arial", 13, "bold"), fg_color="#2ECC71", hover_color="#27AE60", command=apply_recommendation)
        btn_apply.pack(pady=(0, 15))

    def _sim_non_preemptive(self, data, criteria_idx=None):
        ready_pool = list(data)
        time = 0
        gantt = []
        while ready_pool:
            available = [p for p in ready_pool if p[1] <= time]
            if not available:
                time = min(p[1] for p in ready_pool)
                available = [p for p in ready_pool if p[1] <= time]
            chosen = min(available, key=lambda x: (x[criteria_idx], x[1])) if criteria_idx is not None else min(available, key=lambda x: x[1])
            pid, at, bt, pr = chosen
            gantt.append((pid, time, time + bt))
            time += bt
            ready_pool.remove(chosen)
        return gantt

    def _sim_preemptive(self, criteria_func):
        pool = sorted(self.processes, key=lambda x: x[1])
        remaining = {p[0]: p[2] for p in pool}
        gantt, time, last_pid, block_start = [], 0, None, 0
        while True:
            available = [p for p in pool if p[1] <= time and remaining[p[0]] > 0]
            if not available:
                unfinished = [p for p in pool if remaining[p[0]] > 0]
                if not unfinished: break
                time = min(p[1] for p in unfinished)
                available = [p for p in pool if p[1] <= time and remaining[p[0]] > 0]
            chosen = min(available, key=lambda x: criteria_func(x, remaining))
            pid = chosen[0]
            if last_pid is not None and last_pid != pid:
                gantt.append((last_pid, block_start, time))
                block_start = time
            elif last_pid is None: block_start = time
            remaining[pid] -= 1
            time += 1
            last_pid = pid
            if remaining[pid] == 0:
                gantt.append((pid, block_start, time))
                last_pid = None
        compressed = []
        for pid, s, e in gantt:
            if compressed and compressed[-1][0] == pid and compressed[-1][2] == s: compressed[-1] = (pid, compressed[-1][1], e)
            else: compressed.append((pid, s, e))
        return compressed

    def _sim_round_robin(self, q):
        pool = sorted(self.processes, key=lambda x: x[1])
        queue = deque()
        remaining_bt = {p[0]: p[2] for p in pool}
        gantt, time, pool_idx = [], 0, 0
        while pool_idx < len(pool) and pool[pool_idx][1] <= time:
            queue.append(pool[pool_idx]); pool_idx += 1
        while queue or pool_idx < len(pool):
            if not queue and pool_idx < len(pool):
                time = pool[pool_idx][1]; queue.append(pool[pool_idx]); pool_idx += 1
            pid, at, bt, pr = queue.popleft()
            execute = min(q, remaining_bt[pid])
            gantt.append((pid, time, time + execute))
            time += execute
            remaining_bt[pid] -= execute
            while pool_idx < len(pool) and pool[pool_idx][1] <= time:
                queue.append(pool[pool_idx]); pool_idx += 1
            if remaining_bt[pid] > 0: queue.append((pid, at, bt, pr))
        return gantt

    def _get_sim_metrics(self, gantt):
        arrival_times = {p[0]: p[1] for p in self.processes}
        burst_times = {p[0]: p[2] for p in self.processes}
        end_times = {pid: end for pid, start, end in gantt}
        wt, tat = [], []
        for pid in arrival_times:
            ft = end_times.get(pid, 0)
            t_at = ft - arrival_times[pid]
            wt.append(max(0, t_at - burst_times[pid]))
            tat.append(max(0, t_at))
        return {"avg_wt": sum(wt)/len(wt) if wt else 0, "avg_tat": sum(tat)/len(tat) if tat else 0}

    def fcfs(self):
        if not self.processes: return
        data = sorted(self.processes, key=lambda x: x[1])
        self.run_non_preemptive(data, "FCFS", None)

    def sjf(self):
        if not self.processes: return
        if self.mode_var.get() == "Preemptive":
            self.run_preemptive("SJF (SRTF)", criteria_func=lambda x, rem: rem[x[0]])
        else:
            data = sorted(self.processes, key=lambda x: x[1])
            self.run_non_preemptive(data, "SJF Non-Preemptive", criteria_idx=2)

    def priority_sched(self):
        if not self.processes: return
        if self.mode_var.get() == "Preemptive":
            self.run_preemptive("Preemptive Priority", criteria_func=lambda x, rem: x[3])
        else:
            data = sorted(self.processes, key=lambda x: x[1])
            self.run_non_preemptive(data, "Non-Preemptive Priority", criteria_idx=3)

    def round_robin(self):
        if not self.processes: return
        try: q = int(self.quantum.get())
        except ValueError: q = 2
        gantt = self._sim_round_robin(q)
        arrival_times = {p[0]: p[1] for p in self.processes}
        burst_times = {p[0]: p[2] for p in self.processes}
        self.calculate_and_display_metrics(gantt, arrival_times, burst_times, f"Round Robin (q={q})")

    def run_non_preemptive(self, data, name, criteria_idx=None):
        gantt = self._sim_non_preemptive(data, criteria_idx)
        arrival_times = {p[0]: p[1] for p in self.processes}
        burst_times = {p[0]: p[2] for p in self.processes}
        self.calculate_and_display_metrics(gantt, arrival_times, burst_times, name)

    def run_preemptive(self, name, criteria_func):
        gantt = self._sim_preemptive(criteria_func)
        arrival_times = {p[0]: p[1] for p in self.processes}
        burst_times = {p[0]: p[2] for p in self.processes}
        self.calculate_and_display_metrics(gantt, arrival_times, burst_times, name)

    def calculate_and_display_metrics(self, gantt, arrival_times, burst_times, name):
        metrics = self._get_sim_metrics(gantt)
        avg_wt, avg_tat = metrics["avg_wt"], metrics["avg_tat"]

        self.result_title_label.configure(text=f"ACTIVE ALGORITHM: {name.upper()}")
        
        #ui
        self.wt_hero_val.configure(text=f"{avg_wt:.2f} ms")
        self.tat_hero_val.configure(text=f"{avg_tat:.2f} ms")

        if avg_wt == 0:
            wt_msg, wt_color = "✨ Zero Latency", "#2ECC71"
        elif avg_wt < 10:
            wt_msg, wt_color = "🟢 Highly Efficient", "#2ECC71"
        elif avg_wt < 25:
            wt_msg, wt_color = "🟡 Moderate Delay", "#F1C40F"
        else:
            wt_msg, wt_color = "🔴 High Waiting Overhead", "#E74C3C"

        if avg_tat < 15:
            tat_msg, tat_color = "🟢 Fast Turnaround", "#2ECC71"
        elif avg_tat < 35:
            tat_msg, tat_color = "🟡 Moderate Profile", "#F1C40F"
        else:
            tat_msg, tat_color = "🔴 Slow Completion Time", "#E74C3C"

        self.wt_hero_status.configure(text=wt_msg, text_color=wt_color)
        self.tat_hero_status.configure(text=tat_msg, text_color=tat_color)
        
        self.metric_cards["avg_wt"]["val_lbl"].configure(text=f"{avg_wt:.2f} ms")
        self.metric_cards["avg_tat"]["val_lbl"].configure(text=f"{avg_tat:.2f} ms")

        self.draw_chart(gantt)
        self.update_metrics(gantt)

    def draw_chart(self, gantt):
        if not gantt: return
        for widget in self.chart_frame.winfo_children(): widget.destroy()

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
            if duration <= 0: continue
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

        for spine in ["top", "right", "left", "bottom"]: ax.spines[spine].set_visible(False)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_metrics(self, gantt):
        if not gantt: return
        total_time = max(p[2] for p in gantt)

        self.metric_cards["exec_time"]["val_lbl"].configure(text=f"{total_time} ms")
        self.metric_cards["proc_count"]["val_lbl"].configure(text=str(len(self.processes)))
        
        self.metric_cards["cpu_status"]["val_lbl"].configure(text="ACTIVE", text_color="#2ECC71")
        self.metric_cards["cpu_status"]["accent"].configure(fg_color="#2ECC71")
        self.metric_cards["sched_status"]["val_lbl"].configure(text="SUCCESS")

    def about_us(self):
        messagebox.showinfo(
            "ABOUT US",
            "CPU Scheduling Simulator\n\n"
            "Project Manager - Patrick Erl Abellanosa\n"
            "Algorithm Engineer (core) - Gaius M. Bongat\n"
            "Algorithm Engineer (advanced) - JhonPaul Cancejo\n"
            "Smart Advisor Developer - Shaider Aron Dimayuga\n"
            "UI/UX Developer - Elijah Lugo\n"
            "Data Visualization Engineer - Arian Jay Narnola\n"
            "Quality Assurance Tester - Angela Quirimit\n"
            "Technical Writer - John michael Bayos\n"
            "Video Producer & Editor - Charlie Robas\n"
            "Lead Presenter - Frence Bea Barte / Mary Luxzary Villarosa\n\n"
            "Email: Group5@gmail.com"
        )


if __name__ == "__main__":
    SchedulerApp()
