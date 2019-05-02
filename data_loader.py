import numpy as np


def load_data(filename) :
    names = []
    latitudes = []
    longitudes = []
    nb_people = []
    
    lat_bank = 0
    long_bank = 0

    """
    On lit le fichier contenant les données, chaque ligne du fichier est sous la forme :
    
    nom_commune latitude longitude nombre_dhabitants
    
    la seule exception est la banque nationale qui est sous la forme :
    
    Banque latitude longitude
    
    les latitudes et longitudes sont sous forme décimale (en degrés)
    Par convention, on place la lattitude et la longitude de la banque en dernière position
    """
    file_o = open(filename, 'r')
    for l in file_o.readlines() :
        words = l.split(" ")
        if(words[0] == "Banque") :
            lat_bank = float(words[1])
            long_bank = float(words[2])
        else :
            names.append(words[0])
            nb_people.append(int(words[3]))
            latitudes.append(float(words[1]))
            longitudes.append(float(words[2]))
    file_o.close()
    latitudes.append(lat_bank)
    longitudes.append(long_bank)
    
    """
    On calcule les distances entre chaque lieu et on stocke dans une matrice (symétrique du coup)
    les distances sont en mètre au format float
    """
    R_earth = 6378137 
    size = len(latitudes)
    distances = np.zeros((size, size))
    for i in range(size) :
        for j in range(i+1, size) :
            latA = latitudes[i]*np.pi/180
            latB = latitudes[j]*np.pi/180
            dlong = np.abs((longitudes[j]-longitudes[i])*np.pi/180)
            d = R_earth*np.arccos(np.sin(latA)*np.sin(latB)+np.cos(latA)*np.cos(latB)*np.cos(dlong))
            distances[i,j] = d
            distances[j,i] = d
    
    return (names, nb_people, latitudes, longitudes, distances)


#names, nb_peoples, latitudes, longitudes, distances = load_data("data_maison_com.txt")

#np.savetxt("distances.txt", distances.astype(int), fmt="%d")
    
