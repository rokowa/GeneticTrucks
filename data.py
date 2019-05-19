import random
import numpy as np
import copy
import numpy as np

"""
    Authors: COUCHARD Darius, KOWALKSI Robin, DIANGALA Jonathan
    
    This file contains all Data structures and Data utilities used by our nsga2.py
    All the NSGA2 processes are coded in the "nsga2.py" file, except the calculation of the fitness score,
    and the genetic operations on chromosomes as selection, crossing and mutation.
    
    This Algorithm is directly based on the original NSGA2 Paper: https://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf
    Some differences in the selection, crossing and mutation are from another paper which uses the NSGA2 algorithm
    on a Transportation Specific problem as we have now:
    
    https://www.researchgate.net/publication/301567660_Analyzing_the_Performance_of_Mutation_Operators_to_solve_
    the_Fixed_Charge_Transportation_Problem?fbclid=IwAR0229rxXYjT5xOed8fL4_7Ngbpzsx1EuXwu_IxT1tIRxhvZKbjKoBZB4o4
    
"""


def printf(str):
    """
        Useful to print our data without a linebreak on each printf call
    """
    print(str, end=', ')


class Data:
    """
        Data object is initialised only once in our algorithm, it contains usefull informations for our fitness score
        and our solution validity such as population per city, distance between each and cities.

        The Data object is created by the DataLoader defined in this same file and called from nsga2.py
    """
    BN_IDX = 0 
    XL_IDX = 1
    UCCLE_IDX = 2
    ANDERLECHT_IDX = 3 
    JETTE_IDX = 4
    EVERE_IDX = 5 
    WSP_IDX = 6
    AUDERGHEM_IDX = 7
    BXL_IDX = 8
    ETBK_IDX = 9
    GANSHOREN_IDX = 10
    KOEKELBERG_IDX = 11
    SCHAERBEEK_IDX = 12 
    BSA_IDX = 13
    STG_IDX = 14
    MSJ_IDX = 15
    SJTN_IDX = 16
    WSL_IDX = 17
    FOREST_IDX = 18 
    WB_IDX = 19 
    SIZE = 20
    distances = [[0 for j in range(20)] for i in range(20)]

    MOST_POPULATED = [ANDERLECHT_IDX, BXL_IDX, SCHAERBEEK_IDX]
    MONEY_PER_HABITANT = 0.7

    def __init__(self):
        self.names = [] 
        self.latitudes = [] 
        self.longitudes = [] 
        self.nb_peoples = [] 

    def add_name(self, name):
        self.names.append(name)

    def add_latitude(self, latitude):
        self.latitudes.append(latitude)

    def add_longitude(self, longitude):
        self.longitudes.append(longitude)

    def add_nb_people(self, n):
        """ Appends the number of people of a city in our number of people list"""
        self.nb_peoples.append(n)

    def calculate_distance(self, i, j):
        """ Calculate the distance in meters between each cities from their longitude and latitude, as described on
            this page here: https://www.movable-type.co.uk/scripts/latlong.html"""
        R_earth = 6378137 
        latA = self.latitudes[i]*np.pi/180
        latB = self.latitudes[j]*np.pi/180
        dlong = np.abs((self.longitudes[j]-self.longitudes[i])*np.pi/180)
        d = R_earth*np.arccos(np.sin(latA)*np.sin(latB)+np.cos(latA)*np.cos(latB)*np.cos(dlong))
        return d

    def init_distances(self):
        """ Initialises the distance table for each cities """
        for i in range(self.SIZE):
            for j in range(i+1, self.SIZE):
                d = self.calculate_distance(i, j)
                self.distances[i][j] = d 
                self.distances[j][i] = d 

    def show(self):
        """ Prints the values of the Data object """
        print('\nnames: [%s]' % ', '.join(map(str, self.names)))
        print('\nlatitudes: [%s]' % ', '.join(map(str, self.latitudes)))
        print('\nlongitudes: [%s]' % ', '.join(map(str, self.longitudes)))
        print('\nnb_peoples: [%s]' % ', '.join(map(str, self.nb_peoples)))
        print(np.matrix(self.distances))


