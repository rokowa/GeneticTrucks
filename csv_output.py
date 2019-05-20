import csv
import pickle

from data import DataLoader, Data, Chromosome

SOLUTIONS_FILE = "saved_sol.bin"

IDX_CONVERSION = [0, 3, 17, 1, 7, 5, 16, 9, 2, 4, 6, 8, 10, 11, 12, 13, 14, 15, 18, 19]

# (OLD, NEW)
# BN_IDX = (0, 0)
# XL_IDX = (1, 3)
# UCCLE_IDX = (2, 17)
# ANDERLECHT_IDX = (3, 1)
# JETTE_IDX = (4, 7)
# EVERE_IDX = (5, 5)
# WSP_IDX = (6, 16)
# AUDERGHEM_IDX = (7, 9)
# BXL_IDX = (8, 2)
# ETBK_IDX = (9, 4)
# GANSHOREN_IDX = (10, 6)
# KOEKELBERG_IDX = (11, 8)
# SCHAERBEEK_IDX = (12, 10)
# BSA_IDX = (13, 11)
# STG_IDX = (14, 12)
# MSJ_IDX = (15, 13)
# SJTN_IDX = (16, 14)
# WSL_IDX = (17, 15)
# FOREST_IDX = (18, 18)
# WB_IDX = (19, 19)


dataloader = DataLoader("data_maison_com.txt")
nb_peoples = dataloader.data.nb_peoples

file_sol = open(SOLUTIONS_FILE, "rb")
sol = pickle.load(file_sol)
file_sol.close()

first_front = sol[0]

rows = []

current_money = 0

for chrom in first_front:
    for path_origin in [chrom.path0, chrom.path1, chrom.path2]:
        path_output = []
        money = []
        path = [0] + path_origin + [0]
        for i, c in enumerate(path):
            if c != -1:
                path_output.append(IDX_CONVERSION[c])
                current_money += 0 if c == 0 or i == 0 else nb_peoples[path[i-1]]*0.7
                money.append(round(current_money, 2))
        rows.append(path_output)
        rows.append(money)
        current_money = 0

file_o = open("pareto_solution.csv", "w", newline="")
csvfile = csv.writer(file_o, delimiter=";")
csvfile.writerows(rows)
file_o.close()
