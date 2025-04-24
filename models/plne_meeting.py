from gurobipy import Model, GRB

def solve_meeting_scheduling(meetings, timeslots, participants, availability):
    model = Model("PlanificationRéunions")
    model.setParam("OutputFlag", 0)

    # Variables : x[r, t] = 1 si réunion r est planifiée au créneau t
    x = {(r, t): model.addVar(vtype=GRB.BINARY, name=f"x_{r}_{t}")
         for r in meetings for t in timeslots}

    # Variables auxiliaires : z[p, t] = 1 si la personne p est assignée à une réunion à t
    z = {(p, t): model.addVar(vtype=GRB.BINARY, name=f"z_{p}_{t}")
         for p in participants for t in timeslots}

    # Chaque réunion a un seul créneau
    for r in meetings:
        model.addConstr(sum(x[r, t] for t in timeslots) == 1, name=f"one_slot_{r}")

    # Une personne ne peut être dans deux réunions à la fois
    for p in participants:
        for t in timeslots:
            model.addConstr(
                sum(x[r, t] for r in meetings if p in meetings[r]) <= 1,
                name=f"conflict_{p}_{t}"
            )

    # Contrainte de disponibilité : z[p,t] = 1 si p est dans une réunion à t
    for p in participants:
        for t in timeslots:
            model.addConstr(
                z[p, t] >= sum(x[r, t] for r in meetings if p in meetings[r]),
                name=f"assign_{p}_{t}"
            )
            # Respecter disponibilité
            if not availability.get(p, {}).get(t, True):
                model.addConstr(z[p, t] == 0, name=f"dispo_{p}_{t}")

    # Objectif : minimiser les conflits potentiels (nb de z[p,t] activés)
    model.setObjective(sum(z[p, t] for p in participants for t in timeslots), GRB.MINIMIZE)
    model.optimize()

    if model.status == GRB.OPTIMAL:
        schedule = {r: t for (r, t) in x if x[r, t].X > 0.5}
        return schedule, model.ObjVal
    else:
        return None, None


# Exemple d’appel
if __name__ == "__main__":
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

    schedule, score = solve_meeting_scheduling(meetings, timeslots, participants, availability)
    if schedule:
        print("Planning des réunions :")
        for r in schedule:
            print(f" - {r} → {schedule[r]}")
        print(f"Score objectif (nb d'assignations) : {score}")
    else:
        print("Aucune solution trouvée.")