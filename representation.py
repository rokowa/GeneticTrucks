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

SOLUTIONS_FILE = "saved_sol.bin"
SAVE_FILE = "graphe_communes.pdf"

latitudeRef = 50.8
longitudeRef = 4.4
R_earth = 6378137 


def geoToCart(latitudes, longitudes, latitudeRef, longitudeRef, radius):
    x = []
    y = []

    for i in range(len(latitudes)) :
        x.append(radius*(longitudes[i]-longitudeRef))
        y.append(radius*(latitudes[i]-latitudeRef))

    return x, y


def coordOnCircle(x0, y0, radius, nb):
    xs = [radius*np.cos(x*2*np.pi/nb)+x0 for x in range(nb)]
    ys = [radius*np.sin(y*2*np.pi/nb)+y0 for y in range(nb)]

    return xs, ys


def plotArcs(x, y, ax):
    for i in range(len(x)) :
        for j in range(i,len(x)) :
            ax.plot([x[i],x[j]],[y[i],y[j]],color="black", alpha=0.2)


def plotCities(x, y, nbH, names, ax):
    factor = 70

    for i in range(len(x)) :
        #aire proportionelle nb habitants
        #-> rayon proportionel sqrt(nb_h)
        color = "yellow" if i == Data.BN_IDX else "white"
        radius = 10000 if i == Data.BN_IDX else factor*np.sqrt(nbH[i])
        circle = plt.Circle((x[i], y[i]), radius, color=color, fill=True, zorder=10)
        circle2 = plt.Circle((x[i], y[i]), radius, color="black", fill=False, zorder=11, linewidth=1)

        x_text = x[i]
        y_text = y[i]+radius
        halign = "center"
        valign = "bottom"
        if i == Data.SJTN_IDX:
            halign = "left"
        elif i == Data.MSJ_IDX:
            halign="right"
            valign="center"
            y_text = y[i]
            x_text = x[i] - radius
        elif (i == Data.WSP_IDX or
              i == Data.BSA_IDX or
              i == Data.BN_IDX or
              i == Data.AUDERGHEM_IDX or
              i == Data.WB_IDX or
              i == Data.UCCLE_IDX or
              i == Data.FOREST_IDX):
            valign="top"
            y_text = y[i]-radius

        if i != Data.BN_IDX :
            ax.text(x_text, y_text, names[i], fontsize="small", backgroundcolor="white", zorder=13,
                    bbox=dict(alpha=0.3, color="white", linewidth=0),
                    horizontalalignment=halign,
                    verticalalignment=valign)

        ax.add_patch(circle)
        ax.add_patch(circle2)


def plotPath(x, y, path_origin, color, ax):

    x0 = -1
    y0 = -1

    path = [0] + path_origin + [0]

    alpha = 1

    for i in range(len(path)):
        if path[i] != -1:
            x1 = x[path[i]]
            y1 = y[path[i]]

            if path[i] == 0:
                alpha = 0.3

            if x0 != -1 and y0 != -1:
                ax.arrow(x0, y0, (x1-x0), (y1-y0), color=color, width=500, length_includes_head=True, alpha=alpha,
                         zorder=12)
                alpha = 1

            x0 = x1
            y0 = y1


def plotChromosom(chrom, x, y, ax):
    plotPath(x, y, chrom.path0, "red", ax)
    plotPath(x, y, chrom.path1, "green", ax)
    plotPath(x, y, chrom.path2, "blue", ax)


dataloader = DataLoader("data_maison_com.txt")

x, y = geoToCart(dataloader.data.latitudes, dataloader.data.longitudes, latitudeRef, longitudeRef, R_earth)


file_sol = open(SOLUTIONS_FILE, "rb")
sol = pickle.load(file_sol)
file_sol.close()

fig = plt.figure()
ax = plt.axes([0, 0, 1, 1])
ax.axis("off")
ax.set_aspect("equal")
plt.autoscale(tight=True)
xmargin = 200000
ymargin = 50000
ax.set_xlim(min(x)-xmargin,max(x)+xmargin)
ax.set_ylim(min(y)-ymargin,max(y)+ymargin)

#Plot all arcs
#plotArcs(x,y,ax)

#Plot cities
plotCities(x,y,dataloader.data.nb_peoples, dataloader.data.names, ax)

#sort first front
front = sorted(sol[0], key=lambda chromosome: chromosome.get_fitness_score()[0])

#Plot chromosom
plotChromosom(front[0],x,y,ax)

#Save figure
#plt.savefig(SAVE_FILE, frameon=False, bbox_inches="tight", pad_inches=0)

plt.show()
