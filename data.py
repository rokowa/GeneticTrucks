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
        for element in self.names:
            print("names: " + element)
        print("\n")
        for element in self.latitudes:
            print("latitudes: " + str(element))
        print("\n")
        for element in self.longitudes:
            print("longitudes: " + str(element))
        print("\n")
        for element in self.nb_peoples:
            print("nb_peoples: " + str(element))
        print("\n")


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
        self.path0 = []
        self.path1 = []
        self.path2 = []

    def set_visited(self, city_idx, value, fourgon):
        if(city_idx>=self.SIZE):
            print("set_visited: index trop grand")
        else:
            if(fourgon == 0):
                self.visited0[city_idx] = 1 if value else 0 
            elif(fourgon == 1):
                self.visited1[city_idx] = 1 if value else 0 
            elif(fourgon == 2):
                self.visited2[city_idx] = 1 if value else 0 

    def add_city(self, city_idx, fourgon):
        if(city_idx>=self.SIZE):
            print("add_city: index trop grand")
        else:
            if(fourgon == 0):
                self.path0.append(city_idx)
            elif(fourgon == 1):
                self.path1.append(city_idx)
            elif(fourgon == 2):
                self.path2.append(city_idx)

    def show(self):
        i = 0
        for element in self.visited0:
            print(str(i) + " visited0: " + str(element))
            i+=1
        i = 0
        for element in self.visited1:
            print(str(i) + " visited1: " + str(element))
            i+=1
        i = 0
        for element in self.visited2:
            print(str(i) + " visited2: " + str(element))
            i+=1
        i = 0
        for element in self.path0:
            print(str(i) + " path0: " + str(element))
            i+=1
        i = 0
        for element in self.path1:
            print(str(i) + " path1: " + str(element))
            i+=1
        i = 0
        for element in self.path2:
            print(str(i) + " path2: " + str(element))
            i+=1

""" Uncoment to test """
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


