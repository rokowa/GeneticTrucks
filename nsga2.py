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
import matplotlib.pyplot as plt
import random
import numpy as np

# Parameters of the algorithm
INITIAL_POP = 20
MAX_SOLUTIONS = 50
NBR_ITERATIONS = 50
MUTATION_CHANCE = 0.1

dataloader = DataLoader("data_maison_com.txt")
data = dataloader.data
data.init_distances()
best_chromosomes = []
final_solution = []
iterations_solutions = []


def main(p, q, iteration):
    solutions = p + q
    iterations_solutions.append(solutions)
    if iteration > NBR_ITERATIONS:
        return p + q
    else:
        print("---------[Iteration {}]----------".format(iteration))
        print("Population size: {}".format(len(solutions)))
        F = fast_non_dominated_sort(solutions)
        pplus = []
        i = 0
        while len(pplus) + get_safe_f_size(F, i) <= MAX_SOLUTIONS and F[i]:
            F[i] = crowding_distance_assignment(F[i])
            pplus += F[i]
            i += 1
        sorted(F[i], key=lambda x: x.get_fitness_score())
        pplus += F[i][0:(MAX_SOLUTIONS - len(pplus))]
        qplus = make_new_pop(pplus)
        return main(pplus, qplus, iteration+1)


def get_safe_f_size(F, index):
    """ This is a solution simple trick for out problem in the while loop of main function
        If we are crossing the end of the list, we add a final empty front to F, the while
        loop will stop (check the second condition of the while loop) """
    if index < len(F):
        return len(F[index])
    else:
        F.append([])
        return 0


def make_new_pop(pplus):
    temp_pplus = pplus.copy()
    # Picks two random elements from a list, until there is 1 or 0 elements remaining
    # Couples are stored in couple_list
    couple_list = []

    new_chromosomes = []
    for i in range(int(len(temp_pplus) / 2)):
        couple = random.sample(temp_pplus, 2)
        couple_list.append(couple)
        temp_pplus.remove(couple[0])
        temp_pplus.remove(couple[1])
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
    ranks = {}  # Dictionary containing key: chromosome, value: it's rank value
    dominated = {}  # Dictionary containing key: chromosome, value: chromosomes dominated by the chromosome
    domination_count = {}  # Dictionary containing key: chromosome, value: number of chromosomes that dominate the key
                           # chromosome
    fronts = [[]]  # Fronts, at the first row there are all the chromosomes that are non dominated
    for index, chromosome in enumerate(pop):
        # Number of chromosomes that dominate chromosome
        domination_count[chromosome] = 0
        ranks[chromosome] = 0
        dominated[chromosome] = []
        for chromosome2 in pop:
            if dominate(chromosome, chromosome2):
                dominated[chromosome].append(chromosome2)
            elif dominate(chromosome2, chromosome):
                domination_count[chromosome] += 1
        if domination_count[chromosome] == 0:
            ranks[chromosome] = 1
            fronts[0].append(chromosome)

    i = 0
    # Not sure about this one
    while i < len(fronts):
        if not fronts[i]:
            break
        temp = []
        # For each chromosome in front i
        for chromosome in fronts[i]:
            # For each chromosome dominated by the chromosome we have on iteration
            for chromosome2 in dominated[chromosome]:
                domination_count[chromosome2] -= 1
                if domination_count[chromosome2] == 0:
                    ranks[chromosome2] += 1
                    temp.append(chromosome2)
        i += 1
        if temp:
            if i < len(fronts):
                fronts[i] += temp
            else:
                fronts.append(temp)

    return fronts


def crowding_distance_assignment(pop_set):
    """ Crowding distance calculation, the pop_set is only a front of the total population
        @:param a population set (a single front of the population)
        @:return returns the given front of chromosomes sorted by the crowding distance of each chromosome"""
    solution_nmbr = len(pop_set)
    distance = [0.0] * len(pop_set)  # List of float distance, the chromosomes are identified by index in this case
    for m in range(2):  # We iterate over the two chromosome fitness function values
        sorted(pop_set, key=lambda x: x.get_fitness_score()[m])  # we sort our pop_set by the m objective value
        max_value = pop_set[0].get_fitness_score()[m]  # Max fitness score of the current m objective
        min_value = pop_set[-1].get_fitness_score()[m]  # Min fitness score of the current m objective
        if (max_value == 0 and min_value == 0) or (max_value == min_value):  # Workaround, the max_value and the min_
                                                                             # value are equals, so we have to find
                                                                             # a solution to avoid DivideBy0 exception
            max_value = np.inf
            min_value = 0
        distance[0] = np.inf
        distance[-1] = np.inf
        for i in range(1, solution_nmbr - 1):
            distance[i] += (pop_set[i+1].get_fitness_score()[m] - pop_set[i-1].get_fitness_score()[m]) \
                           / (max_value - min_value)
    # We sort our list by the distance values
    joined_list = [[None, 0.0]]*len(pop_set)
    for i in range(len(pop_set)):
        joined_list[i] = [pop_set[i], distance[i]]
    sorted(joined_list, key=lambda x: x[1])
    # I know there a better way of doing that but i'm kinda by zip rn
    final_list = [item[0] for item in joined_list]
    return final_list


def initial_data_creator(nbrpopulation):
    initial_pop = []
    cities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    for i in range(nbrpopulation):
        # We do a copy so we don't change the cities array
        temp_cities = cities.copy()
        random.shuffle(temp_cities)
        chromo = Chromosome(data)
        for j in temp_cities:
            chromo.add_city(j, random.randint(0, random.randint(0, 2)))
        initial_pop.append(chromo)
    return initial_pop


initial_population = initial_data_creator(INITIAL_POP)
print(initial_population)

final_solution = main(initial_population, [], 1)

score_1_list = []
score_2_list = []

for chromosome in final_solution:
    score_1_list.append(chromosome.get_fitness_score()[0])
    score_2_list.append(chromosome.get_fitness_score()[1])


plt.style.use("ggplot")
fig = plt.scatter(score_1_list, score_2_list, s=8)
plt.xlabel("Distance")
plt.ylabel("Risk")
plt.show()

