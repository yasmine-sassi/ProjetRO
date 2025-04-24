import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Allow import from models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))
from pl_staffing import solve_staffing  # Adjust this if your function name differs

def run_solver():
    try:
        output = solve_staffing()  # Update with actual arguments if needed
        output_text.configure(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output)
        output_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Setup main window
root = tk.Tk()
root.title("Staffing Planner")
root.geometry("700x500")
root.configure(bg="#f0f4f8")

style = ttk.Style()
style.theme_use("clam")

# Configure style for widgets
style.configure('TButton', font=("Helvetica", 12, 'bold'), background="#4CAF50", foreground="white", padding=10)
style.configure('TLabel', font=("Helvetica", 14), background="#f0f4f8", foreground="#333")
style.configure('TText', font=("Helvetica", 12), padding=10)

# Top title
title = ttk.Label(root, text="👥 Staffing Planner", font=("Helvetica", 20, "bold"), anchor="center", background="#4CAF50", foreground="white")
title.pack(pady=20, fill="x")

# Frame for inputs (use tk.Frame instead of ttk.Frame for background color)
input_frame = tk.Frame(root, bg="#f0f4f8", padx=20, pady=10)
input_frame.pack(pady=10, fill="x")

# Input fields
ttk.Label(input_frame, text="Team Members (comma-separated):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
team_members_entry = ttk.Entry(input_frame, width=40)
team_members_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Tasks (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tasks_entry = ttk.Entry(input_frame, width=40)
tasks_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(input_frame, text="Availability (Python dict format):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
availability_entry = ttk.Entry(input_frame, width=40)
availability_entry.grid(row=2, column=1, padx=10, pady=5)

# Frame for button (use tk.Frame instead of ttk.Frame for background color)
button_frame = tk.Frame(root, bg="#f0f4f8", padx=10, pady=10)
button_frame.pack(pady=20)

solve_btn = ttk.Button(button_frame, text="Run Staffing", command=run_solver)
solve_btn.grid(row=0, column=0, padx=15, pady=10)

# Frame for output
output_frame = ttk.LabelFrame(root, text="", padding=10)
output_frame.pack(padx=10, pady=5, fill="both", expand=True)

# Label inside the LabelFrame for the "Output" text
output_label = ttk.Label(output_frame, text="Resultat", font=("Helvetica", 14, "bold"))
output_label.pack(pady=5)

# Output Text Area (Scrollable)
output_text = scrolledtext.ScrolledText(output_frame, wrap="word", height=10, font=("Helvetica", 12), state='disabled')
output_text.pack(fill="both", expand=True)

# Run the app
root.mainloop()
