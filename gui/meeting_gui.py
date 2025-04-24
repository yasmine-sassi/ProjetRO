import tkinter as tk
from tkinter import messagebox, ttk
from models.plne_meeting import solve_meeting_scheduling

def launch_meeting_app():
    root = tk.Tk()
    root.title("Planification de Réunions – PLNE")

    # Données d'exemple
    meetings = {
        "Réunion1": ["Alice", "Bob"],
        "Réunion2": ["Bob", "Charlie"],
        "Réunion3": ["Alice", "Charlie"]
    }
    timeslots = ["9h", "10h", "11h"]
    participants = ["Alice", "Bob", "Charlie"]
    availability = {
        "Alice": {"9h": True, "10h": True, "11h": True},
        "Bob": {"9h": True, "10h": False, "11h": True},
        "Charlie": {"9h": True, "10h": True, "11h": True}
    }

    result_text = tk.Text(root, height=15, width=60)
    result_text.grid(row=2, column=0, columnspan=3, pady=10)

    def solve():
        try:
            result, obj = solve_meeting_scheduling(meetings, timeslots, participants, availability)
            result_text.delete(1.0, tk.END)
            if result:
                for r, t in result.items():
                    result_text.insert(tk.END, f"{r} → {t}\n")
                result_text.insert(tk.END, f"\nScore objectif : {obj:.2f}")
            else:
                result_text.insert(tk.END, "Aucune solution trouvée.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    ttk.Button(root, text="Résoudre", command=solve).grid(row=1, column=1, pady=5)
    root.mainloop()