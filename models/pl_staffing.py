from gurobipy import Model, GRB

def solve_staffing(employees, projects, availability, needs, efficiency):
    """Résout le problème d'affectation optimale
    
    Args:
        employees: Liste des noms des employés
        projects: Liste des noms des projets
        availability: Dict {employé: heures_disponibles}
        needs: Dict {projet: heures_requises}
        efficiency: Dict {employé: {projet: coefficient_efficacité}}
    
    Returns:
        Tuple (assignations, valeur_objectif) ou (None, None) si pas de solution
    """
    model = Model("AffectationOptimale")
    
    # Variables de décision
    x = {(e, p): model.addVar(lb=0, name=f"x_{e}_{p}") 
         for e in employees for p in projects}
    
    # Fonction objectif
    model.setObjective(
        sum(efficiency[e][p] * x[e, p] for e in employees for p in projects),
        GRB.MAXIMIZE
    )
    
    # Contraintes
    for e in employees:
        model.addConstr(sum(x[e, p] for p in projects) <= availability[e])
    
    for p in projects:
        model.addConstr(sum(x[e, p] for e in employees) >= needs[p])
    
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        return (
            {(e, p): x[e, p].X for e in employees for p in projects if x[e, p].X > 1e-6},
            model.ObjVal
        )
    return None, None