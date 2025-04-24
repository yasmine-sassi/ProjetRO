# Problème 1 – Programmation Linéaire (PL) : Affectation de personnel à des projets

## Contexte

Une entreprise doit affecter ses employés à trois projets différents, chacun nécessitant un certain nombre d’heures.  
Chaque employé a une disponibilité horaire limitée et une efficacité (rendement) différente sur chaque projet.  
L’objectif est de maximiser l’efficacité globale de l’affectation.

### Données (exemple simplifié)

- **Employés :** E1, E2, E3
- **Projets :** P1, P2, P3
- **Disponibilité des employés :**
  - E1 : 40 h
  - E2 : 35 h
  - E3 : 30 h
- **Besoin en heures par projet :**
  - P1 : 50 h
  - P2 : 30 h
  - P3 : 25 h
- **Efficacité par heure :**

|        | P1  | P2  | P3  |
| ------ | --- | --- | --- |
| **E1** | 3   | 2   | 4   |
| **E2** | 2   | 3   | 1   |
| **E3** | 4   | 2   | 3   |

## Modélisation

### Variables

- \( x\_{ij} \) : nombre d’heures de l’employé \( i \) affectées au projet \( j \).

### Fonction objectif

Maximiser :

\[
Z = \sum*{i=1}^{3} \sum*{j=1}^{3} eff*{ij} \cdot x*{ij}
\]

où \( eff\_{ij} \) est l'efficacité de l'employé \( i \) sur le projet \( j \).

### Contraintes

1. **Pour chaque employé :** Total des heures affectées ≤ disponibilité de l'employé.
   \[
   \sum*{j=1}^{3} x*{ij} \leq \text{disponibilité de l'employé } i, \quad \forall i \in \{1, 2, 3\}
   \]

2. **Pour chaque projet :** La somme des heures affectées ≥ besoin du projet.
   \[
   \sum*{i=1}^{3} x*{ij} \geq \text{besoin du projet } j, \quad \forall j \in \{1, 2, 3\}
   \]

3. **Non-négativité :**
   \[
   x\_{ij} \geq 0, \quad \forall i \in \{1, 2, 3\}, \forall j \in \{1, 2, 3\}
   \]

---

# Problème 2 – Programmation Linéaire Mixte (PLM) : Optimisation d’un planning de réunions

## Contexte

On souhaite planifier des réunions dans des créneaux horaires limités, en respectant la présence obligatoire de certains participants.  
Chaque réunion doit être attribuée à un créneau (1 seul) et une salle.  
Les salles ont des capacités et disponibilités.  
Certaines personnes ne peuvent pas assister à deux réunions en même temps.  
L’objectif est de maximiser le nombre de réunions organisées.

### Données (exemple simplifié)

- **Réunions :** R1, R2, R3
- **Créneaux horaires :** H1, H2
- **Salles :** S1 (10 pers.), S2 (5 pers.)
- **Nombre de participants par réunion :**
  - R1 : 6
  - R2 : 4
  - R3 : 7
- **Conflit :** Une même personne participe à R1 et R3 ⇒ R1 et R3 ne peuvent pas avoir lieu en même temps.
- **Disponibilité des salles :** Disponibles à tous les horaires.

## Modélisation

### Variables binaires

- \( x\_{r,h,s} \in \{0,1\} \) : 1 si la réunion \( r \) est planifiée au créneau \( h \) dans la salle \( s \), 0 sinon.

### Fonction objectif

Maximiser :

\[
Z = \sum*{r,h,s} x*{r,h,s}
\]

### Contraintes

1. **Une réunion ne peut être planifiée qu'une seule fois :**
   \[
   \sum*{h,s} x*{r,h,s} \leq 1, \quad \forall r \in \{1, 2, 3\}
   \]

2. **Une salle ne peut accueillir qu'une seule réunion à la fois :**
   \[
   \sum*{r} x*{r,h,s} \leq 1, \quad \forall h \in \{1, 2\}, \forall s \in \{S1, S2\}
   \]

3. **Conflit d’agenda :** R1 et R3 ne peuvent pas être planifiées en même temps.
   \[
   \sum*{s} x*{R1,h,s} + \sum*{s} x*{R3,h,s} \leq 1, \quad \forall h \in \{H1, H2\}
   \]

4. **Capacité des salles :** La capacité de la salle doit être supérieure ou égale au nombre de participants.
   \[
   \sum*{r} x*{r,h,s} \cdot \text{participants de } r \leq \text{capacité de la salle } s, \quad \forall h \in \{H1, H2\}, \forall s \in \{S1, S2\}
   \]

### Remarque :

- Les variables \( x\_{r,h,s} \) sont binaires, ce qui en fait un problème de programmation linéaire mixte (PLM).
