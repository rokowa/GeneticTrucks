import random
import copy
import numpy

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

    def get_distance(self, c1, c2):
        """ Calculates the distance between C1 and C2.
            C1 and C2 are the indexes """
        R_earth = 6378137
        lat1 = self.latitudes[c1]*np.pi/180
        lat2 = self.latitudes[c2]*np.pi/180
        dlong = np.abs((self.longitudes[c2]-self.longitudes[c1])*np.pi/180)
        d = R_earth*np_arccos(np.sin(lat1)*np.sin(lat2)+np.cos(lat1)*np.cos(lat2)*np.cos(dlong))
        return d

    def show(self):
        print('\nnames: [%s]' % ', '.join(map(str, self.names)))
        print('\nlatitudes: [%s]' % ', '.join(map(str, self.latitudes)))
        print('\nlongitudes: [%s]' % ', '.join(map(str, self.longitudes)))
        print('\nnb_peoples: [%s]' % ', '.join(map(str, self.nb_peoples)))


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


class Chromosome:
    SIZE = 21
    H = -1
    def __init__(self):
        self.distance = 0
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
        # les entrées vont de -1 (un trou), 0 (la banque), ... 19 
        # si le numero 8 se trouve dans la case 2 et 
        # que 18 se trouve dans la case 1, cela veut dire
        # que la commune 18 a été visité avant la commune 8
        self.path0 = [-1 for i in range(self.SIZE)]
        self.path1 = [-1 for i in range(self.SIZE)]
        self.path2 = [-1 for i in range(self.SIZE)]

    #TODO def get_risk(self):
    #TODO def get_distance(self):


    def set_visited(self, city_idx, value, fourgon):
        if(city_idx>=self.SIZE):
            printf("set_visited: index trop grand")
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
            printf("add_city: index trop grand")
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

    def fitness_fct(self):
        d

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


""" Uncomment to test """
"""
dataLoader = DataLoader("data_maison_com.txt")
data = dataLoader.data
data.show()

c = Chromosome()
d = Chromosome()

for i in range(10):
    c.add_city(i, 2)

for i in range(10,21):
    d.add_city(i, 2)

a, b = c.cross(d)
a.show()
b.show()
"""