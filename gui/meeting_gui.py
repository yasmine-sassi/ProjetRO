import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import ast

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))
from plne_meeting import solve_meeting_scheduling

def run_solver():
    try:
        participants = participants_entry.get().split(",")
        meetings = meetings_entry.get().split(",")
        timeslots = timeslots_entry.get().split(",")
        availability_input = availability_entry.get("1.0", tk.END).strip()
        availability = ast.literal_eval(availability_input)

        result = solve_meeting_scheduling(participants, meetings, timeslots, availability)

        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        for meeting, slot in result.items():
            result_text.insert(tk.END, f"📅 {meeting} → {slot}\n")
        result_text.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{e}")

# === Window Setup ===
root = tk.Tk()
root.title("🗓️ Planification de Réunions")
root.geometry("700x650")
root.configure(bg="#f0f4f8")

# Style Setup
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', font=("Helvetica", 12, 'bold'), background="#4CAF50", foreground="white", padding=10)
style.configure('TLabel', font=("Helvetica", 14), background="#f0f4f8", foreground="#333")

# Title Header
title = ttk.Label(root, text="🗓️ Planification de Réunions", font=("Helvetica", 20, "bold"),
                  anchor="center", background="#4CAF50", foreground="white")
title.pack(pady=20, fill="x")

# === Input Frame ===
input_frame = tk.Frame(root, bg="#f0f4f8", padx=20, pady=10)
input_frame.pack(pady=10, fill="x")

ttk.Label(input_frame, text="Participants (séparés par virgule) :").grid(row=0, column=0, sticky="w", padx=10, pady=5)
participants_entry = ttk.Entry(input_frame, width=50)
participants_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Réunions :").grid(row=1, column=0, sticky="w", padx=10, pady=5)
meetings_entry = ttk.Entry(input_frame, width=50)
meetings_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Créneaux horaires :").grid(row=2, column=0, sticky="w", padx=10, pady=5)
timeslots_entry = ttk.Entry(input_frame, width=50)
timeslots_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Disponibilités (dict Python) :").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
availability_entry = scrolledtext.ScrolledText(input_frame, height=6, width=48, font=("Helvetica", 12))
availability_entry.grid(row=3, column=1, padx=10, pady=5)

# === Button Frame ===
button_frame = tk.Frame(root, bg="#f0f4f8", padx=10, pady=10)
button_frame.pack(pady=20)

solve_btn = ttk.Button(button_frame, text="📌 Lancer la planification", command=run_solver)
solve_btn.grid(row=0, column=0, padx=15, pady=10)

# === Output Frame ===
output_frame = ttk.LabelFrame(root, text="", padding=10)
output_frame.pack(padx=10, pady=5, fill="both", expand=True)

output_label = ttk.Label(output_frame, text="Résultat", font=("Helvetica", 14, "bold"))
output_label.pack(pady=5)

result_text = scrolledtext.ScrolledText(output_frame, wrap="word", height=10, font=("Helvetica", 12), state='disabled')
result_text.pack(fill="both", expand=True)

root.mainloop()
