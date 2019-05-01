print("Projet RO")

"""
La solution est une liste contenant trois autres listes.
Chaque liste représente les communes traversées par un
camion, marqués par leur indice

Exemple:
solution = [ [0, 5, 1,...,3], [2, 4, 7,...,1,0], [11, 18, 13,...,8] ]
"""

"""
Cette liste est un tableau qui indique la distance entre deux communes.
Par exemple, si Ixelles est d'indice 0 et Auderghem est d'indice 1, alors
la distance entre Ixelles et Auderghem sera obtenue par distance_sheet[0][1]
"""
distance_sheet = []


"""
Cette liste est un tableau d'une seule colonne qui indique le nombre
d'habitants par commune, elle permet de calculer le coût transporté
par les camions. Si Ixelles est d'indice 0, la population à Ixelles sera
obtenue par population_sheet[0]
"""
population_sheet = []


"""
Cette liste est un tableau d'une seule colonne qui indique les indices
des trois communes les plus larges
"""
biggest_districts = []

def minimize_path(solution):
	"""
	Première fonction à minimiser, elle se calcule en fesant 
	la somme de tous les chemins de tous les camions
	"""
