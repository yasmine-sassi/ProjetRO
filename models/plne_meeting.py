from gurobipy import Model, GRB

def solve_meeting_scheduling(meetings, timeslots, rooms, room_capacities, meeting_participants, conflicts):
    model = Model("PlanificationReunions")
    model.setParam("OutputFlag", 0)

    # Variables de décision
    x = model.addVars(
        [(r, h, s) for r in meetings for h in timeslots for s in rooms],
        vtype=GRB.BINARY,
        name="x"
    )

    # Objectif : maximiser le nombre de réunions planifiées
    model.setObjective(x.sum(), GRB.MAXIMIZE)

    # Contraintes
    # 1. Une réunion ne peut être planifiée qu'une seule fois
    model.addConstrs(
        (sum(x[r, h, s] for h in timeslots for s in rooms) <= 1 for r in meetings),
        name="single_assign"
    )

    # 2. Une salle ne peut accueillir qu'une réunion à la fois
    model.addConstrs(
        (sum(x[r, h, s] for r in meetings) <= 1 
        for h in timeslots for s in rooms),
        name="room_occupancy"
    )

    # 3. Gestion des conflits
    for conflict_group in conflicts:
        model.addConstrs(
            (sum(x[r, h, s] for r in conflict_group for s in rooms) <= 1 
            for h in timeslots),
            name=f"conflict_{'_'.join(conflict_group)}"
        )

    # 4. Respect des capacités des salles
    model.addConstrs(
        (sum(x[r, h, s] * meeting_participants[r] for r in meetings) <= room_capacities[s]
        for h in timeslots for s in rooms),
        name="capacity"
    )

    # Résolution
    model.optimize()

    if model.status == GRB.OPTIMAL:
        planning = []
        for r in meetings:
            for h in timeslots:
                for s in rooms:
                    if x[r, h, s].X > 0.5:
                        planning.append((r, h, s))
        return planning, len(planning)
    return None ,0