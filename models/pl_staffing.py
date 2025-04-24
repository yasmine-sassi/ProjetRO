from gurobipy import Model, GRB

def solve_staffing(efficiency, availability, project_needs):
    model = Model("AffectationPersonnel")
    employees = list(efficiency.keys())
    projects = list(project_needs.keys())

    # Variables : heures que i passe sur j
    x = {
        (i, j): model.addVar(lb=0, name=f"x_{i}_{j}")
        for i in employees
        for j in projects
    }

    # Objectif : maximiser efficacité globale
    model.setObjective(
        sum(efficiency[i][j] * x[i, j] for i in employees for j in projects),
        GRB.MAXIMIZE
    )

    # Contraintes de disponibilité
    for i in employees:
        model.addConstr(sum(x[i, j] for j in projects) <= availability[i], name=f"disp_{i}")

    # Contraintes de besoin projet
    for j in projects:
        model.addConstr(sum(x[i, j] for i in employees) >= project_needs[j], name=f"need_{j}")

    model.optimize()

    result = {(i, j): x[i, j].X for i in employees for j in projects if x[i, j].X > 1e-6}
    return result, model.ObjVal