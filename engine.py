import customtkinter as ctk
from tkinter import ttk, messagebox


def toggle_theme(self):
    """Toggles interface application dark or light mode configurations."""
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if current == "Dark" else "dark")

def add_process(self):
        """Validates input fields and saves valid process configurations to state."""
        try:
            p = (
                self.pid.get(),
                int(self.at.get()),
                int(self.bt.get()),
                int(self.pr.get())
            )
            if not p[0]:
                raise ValueError
            self.processes.append(p)
            self.tree.insert("", "end", values=p)
            self.pid.delete(0, "end")
            self.at.delete(0, "end")
            self.bt.delete(0, "end")
            self.pr.delete(0, "end")
            
            self.metric_cards["proc_count"]["val_lbl"].configure(text=str(len(self.processes)))
        except ValueError:
            messagebox.showerror("Error", "Invalid Input. Ensure fields are filled correctly.")

def reset_to_main_ui(self):
        """Wipes simulation context, charts, tables, and resets tracking monitors."""
        self.processes.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.result_title_label.configure(text="ACTIVE ALGORITHM: NONE")
        self.center_metrics_label.configure(text="Avg Waiting Time: 0.00 ms  |  Avg Turnaround Time: 0.00 ms")
        
        self.metric_cards["exec_time"]["val_lbl"].configure(text="0ms")
        self.metric_cards["proc_count"]["val_lbl"].configure(text="0")
        self.metric_cards["avg_wt"]["val_lbl"].configure(text="0.00 ms")
        self.metric_cards["avg_tat"]["val_lbl"].configure(text="0.00 ms")
        
        self.metric_cards["cpu_status"]["val_lbl"].configure(text="IDLE", text_color="#FFFFFF")
        self.metric_cards["cpu_status"]["accent"].configure(fg_color="#E74C3C")
        self.metric_cards["sched_status"]["val_lbl"].configure(text="READY")
        
        messagebox.showinfo("Simulation Status", "Simulation data has been fully cleared.")

def smart_advisor(self):
        """Analyzes processing distributions and recommends optimal algorithms."""
        if not self.processes:
            messagebox.showwarning("Smart Advisor", "Please add some processes first before consulting the advisor!")
            return

        num_processes = len(self.processes)
        burst_times = [p[2] for p in self.processes]
        priorities = [p[3] for p in self.processes]
        
        avg_burst = sum(burst_times) / num_processes
        max_burst = max(burst_times)
        min_burst = min(burst_times)
        burst_variance = max_burst - min_burst
        
        has_distinct_priorities = len(set(priorities)) > 1

        if has_distinct_priorities:
            recommendation = "PRIORITY SCHEDULING"
            rationale = ("You have assigned explicit, varying priorities across your processes. "
                         "Executing them by structural weight ensures critical tasks finish first.")
        elif burst_variance > 10 and any(b > avg_burst * 1.5 for b in burst_times):
            recommendation = "ROUND ROBIN (RR)"
            rationale = ("Your workload suffers from significant length imbalances. A time-sliced mechanism "
                         "is critical here to prevent short processes from starving behind massive ones (Convoy Effect).")
        elif avg_burst <= 3 and max_burst <= 5 and burst_variance <= 2:
            recommendation = "FIRST-COME, FIRST-SERVED (FCFS)"
            rationale = ("Your processes are uniformly brief and tightly packed. A basic FIFO stack "
                         "delivers minimal system overhead without context-switching costs.")
        else:
            recommendation = "SHORTEST JOB FIRST (SJF)"
            rationale = ("For this distribution, processing the shortest burst times first "
                         "mathematically guarantees the minimized global average waiting time (WT).")

        advisor_msg = (
            f"💡 SMART ADVISOR INSIGHTS\n"
            f"-----------------------------------------\n"
            f"• Active Processes: {num_processes}\n"
            f"• Avg Burst Time: {avg_burst:.1f}ms\n"
            f"• Burst Disparity: {burst_variance}ms\n\n"
            f"RECOMMENDED ALGORITHM:\n👉 {recommendation}\n\n"
            f"WHY? \n{rationale}"
        )
        messagebox.showinfo("Smart Advisor", advisor_msg)