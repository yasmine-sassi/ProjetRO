import tkinter as tk
from tkinter import messagebox, ttk
from models.pl_staffing import solve_pl_problem  # Le modèle PL sera défini dans un fichier séparé

def launch_pl_app():
    root = tk.Tk()
    root.title("Problème de Programmation Linéaire – PL")

    # Frame de saisie des données
    input_frame = tk.LabelFrame(root, text="Saisir les données", padx=10, pady=10)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Variables de décision
    tk.Label(input_frame, text="Variables de décision (séparées par des virgules) :").grid(row=0, column=0, sticky="w")
    decision_vars_entry = tk.Entry(input_frame, width=40)
    decision_vars_entry.grid(row=0, column=1)

    # Coefficients de la fonction objectif
    tk.Label(input_frame, text="Coefficients de la fonction objectif (séparés par des virgules) :").grid(row=1, column=0, sticky="w")
    objective_coeff_entry = tk.Entry(input_frame, width=40)
    objective_coeff_entry.grid(row=1, column=1)

    # Contraintes
    tk.Label(input_frame, text="Contraintes (format 'a1*x1 + a2*x2 <= b') :").grid(row=2, column=0, sticky="w")
    constraints_entry = tk.Entry(input_frame, width=40)
    constraints_entry.grid(row=2, column=1)

    # Zone de texte pour afficher les résultats
    result_text = tk.Text(root, height=15, width=60)
    result_text.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def solve():
        try:
            # Récupérer les données depuis les champs de saisie
            decision_vars = decision_vars_entry.get().split(",")
            objective_coeff = list(map(float, objective_coeff_entry.get().split(",")))
            constraints_str = constraints_entry.get().split(",")
            
            # Conversion des contraintes en format exploitable
            constraints = []
            for c in constraints_str:
                lhs, rhs = c.split("<=")
                lhs_coeffs = list(map(float, lhs.split("*")))
                rhs_value = float(rhs)
                constraints.append((lhs_coeffs, rhs_value))

            # Résolution du problème PL
            result, obj_value = solve_pl_problem(decision_vars, objective_coeff, constraints)

            result_text.delete(1.0, tk.END)  # Effacer les anciens résultats
            if result:
                for var, value in result.items():
                    result_text.insert(tk.END, f"{var} → {value:.2f}\n")
                result_text.insert(tk.END, f"\nValeur optimale de la fonction objectif : {obj_value:.2f}")
            else:
                result_text.insert(tk.END, "Aucune solution trouvée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul : {e}")

    # Bouton de lancement du calcul
    ttk.Button(root, text="Lancer le calcul", command=solve).grid(row=2, column=0, pady=10)

    root.mainloop()