class DataLoader:

    """
        Class to load the data we use in our Algorithm.
        The data can be the distance between cities (communes), the population of each city and an initial
        population encoded in a txt file (But this one is not used in standard usage)
    """

    def __init__(self, filename):
        """ Loads the distance between cities and the population on each city, sets those values
            in the created Data object"""
        self.data = Data()
        file_o = open(filename, 'r')
        for l in file_o.readlines() :
            words = l.split(" ")
            if words[0] == "Banque":
                self.data.add_name(words[0])
                self.data.add_nb_people(0)  # fancy entry for bank
                self.data.add_latitude(float(words[1]))
                self.data.add_longitude(float(words[2]))
            else:
                self.data.add_name(words[0])
                self.data.add_nb_people(int(words[3]))
                self.data.add_latitude(float(words[1]))
                self.data.add_longitude(float(words[2]))
        file_o.close()
        self.data.init_distances()

    def get_initial_pop(self, filename):
        """
        Loads the initial population from the specifies text file
        (It is not used in our case as we generate random populations every time but has been used
        for testing purposes """

        population = []
        file_o = open(filename, 'r')
        temp_chromosome = Chromosome(self.data)
        truck_index = 0
        for index, l in enumerate(file_o.readlines()):
            if l == "----------------------------------------------------\n":
                if index != 0:
                    population.append(temp_chromosome)
                    temp_chromosome = Chromosome(self.data)
                    truck_index = 0
                continue
            l = l.replace('\n', '')
            cities = l.split(', ')
            for city in cities:
                temp_chromosome.add_city(int(city), truck_index)
            truck_index += 1
            temp_chromosome.init_fitness_score()
        return population


