import main
import data_loader

names, nb_peoples, latitudes, longitudes, distances = data_loader.load_data("data_maison_com.txt")

most_pop = main.most_populated(nb_peoples)
print(most_pop)
print("{}, {}, {}".format(names[most_pop[0]],names[most_pop[1]],names[most_pop[2]]))


#bonne solution
sol_bidon1 = [[1,4,5,16,8,4,3,11],[3,2,14,13,10,7,12,15],[0,6,9,16,17,18]]

#mauvaise solution : premier camion visite 3 communes plus peuplés
sol_bidon2 = [[1,4,5,7,8,2,3,11],[3,4,14,13,10,16,12,15],[0,6,9,16,17,18]]

#mauv solution, l'un des camions a une trop grande recette
sol_bidon3 = [[1,4,5,16,8,4,3,11],[3,2,14,13,10,7,12,15,6,9,16],[0,17,18]]

print(main.is_admissible(sol_bidon1,nb_peoples,most_pop,sum(nb_peoples)))
print(main.fitness_fct(sol_bidon1, distances, nb_peoples))

print(main.is_admissible(sol_bidon2,nb_peoples,most_pop,sum(nb_peoples)))
print(main.fitness_fct(sol_bidon2, distances, nb_peoples))

print(main.is_admissible(sol_bidon3,nb_peoples,most_pop,sum(nb_peoples)))
print(main.fitness_fct(sol_bidon3, distances, nb_peoples))
