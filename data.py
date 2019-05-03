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
        self.path0 = [0 for i in range(-1, self.SIZE)]
        self.path1 = [0 for i in range(self.SIZE)]
        self.path2 = [0 for i in range(self.SIZE)]

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

    def add_city(self, city_idx, fourgon):
        if(city_idx>=self.SIZE):
            printf("add_city: index trop grand")
        else:
            if(fourgon == 0):
                self.path0.append(city_idx)
            elif(fourgon == 1):
                self.path1.append(city_idx)
            elif(fourgon == 2):
                self.path2.append(city_idx)

    #TODO mutation

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
data.show()

c = Chromosome()
c.show()
c.set_visited(Data.BXL_IDX, True, 2)
c.show()
c.add_city(Data.BXL_IDX, 2)
c.show()
#"""


