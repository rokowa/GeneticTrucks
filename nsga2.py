"""

fast_nondominated_sort(P)
-------------------------
for each p in P                                         P : ensemble des solutions
    S_p = vide
    n_p = 0
    for each q in P
        if(p dominate q) :
            S_p = S_p union {q}
        else if(q dominate p) :
            n_p = n_p + 1
    if n_p = 0 :
        p_rank = 1
        F_1 = F_1 union {p}
i = 0
while F_i != vide :
    Q = vide
    for each p in F_i :
        for each q in S_p
            n_q = n_q - 1
            if n_q == 0 :
                q_rank = i + 1
                Q = Q union {q}
    i = i + 1
    F_i = Q

"dominate" ICI -> cette solution est meilleure ou égale cad (dans le cas d'une minimisation)
que chaque fonction objectif est égale ou inférieure
autrement dit : p domine q si il existe un objectif pour lequel p est meilleure sans dégrader les autres objectifs


crowding_distance_assignment(I)                         I : ensemble des solutions
-------------------------------
l = |I|                                                 l = nombre de solution
for each i, set I[i]_distance = 0                       init distance
for each objective m
    I = sort(I,m)                                       sort using objective value
    I[1]_distance = I[l]_distance = inf                 boundary point selected (why both ??)
    for i = 2 to (l-1)
        I[i]_distance = I[i]_distance + (I[i+1] - I[I-1])/(m_max_value-m_min_value)


domination operator
-------------------
dans la main loop !! (pas le même que plus haut)
i domine j si (rang i > rang j) ou ((rang i = rang j) et (distance i > distance j))


main loop
---------
R_t = P_t union Q_t
F = fast_nondominated_sort(R_t)                         F = [F_1, ...] tous les fronts
P_t+1 = vide and i = 1
until |P_t+1| + |F_i| <= N
    crowding_distance_assignment(F_i)
    P_t+1 = P_t+1 union F_i
    i = i + 1
sort(F_i, dominate)
P_t+1 = P_t+1 union F_i[1:(N-|P_t+1|)]
Q_t+1 = make_new_pop(P_t+1)                             "usual" selection, crossover and mutation (???)
t = t+1
"""

from data import DataLoader, Data, Chromosome
import random
import numpy as np

NBR_ITERATIONS = 10
MAX_SOLUTIONS = 30
MUTATION_CHANCE = 0.1

dataloader = DataLoader("data_maison_com.txt")
data = dataloader.data
data.init_distances()
best_chromosomes = []


def main(p, q, iteration):
    if iteration > NBR_ITERATIONS:
        return
    else:
        print("---------[Iteration {}]----------".format(iteration))
        solutions = p + q
        F = fast_non_dominated_sort(solutions)
        pplus = []
        i = 1
        while len(pplus) + len(F[i]) <= MAX_SOLUTIONS:
            F[i] = crowding_distance_assignment(F[i])
            pplus.extend(F[i])
            i += 1
        sorted(F[i], key=lambda x: x.get_fitness_score())
        pplus.extend(F[i][0:(MAX_SOLUTIONS - len(pplus))])
        qplus = make_new_pop(pplus)

        return main(pplus, qplus, iteration+1)


def make_new_pop(pplus):
    # Picks two random elements from a list, until there is 1 or 0 elements remaining
    # Couples are stored in couple_list
    couple_list = []

    new_chromosomes = []
    for i in len(pplus)/2:
        couple = random.sample(pplus, 2)
        couple_list.append(couple)
        pplus.remove(couple[0], couple[1])
    for couple in couple_list:
        (a, b) = couple[0].cross(couple[1])
        new_chromosomes.append(a)
        new_chromosomes.append(b)
    for chromosome in new_chromosomes:
        if random.random() < MUTATION_CHANCE:
            chromosome.mutate()
    return new_chromosomes


def rank_sort(F):
    for i in range(F):
        backward_index = i
        while True:
            if backward_index > 0:
                if F[backward_index].get_fitness_score() > F[backward_index-1].get_fitness_score():
                    F[backward_index], F[backward_index-1] = F[backward_index-1], F[backward_index]
                    backward_index -= 1
                    continue
            break
    return F


def dominate(s1, s2):
    """ Calculates if S1 dominates S2"""
    score1 = s1.get_fitness_score()
    score2 = s2.get_fitness_score()
    return False if (score1[0] > score2[0] or score1[1] > score2[1] or
                     (score1[0] == score2[0] and score1[1] == score2[1])) else True


def fast_non_dominated_sort(pop):
    """ Sorts the population, the best ones are the less dominated ones"""
    ranks = [0]*pop_size
    fronts = [[]]

    dominated = [[]]*pop_size
    dom_count = [0]*pop_size
    
    for i in range(pop_size):
        for j in range(pop_size):
            if dominate(pop[i], pop[j]):
                dominated[i].append(j)
            elif dominate(pop[j], pop[i]):
                dom_count[i] += 1
        if dom_count[i] == 0:
            ranks[i] = 0
            fronts[0].append(i)
    k = 0
    while len(fronts[k]) > 0:
        q = []
        for i in fronts[k]:
            for j in range(len(dominated)):
                dom_count[j] -= 1
                if dom_count[j] == 0:
                    ranks[j] = k + 1
                    q.append(j)
        k += 1
        fronts.append(q)
    
    f = [[pop[i] for i in f] for f in fronts]
    return f


def crowding_distance_assignment(pop_set):
    l = len(pop_set)
    crow_dist = [0]*l
    obj_values = np.empty(len(pop_set))

    for s in pop_set:
        obj_values.add(s.get_fitness_score)
        
    for i in range(2):
        sorted_idx = np.argsort(obj_values[:, i])
        
        min_value = obj_values[sorted_idx[0], i]
        max_value = obj_values[sorted_idx[l-1], i]
        crow_dist[sorted_idx[0]] = np.inf
        crow_dist[sorted_idx[l-1]] = np.inf
        for j in range(1, l-2):
            crow_dist[sorted_idx[j]] += (obj_values[sorted_idx[j-1], i] - obj_values[sorted_idx[j+1], i])/(max_value-min_value)
    
    return crow_dist


def initial_data_creator(nbrpopulation):
    initial_pop = []
    cities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13, 14, 15, 16, 17, 18, 19, 20]
    sets = int(len(cities) / nbrpopulation)

    for i in range(nbrpopulation):
        chromo = Chromosome(data)
        t1 = [cities.pop(random.randint(0, len(cities)-1)) for _ in range(sets)]
        for j in t1:
            chromo.add_city(j, 0)
        initial_pop.append(chromo)

    last_chromo = Chromosome(data)
    # Only remaining cities
    for u in cities:
        last_chromo.add_city(u)
    initial_pop.append(last_chromo)
    return initial_pop


initial_population = initial_data_creator(4)
main(initial_population, [], 1)