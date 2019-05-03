import random
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

    def show(self):
        print("names: ")
        for element in self.names:
            printf(element)
        print("\nlatitudes: ")
        for element in self.latitudes:
            printf(str(element))
        print("\nlongitudes: ")
        for element in self.longitudes:
            printf(str(element))
        print("\nnb_peoples: ")
        for element in self.nb_peoples:
            printf(str(element))
        printf("\n")


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

    def add_city(self, city_idx, fourgon):
        if(city_idx>=self.SIZE):
            printf("add_city: index trop grand")
        else:
            i = self.find_free_idx(fourgon)
            if(fourgon == 0):
                self.path0[i] = city_idx
            elif(fourgon == 1):
                self.path1[i] = city_idx
            elif(fourgon == 2):
                self.path2[i] = city_idx

    #mutation
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
        res = [-1 for i in range(self.SIZE)]
        # 4 H par partie donc 12
        while count < 12:
            if(count < 4):
                i = random.randint(0,self.SIZE//3-1)
            elif(count < 8):
                i = random.randint(0,2*self.SIZE//3-1)
            elif(count < 12):
                i = random.randint(0,self.SIZE-1)
            print(str(i))
            if( res[i] == -1 ):
                res[i] = i;
                count += 1
        # les cases avec -1 -> pas de trous
        # sinon la case contient l'index du trou
        print('[%s]' % ', '.join(map(str, res)))
        return res

    #TODO Faire en sorte de generer un nouvel objet plutot que de modifier 
    # self
    def apply_holes(self):
        #on introduit 4 trous par partie
        rdm_holes0 = self.generate_holes()
        rdm_holes1 = self.generate_holes()
        rdm_holes2 = self.generate_holes()
        for element in rdm_holes0:
            if(element != -1):
                self.path0[element] = -1
                self.visited0[element] = 0
        for element in rdm_holes1:
            if(element != -1):
                self.path1[element] = -1
                self.visited1[element] = 0
        for element in rdm_holes2:
            if(element != -1):
                self.path2[element] = -1
                self.visited2[element] = 0
        print('[%s]' % ', '.join(map(str, self.path2)))

    #crossover
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
    def cross(self, chromosome):
        self.apply_holes()



    def show(self):
        i = 0
        printf("\nfourgon 0: ")
        printf("\nvisited: ")
        for element in self.visited0:
            printf(str(i) + " : " + str(element))
            i+=1

        i = 0
        printf("\npath: ")
        for element in self.path0:
            printf(str(i) + " path0: " + str(element))
            i+=1

        printf("\nfourgon 1: ")
        printf("\nvisited: ")
        i = 0
        for element in self.visited1:
            printf(str(i) + " : " + str(element))
            i+=1

        i = 0
        printf("\npath: ")
        for element in self.path1:
            printf(str(i) + " : " + str(element))
            i+=1

        printf("\nfourgon 2: ")
        printf("\nvisited: ")
        i = 0
        for element in self.visited2:
            printf(str(i) + " : " + str(element))
            i+=1

        i = 0
        printf("\npath: ")
        for element in self.path2:
            printf(str(i) + " : " + str(element))
            i+=1


""" Uncomment to test """
#"""
dataLoader = DataLoader("data_maison_com.txt")
data = dataLoader.data
#data.show()

c = Chromosome()
#c.show()
c.set_visited(Data.BXL_IDX, True, 2)
#c.show()
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.add_city(Data.BXL_IDX, 2)
c.mutate()
c.apply_holes()
#c.show()
#"""


