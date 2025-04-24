import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from pathlib import Path

# Configuration du chemin pour les imports
sys.path.append(str(Path(__file__).parent.parent))
from models.pl_staffing import solve_staffing

def run_solver():
    try:
        # Récupération des données
        employees = [e.strip() for e in employees_entry.get().split(",") if e.strip()]
        projects = [p.strip() for p in projects_entry.get().split(",") if p.strip()]
        
        # Parsing des disponibilités
        availability = {}
        for line in availability_entry.get("1.0", tk.END).strip().split("\n"):
            if ":" in line:
                emp, hours = line.split(":", 1)
                availability[emp.strip()] = float(hours.strip())
        
        # Parsing des besoins
        needs = {}
        for line in needs_entry.get("1.0", tk.END).strip().split("\n"):
            if ":" in line:
                proj, hours = line.split(":", 1)
                needs[proj.strip()] = float(hours.strip())
        
        # Matrice d'efficacité par défaut (1 pour tous)
        efficiency = {e: {p: 1.0 for p in projects} for e in employees}
        
        # Résolution
        assignments, total_eff = solve_staffing(employees, projects, availability, needs, efficiency)
        
        # Affichage des résultats
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        
        if assignments:
            result_text.insert(tk.END, f"⚡ Efficacité totale: {total_eff:.2f}\n\n")
            for (emp, proj), hours in assignments.items():
                result_text.insert(tk.END, f"🧑 {emp} → 🏗️ {proj}: {hours:.1f}h\n")
        else:
            result_text.insert(tk.END, "Aucune solution trouvée. Vérifiez les contraintes.")
            
        result_text.config(state='disabled')
    
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{e}")

# === Configuration de la fenêtre ===
root = tk.Tk()
root.title("👥 Affectation du Personnel")
root.geometry("800x700")
root.configure(bg="#f0f4f8")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', font=("Helvetica", 12, 'bold'), background="#4CAF50", foreground="white", padding=10)
style.configure('TLabel', font=("Helvetica", 14), background="#f0f4f8", foreground="#333")
style.configure('TText', font=("Helvetica", 12), padding=10)

# Titre
title = ttk.Label(root, text="👥 Affectation du Personnel", font=("Helvetica", 20, "bold"),
                 anchor="center", background="#4CAF50", foreground="white")
title.pack(pady=20, fill="x")

# === Cadre des entrées ===
input_frame = tk.Frame(root, bg="#f0f4f8", padx=20, pady=10)
input_frame.pack(pady=10, fill="x")

# Champs de saisie
ttk.Label(input_frame, text="Employés (séparés par virgule) :").grid(row=0, column=0, sticky="w", padx=10, pady=5)
employees_entry = ttk.Entry(input_frame, width=40)
employees_entry.grid(row=0, column=1, padx=10, pady=5)
employees_entry.insert(0, "E1, E2, E3")

ttk.Label(input_frame, text="Projets (séparés par virgule) :").grid(row=1, column=0, sticky="w", padx=10, pady=5)
projects_entry = ttk.Entry(input_frame, width=40)
projects_entry.grid(row=1, column=1, padx=10, pady=5)
projects_entry.insert(0, "P1, P2, P3")

ttk.Label(input_frame, text="Disponibilités (une par ligne, format 'nom:heures') :").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
availability_entry = scrolledtext.ScrolledText(input_frame, height=4, width=40, font=("Helvetica", 12))
availability_entry.grid(row=2, column=1, padx=10, pady=5)
availability_entry.insert(tk.END, "E1:40\nE2:35\nE3:30")

ttk.Label(input_frame, text="Besoins (une par ligne, format 'projet:heures') :").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
needs_entry = scrolledtext.ScrolledText(input_frame, height=3, width=40, font=("Helvetica", 12))
needs_entry.grid(row=3, column=1, padx=10, pady=5)
needs_entry.insert(tk.END, "P1:50\nP2:30\nP3:25")

# === Bouton ===
button_frame = tk.Frame(root, bg="#f0f4f8", padx=10, pady=10)
button_frame.pack(pady=20)

solve_btn = ttk.Button(button_frame, text="📌 Lancer l'optimisation", command=run_solver)
solve_btn.grid(row=0, column=0, padx=15, pady=10)

# === Résultats ===
output_frame = ttk.LabelFrame(root, text="", padding=10)
output_frame.pack(padx=10, pady=5, fill="both", expand=True)

output_label = ttk.Label(output_frame, text="Résultat", font=("Helvetica", 14, "bold"))
output_label.pack(pady=5)

result_text = scrolledtext.ScrolledText(output_frame, wrap="word", height=10, font=("Helvetica", 12), state='disabled')
result_text.pack(fill="both", expand=True)

root.mainloop()