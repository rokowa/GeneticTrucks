import random
import numpy as np
import copy
import numpy as np

def printf(str):
    print(str, end=', ')

class Data:
    BN_IDX = 0 
    XL_IDX = 1
    UCCLE_IDX = 2
    ANDERLECHT_IDX = 3 
    JETTE_IDX = 4
    EVERE_IDX = 5 
    WSP_IDX = 6
    AUDERGHEM_IDX = 7
    BXL_IDX = 8
    ETBK_IDX= 9
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
        self.nb_peoples.append(n)

    def calculate_distance(self, i, j):
        R_earth = 6378137 
        latA = self.latitudes[i]*np.pi/180
        latB = self.latitudes[j]*np.pi/180
        dlong = np.abs((self.longitudes[j]-self.longitudes[i])*np.pi/180)
        d = R_earth*np.arccos(np.sin(latA)*np.sin(latB)+np.cos(latA)*np.cos(latB)*np.cos(dlong))
        return d


    def init_distances(self):
        for i in range(self.SIZE):
            for j in range(i+1, self.SIZE):
                d = self.calculate_distance(i, j)
                self.distances[i][j] = d 
                self.distances[j][i] = d 

    def show(self):
        print('\nnames: [%s]' % ', '.join(map(str, self.names)))
        print('\nlatitudes: [%s]' % ', '.join(map(str, self.latitudes)))
        print('\nlongitudes: [%s]' % ', '.join(map(str, self.longitudes)))
        print('\nnb_peoples: [%s]' % ', '.join(map(str, self.nb_peoples)))
        print(np.matrix(self.distances))


class DataLoader:
    def __init__(self, filename) :
        self.data = Data()
        file_o = open(filename, 'r')
        for l in file_o.readlines() :
            words = l.split(" ")
            if(words[0] == "Banque") :
                self.data.add_name(words[0])
                self.data.add_nb_people(0)#fancy entry for bank
                self.data.add_latitude(float(words[1]))
                self.data.add_longitude(float(words[2]))
            else :
                self.data.add_name(words[0])
                self.data.add_nb_people(int(words[3]))
                self.data.add_latitude(float(words[1]))
                self.data.add_longitude(float(words[2]))
        file_o.close()
        self.data.init_distances()


