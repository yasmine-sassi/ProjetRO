import tkinter as tk
from tkinter import ttk, messagebox
from models.pl_staffing import solve_staffing

def launch_app():
    root = tk.Tk()
    root.title("Optimisation – Affectation de Personnel")

    # Exemple de données par défaut
    employees = ["E1", "E2", "E3"]
    projects = ["P1", "P2", "P3"]

    availability = {"E1": 40, "E2": 35, "E3": 30}
    project_needs = {"P1": 50, "P2": 30, "P3": 25}
    efficiency = {
        "E1": {"P1": 3, "P2": 2, "P3": 4},
        "E2": {"P1": 2, "P2": 3, "P3": 1},
        "E3": {"P1": 4, "P2": 2, "P3": 3}
    }

    result_text = tk.Text(root, height=15, width=60)
    result_text.grid(row=6, column=0, columnspan=3, pady=10)

    def solve():
        try:
            result, obj = solve_staffing(efficiency, availability, project_needs)
            result_text.delete(1.0, tk.END)
            for (emp, proj), hours in result.items():
                result_text.insert(tk.END, f"{emp} → {proj} : {hours:.2f} h\n")
            result_text.insert(tk.END, f"\nEfficacité totale : {obj:.2f}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    ttk.Button(root, text="Résoudre", command=solve).grid(row=5, column=1, pady=5)
    root.mainloop()