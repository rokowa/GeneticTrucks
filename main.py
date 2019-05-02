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


def fitness_fct(sol, distances, nb_peoples) :
    """
    Fonction à minimiser
    Calcule la distance totale et le risque (y compris de la banque à la première commune
    et de la dernière commune à la banque)
    - sol : une solution : liste de 3 sous-liste contenant les numéros des communes visitées
        dans l'ordre. Indices de 0 à 18.
        Ne doit pas contenir l'indice de la banque (19) !!
    - distances : ndarray (numpy) 20x20 symétrique contenant les distances de maison communale
        à maison communale, la dernière ligne et la dernière colonne contiennent les distances de
        maison communales à la banque nationale
    - nb_peoples : liste de 19 élements contenant le nombre d'habitants de chaque commune
    Retourne un tuple (somme_distance, somme_risque)
    """
    dist = []
    risk = []
    money = []
    
    #on crée une liste contenent les indices des communes (0 à 18)
    non_visited = [x for x in range(len(nb_peoples))]
    
    for j in range(len(sol)) :
        bank_idx = distances.shape[0]-1
        #on rajoutte la banque à la fin de la liste pour éviter de devoir le faire manuellement
        #à la fin de la boucle
        truck = sol[j] + [bank_idx]
        size = len(truck)
        if(size > 1) :
            dist.append(0)
            risk.append(0)
            money.append(0)
            #on ajoute la distance de la banque (dernier indice) à la 1è commune
            dist[j] += distances[bank_idx,truck[0]]
            for i in range(size-1) :
                #on ajoute la distance de maison communale à maison communale
                #à la dernière itération ce sera la banque nationale
                dist[j] += distances[truck[i], truck[i+1]]
                if(i in non_visited) :
                    #on ajoute l'argent récupéré dans la commune i si elle n'a pas encore été visitée
                    #on s'épargne le facteur 70 centimes qui est inutile
                    money[j] += nb_peoples[truck[i]]
                    non_visited.remove(i)
                #on ajoute le risque qui est modélisé comme la distance TOTALE pondérée par
                #l'argent transporté EN COURS DE TRAJET
                risk[j] += money[j]*dist[j]
        else :
            #on ne devrait pas se retrouver ici (cas où un camion ne visite aucune commune)
            pass
    
    if(len(non_visited) > 0) :
        #une des communes n'a pas été visitée.. on a donc évalué une solution non admissible
        #on ne devrait jamais se trouver ici
        print("Paaaaas bon")

    return (sum(dist), sum(risk))

def is_admissible(sol, nb_peoples, most_populated, total_money) :
    """
    Les contraintes de l'énoncé sont :
    - à aucun moment un camion ne peut transporter +50% du montant total à réupérer
    - les trois communes les plus peuplés ne peuvent être visitées par un même camion
    A cela il faut rajouter :
    - toutes les communes doivent être visitées (les indices de 0 à nb_communes-1 doivent apparaitre au moins 1 fois
    """
    
    res = True
    #on crée une liste contenent les indices des communes (0 à 18)
    non_visited = [x for x in range(len(nb_peoples))]
    
    #pour éviter de faire le calcul à chaque itération
    half_total_money = total_money / 2
    
    for truck in sol :
        money = 0
        most_populated_visited = 0
        for i in truck :
            #on ajoute l'argent transporté par le camion
            money += nb_peoples[i]
            if(i in non_visited) :
                #si la commune n'a pas encore été visitée, on la retire de la liste
                non_visited.remove(i)
            if(i in most_populated) :
                #si la commune fait partie des 3 plus peuplées, on incrémente
                most_populated_visited += 1

            if(money > half_total_money or most_populated_visited > 2) :
                #si on transporte plus de la moitié de l'argent total ou qu'on visite plus
                #de deux des communes les plus peuplées, la solution n'est pas admissible
                res = False
            
            if(res == False) :
                break;
        if(res == False) :
            break;
    
    #si il reste des éléments, cela veut dire qu'une des communes n'est pas visitées,
    #la solution n'est pas admissible
    if(len(non_visited) > 0) :
        res = False

    return res;

def most_populated(nb) :
    s = sorted(nb, reverse=True)
    return [nb.index(s[0]), nb.index(s[1]), nb.index(s[2])]