class Chromosome:
    """
        Chromosome class, this is the data structure for the NSGA2 Algorithm's solutions
        Most function are to get the fitness score of a solution, genetically cross or mutate a solution, or modify
        the solution during our solutions generation processes
    """
    SIZE = 20
    H = -1

    def __init__(self, data):
        self.data = data
        self.risk = 0

        self.total_distance = [0, 0, 0]
        self.carried_money = [0, 0, 0]
        self.total_risk = [0, 0, 0]

        self.holes0 = [] 
        self.holes1 = [] 
        self.holes2 = [] 

        self.new_holes0 = [] 
        self.new_holes1 = [] 
        self.new_holes2 = [] 
        # c1 = 1 si la commune 1 a été visitée
        self.visited0 = [0 for i in range(self.SIZE)]
        self.visited1 = [0 for i in range(self.SIZE)]  
        self.visited2 = [0 for i in range(self.SIZE)]  
        # ordre dans lequel les neuds sont visités
        # les entrées vont de -1 (un trou), 0 (la banque), ... 19, 20
        # (la banque). Si le numero 8 se trouve dans la case 2 et
        # que 18 se trouve dans la case 1, cela veut dire
        # que la commune 18 a été visité avant la commune 8
        self.path0 = [-1 for i in range(self.SIZE)]
        self.path1 = [-1 for i in range(self.SIZE)]
        self.path2 = [-1 for i in range(self.SIZE)]

    def set_visited(self, city_idx, value, fourgon):
        """ Marks a city as visited, this is strictly related to our solution encoding method"""
        if city_idx >= self.SIZE:
            printf("set_visited: index trop grand: "+ str(city_idx))
        else:
            if fourgon == 0:
                self.visited0[city_idx] = 1 if value else 0 
            elif fourgon == 1:
                self.visited1[city_idx] = 1 if value else 0 
            elif fourgon == 2:
                self.visited2[city_idx] = 1 if value else 0 

    def find_non_free_idx(self, fourgon, inf, sup):
        """ Finds the first non free index of a Truck, this is strictly related to our solution encoding method"""
        found = False
        i = inf-1
        if fourgon == 0:
            while i < sup and not found:
                found = False if (self.path0[i] == -1) else True
                i += 1
        elif fourgon == 1:
            while i < sup and not found:
                found = False if (self.path1[i] == -1) else True
                i += 1
        elif fourgon == 2:
            while i < sup and not found:
                found = False if (self.path2[i] == -1) else True
                i += 1
        return -1 if not found else i-1

    def find_free_idx(self, fourgon):
        """ Finds the first free index (-1) in a truck path, this is strictly related to our solution encoding method"""
        found = False
        i = 0
        if fourgon == 0:
            while i < self.SIZE and not found:
                found = True if (self.path0[i] == -1) else False
                i += 1
        elif fourgon == 1:
            while i < self.SIZE and not found:
                found = True if (self.path1[i] == -1) else False
                i += 1
        elif fourgon == 2:
            while i < self.SIZE and not found:
                found = True if (self.path2[i] == -1) else False
                i += 1
        return -1 if not found else i-1

    def add_city(self, city_idx, fourgon):
        """ Adds the city to the precised truck path"""
        if city_idx >= self.SIZE:
            printf("add_city: index trop grand: " + str(city_idx))
        else:
            i = self.find_free_idx(fourgon)
            if fourgon == 0:
                self.path0[i] = city_idx
                self.set_visited(city_idx, True, 0)
            elif fourgon == 1:
                self.path1[i] = city_idx
                self.set_visited(city_idx, True, 1)
            elif fourgon == 2:
                self.path2[i] = city_idx
                self.set_visited(city_idx, True, 2)

    def mutate(self):
        """ Mutation method we learned during lessons, not used anymore as a more adapted method
            exists for transportation problems"""
        # les deux barres verticales
        i = self.SIZE//3 - 1  # cad 6
        j = 2*self.SIZE//3 - 1  # cad 13
        for k in range(2):
            self.path0[i+k], self.path0[j-k] = self.path0[j-k], self.path0[i+k]
            self.path1[i+k], self.path1[j-k] = self.path1[j-k], self.path1[i+k]
            self.path2[i+k], self.path2[j-k] = self.path2[j-k], self.path2[i+k]
    
    def swap_mutation(self):
        """ Mutation method found in this paper, it is more adapted for transportation
            problems as we are facing here:
            https://www.researchgate.net/publication/301567660_Analyzing_the_Performance_of_Mutation_Operators_to_solve_
            the_Fixed_Charge_Transportation_Problem?fbclid=IwAR0229rxXYjT5xOed8fL4_7Ngbpzsx1EuXwu_IxT1tIRxhvZKbjKoBZB4o4
        """
        j = 0
        k = 0
        while j >= k:
            j = random.randint(0,19)
            k = random.randint(0,19)
        
        i = 0
        
        l_bak = 0
        c_bak = 0
        path_bak = None
        for path in [self.path0, self.path1, self.path2]:
            for l, c in enumerate(path):
                if c != -1:
                    if i == j:
                        l_bak = l
                        c_bak = c
                        path_bak = path
                    elif i == k:
                        path_bak[l_bak] = c
                        path[l] = c_bak
                        break
                    i += 1
            if i >= k:
                break

    def generate_holes(self):
        """ Function used by the crossing method"""
        count = 0
        res = []
        while count < 7:
            if count < 2:
                i = random.randint(0, self.SIZE//3-1)
            elif count < 5:
                i = random.randint(self.SIZE//3, 2*self.SIZE//3-1)
            elif count < 7:
                i = random.randint(2*self.SIZE//3, self.SIZE-1)
            if i not in res:
                res.append(i)
                count += 1
        return res
    
    def cancel(self, index, fourgon):
        """Function used by the crossing method"""
        if fourgon == 0:
            self.path0[index] = -1
            self.set_visited(index, False, 0)
        elif fourgon == 1:
            self.path1[index] = -1
            self.set_visited(index, False, 1)
        elif fourgon == 2:
            self.path2[index] = -1
            self.set_visited(index, False, 2)

    def create_holes(self):
        """ Function used by the crossing method"""
        self.holes0 = self.generate_holes()
        self.holes1 = self.generate_holes()
        self.holes2 = self.generate_holes()
        for element in self.holes0:
            self.cancel(element, 0)
        for element in self.holes1:
            self.cancel(element, 1)
        for element in self.holes2:
            self.cancel(element, 2)

    def move_holes(self):
        """ Function used by the crossing method"""
        for i in self.holes0:
            j = self.find_non_free_idx(0, self.SIZE//3, 2*self.SIZE//3 - 1)
            self.path0[i], self.path0[j] = self.path0[j], self.path0[i]  

        for i in self.holes1:
            j = self.find_non_free_idx(1, self.SIZE//3, 2*self.SIZE//3 - 1)
            self.path1[i], self.path1[j] = self.path1[j], self.path1[i]  

        for i in self.holes0:
            j = self.find_non_free_idx(2, self.SIZE//3, 2*self.SIZE//3 - 1)
            self.path2[i], self.path2[j] = self.path2[j], self.path2[i]  

    def fill_holes(self, chromosome):
        """ Function used by the crossing method"""
        for i in range(self.SIZE//3-1, 2*self.SIZE//3-1):
            self.path0[i] = chromosome.path0[i]
            if chromosome.path0[i] == -1:
                self.set_visited(self.path0[i], False, 0)
            else:
                self.set_visited(self.path0[i], True, 0)
                
            self.path1[i] = chromosome.path1[i]
            if chromosome.path1[i] == -1:
                self.set_visited(self.path1[i], False, 1)
            else:
                self.set_visited(self.path1[i], True, 1)

            self.path2[i] = chromosome.path2[i]
            if chromosome.path2[i] == -1:
                self.set_visited(self.path2[i], False, 2)
            else:
                self.set_visited(self.path2[i], True, 2)

    def init_fitness_score(self):
        """ Calculates the score of the two function we need to minimize (found in the assignment)
            and sets the value to the Chromosome's class values"""
        self.total_distance = [0, 0, 0]
        self.carried_money = [0, 0, 0]
        self.total_risk = [0, 0, 0]
        clearPath0 = list(filter(lambda a: a != -1, self.path0))
        clearPath1 = list(filter(lambda a: a != -1, self.path1))
        clearPath2 = list(filter(lambda a: a != -1, self.path2))
        clearPath = []
        clearPath.append(clearPath0)
        clearPath.append(clearPath1)
        clearPath.append(clearPath2)
        for index, j in enumerate(clearPath):
            # We add the distance between the bank and the first city
            if len(j) > 0:
                self.total_distance[index] += self.data.distances[0][j[0]]
            for i in range(len(j)):
                # Si on arrive au bout de la liste
                self.carried_money[index] += self.data.nb_peoples[j[i]]*0.7
                if i == len(j)-1:
                    # On ajoute la distance entre la denière commune et la banque
                    self.total_distance[index] += self.data.distances[j[i]][0]
                    self.total_risk[index] += self.data.distances[j[i]][0]*self.carried_money[index]
                    break
                self.total_distance[index] += self.data.distances[j[i]][j[i+1]]
                self.total_risk[index] += self.data.distances[j[i]][j[i+1]]*self.carried_money[index]

    def get_fitness_score(self):
        """ Returns the pre-computed fitness score of the chromosome"""
        return sum(self.total_distance), sum(self.total_risk)

    def is_valid(self):
        """
        Checks if this chromosome respects the constraints defined in the assignment
        """
        total_money = sum(self.data.nb_peoples) * 0.7
        for truck in self.carried_money:
            # If one of the trucks containts more than 50% of the total money
            if truck > total_money * 0.5:
                return False
        # If one truck goes on the 3 most populated cities
        if 8 in self.path0 and 3 in self.path0 and 12 in self.path0:
            return False
        if 8 in self.path1 and 3 in self.path1 and 12 in self.path1:
            return False
        if 8 in self.path2 and 3 in self.path2 and 12 in self.path2:
            return False
        
        non_visited = [x for x in range(1,20)]
        for c in self.path0 + self.path1 + self.path2 :
            if c in non_visited:
                non_visited.remove(c)
                if len(non_visited) == 0:
                    break
        
        if len(non_visited) > 0:
            return False
        
        # If everything is good
        return True

    def cross(self, chromosome):
        """ Crossing method we learned during lessons, not used anymore"""
        child_left = copy.deepcopy(chromosome)
        child_left.create_holes()
        child_left.move_holes()
        child_left.fill_holes(self)

        child_right = copy.deepcopy(self)
        child_right.create_holes()
        child_right.move_holes()
        child_right.fill_holes(chromosome)

        return [child_left, child_right]
    
    def ipx_cross(self, chromosome_origin):
        """ Crossing method found in this paper, it is more adapted for transportation
            problems as we are facing here:
            https://www.researchgate.net/publication/301567660_Analyzing_the_Performance_of_Mutation_Operators_to_solve_
            the_Fixed_Charge_Transportation_Problem?fbclid=IwAR0229rxXYjT5xOed8fL4_7Ngbpzsx1EuXwu_IxT1tIRxhvZKbjKoBZB4o4
        """
        offspring = Chromosome(self.data)
        chromosome = copy.deepcopy(chromosome_origin)

        new_paths = [offspring.path0, offspring.path1, offspring.path2]
        paths1 = [self.path0, self.path1, self.path2]
        paths2 = [chromosome.path0, chromosome.path1, chromosome.path2]
        unused = []


        for k in range(3):
            unused.append([])
            for i, c in enumerate(paths1[k]):
                if random.random() < 0.5:
                    new_paths[k][i] = c
                    for j in range(len(paths2)):
                        if c in paths2[j]:
                            paths2[j].remove(c)
                else:
                    unused[k].append(i)

        for k in range(3):
            for i, c in enumerate(reversed(paths2[2-k])):
                if c != -1:
                    if i < len(unused[k]):
                        new_paths[k][unused[k][i]] = c
                    else:
                        new_paths[k][new_paths[k].index(-1)] = c
        
        return offspring

    def show(self):
        """ Prints the visited cities by each truck of the chromosome"""
        print("fourgon 0: {}".format(self.path0))
        print("fourgon 1: {}".format(self.path1))
        print("fourgon 2: {}".format(self.path2))
