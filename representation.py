"""
    Authors: COUCHARD Darius, KOWALKSI Robin, DIANGALA Jonathan

    This is an additional feature for our project and is not used by our nsga2 algorithm's implementation

    Geographically represents the solution of the first front of the last Algorithm run (from "nsga2.py")
    Loads the saved_sol.bin file and represents the stored solution in it
"""

from data import DataLoader, Data
import matplotlib.pyplot as plt
import numpy as np
import pickle

latitudeRef = 50.8
longitudeRef = 4.4
R_earth = 6378137


def geoToCart(latitudes, longitudes, latitudeRef, longitudeRef, radius):
    x = []
    y = []
    for i in range(len(latitudes)):
        x.append(radius * (longitudes[i] - longitudeRef))
        y.append(radius * (latitudes[i] - latitudeRef))

    return x, y


def plotArcs(x, y, ax):
    for i in range(len(x)):
        for j in range(i, len(x)):
            ax.plot([x[i], x[j]], [y[i], y[j]], color="black")


def plotCities(x, y, nbH, ax):
    factor = 70
    for i in range(len(x)):
        # aire proportionelle nb habitants
        # -> rayon proportionel sqrt(nb_h)
        color = "yellow" if i == Data.BN_IDX else "white"
        radius = 10000 if i == Data.BN_IDX else factor * np.sqrt(nbH[i])
        circle = plt.Circle((x[i], y[i]), radius, color=color, fill=True, zorder=1)
        circle2 = plt.Circle((x[i], y[i]), radius, color="black", fill=False, zorder=2, linewidth=1)
        # ~ circle.set_in_layout(True)
        # ~ circle.set_zorder(1)
        ax.add_patch(circle)
        ax.add_patch(circle2)


def plotPath(x, y, path, color, ax):
    x0 = -1
    y0 = -1

    for i in range(len(path)):
        if (path[i] != -1):
            x1 = x[path[i]]
            y1 = y[path[i]]
            # ~ circle = plt.Circle((x1,y1),5000,color=color,fill=True,zorder=2)
            # ~ ax.add_patch(circle)
            if (x0 != -1 and y0 != -1):
                # ~ ax.plot([x0,x1],[y0,y1],color=color)
                ax.arrow(x0, y0, (x1 - x0), (y1 - y0), color=color, width=500, length_includes_head=True)
            x0 = x1
            y0 = y1


def plotChromosom(chrom, x, y, ax):
    plotPath(x, y, chrom.path0, "red", ax)
    plotPath(x, y, chrom.path1, "green", ax)
    plotPath(x, y, chrom.path2, "blue", ax)


dataloader = DataLoader("data_maison_com.txt")

x, y = geoToCart(dataloader.data.latitudes, dataloader.data.longitudes, latitudeRef, longitudeRef, R_earth)
file_sol = open("saved_sol.bin", "rb")
sol = pickle.load(file_sol)
file_sol.close()

fig = plt.figure()
ax = plt.axes([0, 0, 1, 1])
margin = 50000
ax.set_xlim(min(x) - margin, max(x) + margin)
ax.set_ylim(min(y) - margin, max(y) + margin)

ax.axis("off")
ax.set_aspect("equal")

# ~ plotArcs(x,y,ax)
plotChromosom(sol[1][0], x, y, ax)
plotCities(x, y, dataloader.data.nb_peoples, ax)

plt.show()
