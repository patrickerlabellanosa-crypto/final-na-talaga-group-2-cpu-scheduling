from tkinter import ttk, messagebox
from ui import SchedulerApp


def about_us(self):
        """Displays credits modal for development group members."""
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