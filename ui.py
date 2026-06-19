import customtkinter as ctk
from tkinter import ttk, messagebox


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
        """Assembles the overall interface frames."""
        self._setup_top_bar()

        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self._setup_left_panel(container)
        self._setup_right_panel(container)
        self._setup_center_panel(container)

    def _setup_top_bar(self):
        """Top Header section with title and theme settings."""
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
        """Left side containing Process Inputs and Execution Mode controls."""
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
        """Center frame displaying tracking data and Gantt charts."""
        center = ctk.CTkFrame(parent)
        center.pack(side="left", fill="both", expand=False, padx=10, pady=10)

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
        self.result_title_label.pack(pady=(10, 2))
        
        self.center_metrics_label = ctk.CTkLabel(
            center,
            text="Avg Waiting Time: 0.00 ms  |  Avg Turnaround Time: 0.00 ms",
            font=("Arial", 13, "italic"),
            text_color="#A0A0A0"
        )
        self.center_metrics_label.pack(pady=(0, 10))

        self.chart_frame = ctk.CTkFrame(center)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=15)

    def _setup_right_panel(self, parent):
        """Right side panel housing statistical cards."""
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
        """Initializes structural card components inside the metrics scroll layout."""
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