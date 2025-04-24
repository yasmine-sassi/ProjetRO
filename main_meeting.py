import tkinter as tk
from gui.meeting_gui import MeetingSchedulerApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Optimisation de Planning de Réunions")
    app = MeetingSchedulerApp(root)
    root.mainloop()