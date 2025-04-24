import tkinter as tk
from tkinter import messagebox, ttk
from models.plne_meeting import solve_meeting_scheduling

def launch_meeting_app():
    root = tk.Tk()
    root.title("Planification de Réunions – PLNE")

    # Frame de saisie des données
    input_frame = tk.LabelFrame(root, text="Saisir les données", padx=10, pady=10)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Participants
    tk.Label(input_frame, text="Participants (séparés par des virgules) :").grid(row=0, column=0, sticky="w")
    participants_entry = tk.Entry(input_frame, width=40)
    participants_entry.grid(row=0, column=1)

    # Réunions
    tk.Label(input_frame, text="Réunions (séparées par des virgules) :").grid(row=1, column=0, sticky="w")
    meetings_entry = tk.Entry(input_frame, width=40)
    meetings_entry.grid(row=1, column=1)

    # Créneaux horaires
    tk.Label(input_frame, text="Créneaux horaires (séparés par des virgules) :").grid(row=2, column=0, sticky="w")
    timeslots_entry = tk.Entry(input_frame, width=40)
    timeslots_entry.grid(row=2, column=1)

    # Disponibilités
    tk.Label(input_frame, text="Disponibilités (JSON ou format clé-valeur) :").grid(row=3, column=0, sticky="w")
    availability_entry = tk.Entry(input_frame, width=40)
    availability_entry.grid(row=3, column=1)

    # Zone de texte pour afficher les résultats
    result_text = tk.Text(root, height=15, width=60)
    result_text.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def solve():
        try:
            # Récupérer les données depuis les champs de saisie
            meetings = {m.strip(): participants_entry.get().split(",") for m in meetings_entry.get().split(",")}
            timeslots = timeslots_entry.get().split(",")
            participants = participants_entry.get().split(",")
            availability = eval(availability_entry.get())  # Utilisation d'eval pour interpréter la saisie JSON-like

            # Résolution du problème
            result, obj = solve_meeting_scheduling(meetings, timeslots, participants, availability)

            result_text.delete(1.0, tk.END)  # Effacer les anciens résultats
            if result:
                for r, t in result.items():
                    result_text.insert(tk.END, f"{r} → {t}\n")
                result_text.insert(tk.END, f"\nScore objectif : {obj:.2f}")
            else:
                result_text.insert(tk.END, "Aucune solution trouvée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul : {e}")

    # Bouton de lancement du calcul
    ttk.Button(root, text="Lancer le calcul", command=solve).grid(row=2, column=0, pady=10)

    root.mainloop()
