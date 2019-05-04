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
from main import fitness_fct, is_admissible
import numpy as np

def dominate(s1, s2) :
    d1,r1 = fitness_fct(s1)
    d2,r2 = fitness_fct(s2)
    res = True
    if(d1 > d2 or r1 > r2) :
        res = False
    return res

def fast_non_dominated_sort(pop) :
    pop_size = len(pop)
    
    ranks = [0]*pop_size
    fronts = []
    fronts.append([])
    
    dominated = [[]]*pop_size
    dom_count = [0]*pop_size
    
    for i in range(pop_size) :
        for j in range(pop_size) :
            if(dominate(pop[i], pop[j])) :
                dominated[i].append(j)
            elif(dominate(pop[j], pop[i])) :
                dom_count[i] += 1
        if(dom_count[i] == 0) :
            ranks[i] = 0
            fronts[0].append(i)
    k = 0
    while(len(fronts[k]) > 0) :
        Q = []
        for i in range(len(fronts[k])) :
            for j in range(len(dominated[i])) :
                dom_count[j] -= 1
                if(dom_count[j] == 0) :
                    ranks[j] = k + 1
                    Q.append(j)
        k += 1
        fronts.append(Q)
    
    F = [[pop[i] for i in f] for f in fronts]
    #~ for i in range(len(fronts)) :
        #~ F.append([])
        #~ for e in f :
            #~ F[i].append(pop[e])
    
    return F

def crowding_distance_assignment(pop_set) :
    l = len(pop_set)
    crow_dist = [0]*l
    obj_values = np.empty(len(pop_set))
    for s in pop_set :
        obj_values.add(fitness_fct(s))
        
    for i in range(2) :
        sorted_idx = np.argsort(obj_values[:,i])
        
        min_value = obj_values[sorted_idx[0],i]
        max_value = obj_values[sorted_idx[l-1],i]
        crow_dist[sorted_idx[0]] = np.inf
        crow_dist[sorted_idx[l-1]] = np.inf
        for j in range(1,l-2) :
            crow_dist[sorted_idx[j]] += (obj_values[sorted_idx[j-1],i] - obj_values[sorted_idx[j+1],i])/(max_value-min_value)
    
    return crow_dist

dataloader = DataLoader("data_maison_com.txt")
data = dataloader.data
data.show() 