class Chromosome:
    SIZE = 20
    H = -1
    def __init__(self, data):
        self.data = data
        self.risk = 0

        self.holes0 = [] 
        self.holes1 = [] 
        self.holes2 = [] 

        self.new_holes0 = [] 
        self.new_holes1 = [] 
        self.new_holes2 = [] 
        # [bank, c1, c2, ..., c19, bank]
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
        if(city_idx>=self.SIZE):
            printf("set_visited: index trop grand: "+ str(city_idx))
        else:
            if(fourgon == 0):
                self.visited0[city_idx] = 1 if value else 0 
            elif(fourgon == 1):
                self.visited1[city_idx] = 1 if value else 0 
            elif(fourgon == 2):
                self.visited2[city_idx] = 1 if value else 0 

    # cherche le premier index libre de la partie du milieu
    # qui ne soit pas un trou
    def find_non_free_idx(self,fourgon, inf, sup):
        found = False
        i = inf-1
        if(fourgon==0):
            while i < sup and not found:
                found = False if (self.path0[i]==-1) else True
                i+=1
        elif(fourgon==1):
            while i < sup and not found:
                found = False if (self.path1[i]==-1) else True 
                i+=1
        elif(fourgon==2):
            while i < sup and not found:
                found = False if (self.path2[i]==-1) else True 
                i+=1
        #print(str(i))
        #print('[%s]' % ', '.join(map(str, self.path2)))
        return -1 if not found else i-1

    # Cherche l'indexe du premier trou d'un chemin
    def find_free_idx(self,fourgon):
        found = False
        i = 0
        if(fourgon==0):
            while i < self.SIZE and not found:
                found = True if (self.path0[i]==-1) else False
                i+=1
        elif(fourgon==1):
            while i < self.SIZE and not found:
                found = True if (self.path1[i]==-1) else False
                i+=1
        elif(fourgon==2):
            while i < self.SIZE and not found:
                found = True if (self.path2[i]==-1) else False
                i+=1
        #print(str(i))
        #print('[%s]' % ', '.join(map(str, self.path2)))
        return -1 if not found else i-1

    # Rajoute une commune visitée à un fourgon, en cherchant
    # d'abord un trou puis en l'ajoutant aux communes visitées 
    def add_city(self, city_idx, fourgon):
        if(city_idx>=self.SIZE):
            printf("add_city: index trop grand: "+ str(city_idx))
        else:
            i = self.find_free_idx(fourgon)
            if(fourgon == 0):
                self.path0[i] = city_idx
                self.set_visited(city_idx, True, 0)
            elif(fourgon == 1):
                self.path1[i] = city_idx
                self.set_visited(city_idx, True, 1)
            elif(fourgon == 2):
                self.path2[i] = city_idx
                self.set_visited(city_idx, True, 2)

    # mutation
    # on doit tenter d'implémenter une mutation 
    # inversion comme montrée au cours:
    # A = 3 5 | 7 1 2 4 | 8 6 9
    # A'= 3 5 | 4 2 1 7 | 8 6 9
    def mutate(self):
        # les deux barres verticales
        i = self.SIZE//3 - 1 #cad 6
        j = 2*self.SIZE//3 - 1 #cad 13
        for k in range(2):
            self.path0[i+k], self.path0[j-k] = self.path0[j-k], self.path0[i+k]
            self.path1[i+k], self.path1[j-k] = self.path1[j-k], self.path1[i+k]
            self.path2[i+k], self.path2[j-k] = self.path2[j-k], self.path2[i+k]
    
    def generate_holes(self):
        count = 0
        res = []
        # 7 H au total:
        # 2 dans la partie 1, 2 dans la partie 3 et 3 au milieu
        while count < 7:
            if(count < 2):
                i = random.randint(0,self.SIZE//3-1)
            elif(count < 5):
                i = random.randint(self.SIZE//3, 2*self.SIZE//3-1)
            elif(count < 7):
                i = random.randint(2*self.SIZE//3, self.SIZE-1)
            #print(str(i))
            if( i not in res ):
                res.append(i);
                count += 1
        # les cases avec -1 -> pas de trous
        # sinon la case contient l'index du trou
        #print('[%s]' % ', '.join(map(str, res)))
        return res
    
    def cancel(self, index, fourgon):
        if(fourgon == 0):
            self.path0[index] = -1
            self.set_visited(index, False, 0)
        elif(fourgon == 1):
            self.path1[index] = -1
            self.set_visited(index, False, 1)
        elif(fourgon == 2):
            self.path2[index] = -1
            self.set_visited(index, False, 2)

    def create_holes(self):
        #on introduit 4 trous par partie
        self.holes0 = self.generate_holes()
        self.holes1 = self.generate_holes()
        self.holes2 = self.generate_holes()
        for element in self.holes0:
            self.cancel(element, 0)
        for element in self.holes1:
            self.cancel(element, 1)
        for element in self.holes2:
            self.cancel(element, 2)
        #print('[%s]' % ', '.join(map(str, self.path2)))

    # déplacer les trous dans la partie centrale
    def move_holes(self):
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

    def get_fitness_score(self):
        """ Those are the two functions we need to minimize """
        total_distance = [0, 0, 0]
        carried_money = [0, 0, 0]
        clearPath0 = list(filter(lambda a: a != -1, self.path0))
        clearPath1 = list(filter(lambda a: a != -1, self.path1))
        clearPath2 = list(filter(lambda a: a != -1, self.path2))
        clearPath = []
        clearPath.append(clearPath0)
        clearPath.append(clearPath1)
        clearPath.append(clearPath2)
        for index, j in enumerate(clearPath):
            for i in range(len(j)):
                # Si on arrive au bout de la liste
                carried_money[index] += self.data.nb_peoples[j[i]]
                if i == len(j)-1:
                    # On ajoute la distance entre la denière commune et la banque
                    total_distance[index] += self.data.distances[j[i]][0]
                    break
                total_distance[index] += self.data.distances[j[i]][j[i+1]]
        risk = (carried_money[0]*total_distance[0] + carried_money[1]*total_distance[1] + carried_money[2]*total_distance[2])*self.data.MONEY_PER_HABITANT
        return sum(total_distance), risk

    # crossover
    # on doit tenter d'implémenter un croisement 
    # comme montrée au cours:
    # A = 3 5 | 7 1 2 4 | 8 6 9
    # B = 1 9 | 2 3 4 6 | 8 7 5
    # on prépare B:
    # B = H 9 | H 3 H 6 | 8 H 5
    # on bouge les trous
    # B = 3 6 | H H H H | 8 5 9
    # on import la partie centrale de A
    # B'= 3 6 | 7 1 2 4 | 8 5 9
    # on trouve A' de façon similaire
    def cross(self, chromosome):
        child_left = copy.deepcopy(chromosome)
        child_left.create_holes()
        child_left.move_holes()
        child_left.fill_holes(self)

        child_right= copy.deepcopy(self)
        child_right.create_holes()
        child_right.move_holes()
        child_right.fill_holes(chromosome)

        return [child_left, child_right]

    def show(self):
        print("\nfourgon 0: ")
        print('\nvisited:\t [%s]' % ', '.join(map(str, self.visited0)))
        print('\npath:\t [%s]' % ', '.join(map(str, self.path0)))

        print("\nfourgon 1: ")
        print('\nvisited:\t [%s]' % ', '.join(map(str, self.visited1)))
        print('\npath:\t [%s]' % ', '.join(map(str, self.path1)))

        print("\nfourgon 2: ")
        print('\nvisited:\t [%s]' % ', '.join(map(str, self.visited2)))
        print('\npath:\t [%s]' % ', '.join(map(str, self.path2)))

class Population:
    INITIAL_SIZE = 100
    def __init__(self):
        self.chromosomes = []
        #s'initialise selon l'algo NSGA-II
        for i in range(100):
            c = Chromosome()
            # le point de départ des fourgons c'est la banque 
            c.add_city(Data.BN_IDX, 0) 
            c.add_city(Data.BN_IDX, 1) 
            c.add_city(Data.BN_IDX, 2) 
            # on remplit aléatoirement le reste
            for i in range(1,Chromosome.SIZE):
                # 3 fourgons
                for j in range(3):
                    #on ajoute une ville au fourgon j
                    rdm_city = random.randint(-1, Chromosome.SIZE-1)
                    c.add_city(rdm_city, j) 
            self.chromosomes.append(c)
    #TODO
    """ from stackoverflow:
    2) Chromosomes are sorted and put into fronts based on 
    Pareto Non dominated sets. Within a Pareto front, 
    the chromosomes are ranked based on euclidean between 
    solutions or I-dist (term used in NSGA-II) . 
    Generally, solutions which are far away (not crowded) 
    from other solutions are given a higher preference while selection. 
    This is done in order to make a diverse solution n set and avoid 
    a crowded solution set.

    3)The best N (population) chromosomes are picked from the current 
    population and put into a mating pool
    
    4)In the mating pool, tournament selection, cross over and mating is done.
    
    5)The mating pool and current population is combined. 
    The resulting set is sorted, and the best N chromosomes make 
    it into the new population.
    
    6)Go to step 2, unless maximum number of generations have been reached.
    
    7)The solution set is the highest ranked Pareto non dominated 
    set from the latest population.
    
    supplément:
    About the difference between steady-state GA and generational GA: 
        In generational replacement you create a whole new population 
        of the same size as the old one using only the genes in 
        the old population and then replace it as a whole. 
    In steady-state replacement you create just one new individual which 
    then replaces just one individual in the population. Steady-state 
    GAs usually converge faster, but they're less likely to find 
    the good local optima, because they do not explore 
    the fitness landscape as much as when using generational replacement. 
    It depends on the problem of course and sometimes you can choose 
    how much of the old generation you want to replace which 
    allows you to have some arbitrary scale between these two.
    """







""" Uncomment to test """

"""
dataLoader = DataLoader("data_maison_com.txt")
data = dataLoader.data
data.init_distances()
#data.show()

c = Chromosome(data)
d = Chromosome(data)

for i in range(10):
    c.add_city(i, 2)

for i in range(10, 20):
    d.add_city(i, 2)

a, b = c.cross(d)

c.show()
print("C chromosome score: {}".format(c.get_fitness_score(data)))

d.show()
print("D chromosome score: {}".format(d.get_fitness_score(data)))

a.show()
print("A chromosome score: {}".format(a.get_fitness_score(data)))

b.show()
print("B chromosome score: {}".format(b.get_fitness_score(data)))

"""