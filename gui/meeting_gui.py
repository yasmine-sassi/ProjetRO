import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import sys

# Ajout du chemin pour importer depuis models
sys.path.append(str(Path(__file__).parent.parent))
from models.plne_meeting import solve_meeting_scheduling

class MeetingSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("🗓️ Planification de Réunions Avancée")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f4f8")

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('TButton', font=("Helvetica", 12, 'bold'), 
                           background="#4CAF50", foreground="white", padding=10)
        self.style.configure('TLabel', font=("Helvetica", 14), 
                           background="#f0f4f8", foreground="#333")

        # Titre
        title = ttk.Label(
            self.root, 
            text="🗓️ Planification de Réunions Avancée",
            font=("Helvetica", 20, "bold"),
            anchor="center",
            background="#4CAF50",
            foreground="white"
        )
        title.pack(pady=20, fill="x")

        # Cadre d'entrée
        self.create_input_frame()
        
        # Bouton
        self.create_button_frame()
        
        # Résultats
        self.create_result_frame()

    def create_input_frame(self):
        input_frame = ttk.Frame(self.root, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)

        # Réunions
        ttk.Label(input_frame, text="Réunions (séparées par virgule):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.meetings_entry = ttk.Entry(input_frame, width=50)
        self.meetings_entry.grid(row=0, column=1, padx=5, pady=5)
        self.meetings_entry.insert(0, "R1, R2, R3")

        # Créneaux
        ttk.Label(input_frame, text="Créneaux horaires (séparés par virgule):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.timeslots_entry = ttk.Entry(input_frame, width=50)
        self.timeslots_entry.grid(row=1, column=1, padx=5, pady=5)
        self.timeslots_entry.insert(0, "H1, H2")

        # Salles
        ttk.Label(input_frame, text="Salles (séparées par virgule):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.rooms_entry = ttk.Entry(input_frame, width=50)
        self.rooms_entry.grid(row=2, column=1, padx=5, pady=5)
        self.rooms_entry.insert(0, "S1, S2")

        # Capacités des salles
        ttk.Label(input_frame, text="Capacités des salles (une par ligne, 'salle:capacité'):").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.room_capacities_entry = scrolledtext.ScrolledText(input_frame, width=50, height=3)
        self.room_capacities_entry.grid(row=3, column=1, padx=5, pady=5)
        self.room_capacities_entry.insert(tk.END, "S1:10\nS2:5")

        # Participants par réunion
        ttk.Label(input_frame, text="Participants par réunion (une par ligne, 'réunion:nombre'):").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.participants_entry = scrolledtext.ScrolledText(input_frame, width=50, height=3)
        self.participants_entry.grid(row=4, column=1, padx=5, pady=5)
        self.participants_entry.insert(tk.END, "R1:6\nR2:4\nR3:7")

        # Conflits
        ttk.Label(input_frame, text="Conflits (une par ligne, réunions séparées par virgule):").grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.conflicts_entry = scrolledtext.ScrolledText(input_frame, width=50, height=3)
        self.conflicts_entry.grid(row=5, column=1, padx=5, pady=5)
        self.conflicts_entry.insert(tk.END, "R1,R3")

    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.solve_btn = ttk.Button(
            button_frame, 
            text="📌 Lancer l'optimisation",
            command=self.run_optimization
        )
        self.solve_btn.pack()

    def create_result_frame(self):
        result_frame = ttk.LabelFrame(self.root, text="Résultats", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame, 
            wrap=tk.WORD, 
            height=15, 
            font=("Helvetica", 12)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def parse_inputs(self):
        """Parse et valide toutes les entrées"""
        try:
            meetings = [m.strip() for m in self.meetings_entry.get().split(",") if m.strip()]
            timeslots = [t.strip() for t in self.timeslots_entry.get().split(",") if t.strip()]
            rooms = [r.strip() for r in self.rooms_entry.get().split(",") if r.strip()]
            
            if not meetings or not timeslots or not rooms:
                raise ValueError("Tous les champs doivent être remplis")
            
            # Parse capacités des salles
            room_capacities = {}
            for line in self.room_capacities_entry.get("1.0", tk.END).strip().split("\n"):
                if ":" in line:
                    room, cap = line.split(":", 1)
                    room_capacities[room.strip()] = int(cap.strip())
            
            # Parse participants par réunion
            meeting_participants = {}
            for line in self.participants_entry.get("1.0", tk.END).strip().split("\n"):
                if ":" in line:
                    meeting, parts = line.split(":", 1)
                    meeting_participants[meeting.strip()] = int(parts.strip())
            
            # Parse conflits
            conflicts = []
            for line in self.conflicts_entry.get("1.0", tk.END).strip().split("\n"):
                if line and "," in line:
                    conflicts.append([m.strip() for m in line.split(",")])
            
            return {
                "meetings": meetings,
                "timeslots": timeslots,
                "rooms": rooms,
                "room_capacities": room_capacities,
                "meeting_participants": meeting_participants,
                "conflicts": conflicts
            }
            
        except Exception as e:
            raise ValueError(f"Erreur dans les données d'entrée: {str(e)}")

    def run_optimization(self):
        """Lance l'optimisation et affiche les résultats"""
        try:
            inputs = self.parse_inputs()
            planning, nb_planned = solve_meeting_scheduling(**inputs)
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            if planning:
                self.result_text.insert(tk.END, "📅 Planning optimal des réunions :\n\n")
                
                # Organiser par créneau horaire
                planning_by_timeslot = {}
                for r, h, s in planning:
                    if h not in planning_by_timeslot:
                        planning_by_timeslot[h] = []
                    planning_by_timeslot[h].append((r, s))
                
                for h in inputs["timeslots"]:
                    if h in planning_by_timeslot:
                        self.result_text.insert(tk.END, f"🕒 Créneau {h} :\n")
                        for r, s in planning_by_timeslot[h]:
                            participants = inputs["meeting_participants"][r]
                            self.result_text.insert(tk.END, f"  - {r} en {s} ({participants} participants)\n")
                        self.result_text.insert(tk.END, "\n")
                
                self.result_text.insert(tk.END, f"  - {r} en {s} ({participants} participants)\n")
            else:
                self.result_text.insert(tk.END, "Aucune solution trouvée. Vérifiez les contraintes.")
            
            self.result_text.config(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")