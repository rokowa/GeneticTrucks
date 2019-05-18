"""
    Authors: COUCHARD Darius, KOWALKSI Robin, DIANGALA Jonathan

    Python implementation of NSGA2 Algorithm for the Brussels Transportation problem.
    This Algorithm is directly based on the original NSGA2 Paper: https://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf

    Various Data, Data structures and Data tools are from the file data.py
"""


from data import DataLoader, Chromosome
import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib.cm as cm
import pickle


# NSGA2 Algorithm Parameters
INITIAL_POP = 25
MAX_SOLUTIONS = 100
NBR_ITERATIONS = 50
MUTATION_CHANCE = 0.1

X_SCALE_QUOTA = 1.0
Y_SCALE_QUOTA = 1.0

dataloader = DataLoader("data_maison_com.txt")
data = dataloader.data
data.init_distances()
best_chromosomes = []
final_solution = []
iterations_solutions = []

population = []


def main(p, q, iteration):
    """ Recursive function, it will stop when the parameter NBR_ITERATIONS is reached.
        This the main loop explained in the report """
    global iterations_solutions
    solutions = p + q
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
        F[i] = sorted(F[i], key=lambda x: x.get_fitness_score())
        pplus += F[i][0:(MAX_SOLUTIONS - len(pplus))]
        qplus = make_new_pop(pplus)
        population.append(qplus)
        return main(pplus, qplus, iteration+1)


def get_safe_f_size(F, index):
    """ This is a solution simple trick for out problem in the while loop of main function
        If we going out of the bounds of the list, we add a final empty front to F, the while
        loop will stop (check the second condition of the while loop) """
    if index < len(F):
        return len(F[index])
    else:
        F.append([])
        return 0


def weighted_random_choice(chromosomes):
    """ Randomly picks a chromosome, the chromosome with the best fitness score are the most
        likely to be chosen """
    max = 0
    for c in chromosomes:
        risk, dist = c.get_fitness_score()
        max += risk*10**-6+dist
    pick = random.uniform(0, max)
    current = 0
    for c in chromosomes:
        risk, dist = c.get_fitness_score()
        current += risk+dist
        if current > pick:
            return c


def make_new_pop(pplus):
    """ Creates a new population set by crossing random selected chromosomes (selected by weighted_random_choice() )
        The chromosomes can be swap mutated, the chance is one of the algorithm parameters"""
    new_chromosomes = []
    
    while len(new_chromosomes) < MAX_SOLUTIONS:
        couple = (weighted_random_choice(pplus), weighted_random_choice(pplus))
        c1, c2 = couple[0].cross2(couple[1])
        if random.random() < MUTATION_CHANCE:
            c1.swap_mutation()
            c2.swap_mutation()
        c1.init_fitness_score()
        c2.init_fitness_score()
        if c1.is_valid():
            new_chromosomes.append(c1)
        if c2.is_valid():
            new_chromosomes.append(c2)
        else:
            pass
    print("New generated chromosomes: "+str(len(new_chromosomes)))
    return new_chromosomes


def dominate(s1, s2):
    """ Returns true if S1 dominates S2. S1 dominates S2 if S1 is better
    (it our case lower) in the two fitness functions """
    score1 = s1.get_fitness_score()
    score2 = s2.get_fitness_score()
    return False if (score1[0] > score2[0] or score1[1] > score2[1] or
                     (score1[0] == score2[0] and score1[1] == score2[1])) else True


def fast_non_dominated_sort(pop):
    """ Sorts the population, the best ones are the less dominated ones
        Returns a list of fronts, each front is a list of chromosomes the first front
        is the non-dominated front"""
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
    while len(fronts[i]) > 0:
        Q = []
        for chromosome in fronts[i]:
            for chromosome2 in dominated[chromosome]:
                domination_count[chromosome2] -= 1
                if domination_count[chromosome2] == 0:
                    ranks[chromosome2] = i + 1
                    Q.append(chromosome2)
        i += 1
        fronts.append(Q)

    return fronts


def crowding_distance_assignment(pop_set):
    """ Crowding distance calculation, the pop_set is only a front of the total population
        @:param a population set (a single front of the population)
        @:return returns the given front of chromosomes sorted by the crowding distance of each chromosome"""
    solution_nmbr = len(pop_set)
    distance = [0.0] * len(pop_set)  # List of float distance, the chromosomes are identified by index in this case
    for m in range(2):  # We iterate over the two chromosome fitness function values
        pop_set = sorted(pop_set, key=lambda x: x.get_fitness_score()[m])  # we sort our pop_set by the objective value
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
    joined_list = sorted(joined_list, key=lambda x: x[1])
    # I know there a better way of doing that but i'm kinda by zip rn
    final_list = [item[0] for item in joined_list]
    return final_list


def initial_data_creator(nbrpopulation):
    """ Randomly creates a initial population, the number of the generated chromosomes is nbrpopulation
        and each chromosome verifies our constraints"""
    initial_pop = []
    cities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    while len(initial_pop) < nbrpopulation:
        # We do a copy so we don't change the cities array
        temp_cities = cities.copy()
        random.shuffle(temp_cities)
        chromo = Chromosome(data)
        for j in temp_cities:
            chromo.add_city(j, random.randint(0, random.randint(0, 2)))
        chromo.init_fitness_score()
        if chromo.is_valid():
            initial_pop.append(chromo)
    for chromo in initial_pop:
        print("----------------------------------------------------")
        print(chromo.path0)
        print(chromo.path1)
        print(chromo.path2)
    return initial_pop


# Creates an iniital population, runs the algorithm and shows the fronts of the final solutions with matplotlib

# initial_population = initial_data_creator(INITIAL_POP)
initial_population = dataloader.get_initial_pop("initial_pop.txt")

population.append(initial_population)

final_solution = main(initial_population, [], 1)

# We sort our final solutions
final_solution_fronts = fast_non_dominated_sort(final_solution)

# We save our final solutions in a binary file.
# This will be used for another graph generator in the representation.py file.
saved_sol = open("saved_sol.bin", "wb")
pickle.dump(final_solution_fronts, saved_sol)
saved_sol.close()

# Sets the style of our plot
plt.style.use("ggplot")

# Puts the fronts with a different color in our graph
colors = cm.rainbow(np.linspace(0, 1, len(final_solution_fronts)))
for front, c in zip(final_solution_fronts, colors):
    score_1_list = []
    score_2_list = []
    # Sorts the results in each front so the front lines in the graph doesn't cross
    front = sorted(front, key=lambda chromosome: chromosome.get_fitness_score()[0])
    for chromosome in front:
        score_1_list.append(chromosome.get_fitness_score()[0])
        score_2_list.append(chromosome.get_fitness_score()[1])
    plt.plot(score_1_list, score_2_list, '-o', color=c)

# Sets axes labels
plt.xlabel("Distance")
plt.ylabel("Risk")
plt.show()
