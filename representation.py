from data import DataLoader, Data, Chromosome
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pickle

latitudeRef = 50.8
longitudeRef = 4.4
R_earth = 6378137 

def geoToCart(latitudes, longitudes, latitudeRef, longitudeRef, radius) :
	x = []
	y = []
	
	for i in range(len(latitudes)) :
		x.append(radius*(longitudes[i]-longitudeRef))
		y.append(radius*(latitudes[i]-latitudeRef))
	
	return (x,y)


def coordOnCircle(x0, y0, radius, nb):
	xs = [radius*np.cos(x*2*np.pi/nb)+x0 for x in range(nb)]
	ys = [radius*np.sin(y*2*np.pi/nb)+y0 for y in range(nb)]

	return xs, ys

def plotArcs(x,y,ax) :
	
	for i in range(len(x)) :
		for j in range(i,len(x)) :
			ax.plot([x[i],x[j]],[y[i],y[j]],color="black", alpha=0.2)

def plotCities(x,y,nbH, names,ax) :
	factor = 70
	for i in range(len(x)) :
		#aire proportionelle nb habitants
		#-> rayon proportionel sqrt(nb_h)
		color = "yellow" if i == Data.BN_IDX else "white"
		radius = 10000 if i == Data.BN_IDX else factor*np.sqrt(nbH[i])
		circle = plt.Circle((x[i],y[i]),radius,color=color,fill=True,zorder=10)
		circle2 = plt.Circle((x[i],y[i]),radius,color="black",fill=False,zorder=11, linewidth=1)
		# text = matplotlib.text.Text(x[i], y[i]+radius, names[i], fontsize="small")
		# print(text.bbox)
		# print(text.clip_box)
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
		elif i == Data.WSP_IDX or i == Data.BSA_IDX or i == Data.BN_IDX or i == Data.AUDERGHEM_IDX or i == Data.WB_IDX or i == Data.UCCLE_IDX or i == Data.FOREST_IDX:
			valign="top"
			y_text = y[i]-radius
		if i != Data.BN_IDX :
			text = ax.text(x_text, y_text, names[i], fontsize="small", backgroundcolor="white", zorder=13,
						   bbox=dict(alpha=0.3, color="white", linewidth=0),
						   horizontalalignment=halign,
						   verticalalignment=valign)
		# text.set_bbox(dict(alpha=0.5, ))/
		#~ circle.set_in_layout(True)
		#~ circle.set_zorder(1)
		ax.add_patch(circle)
		ax.add_patch(circle2)


def plotPath(x, y, path_origin, color, ax) :

	x0 = -1
	y0 = -1

	path = [0] + path_origin + [0]

	alpha = 1

	for i in range(len(path)) :
		if path[i] != -1 :
			x1 = x[path[i]]
			y1 = y[path[i]]
			# circle = plt.Circle((x1,y1),5000,color=color,fill=True,zorder=2)
			# ax.add_patch(circle)

			if path[i] == 0:
				alpha = 0.3

			if x0 != -1 and y0 != -1:
				# ax.plot([x0,x1],[y0,y1],color=color)
				ax.arrow(x0, y0, (x1-x0), (y1-y0), color=color, width=500, length_includes_head=True, alpha=alpha, zorder=12)
				alpha = 1

			x0 = x1
			y0 = y1

def plotChromosom(chrom,x,y,ax) :
	plotPath(x,y,chrom.path0,"red",ax)
	plotPath(x,y,chrom.path1,"green",ax)
	plotPath(x,y,chrom.path2,"blue",ax)
	


dataloader = DataLoader("data_maison_com.txt")

x,y = geoToCart(dataloader.data.latitudes,dataloader.data.longitudes,latitudeRef,longitudeRef, R_earth)
# x, y = coordOnCircle(0, 0, 500000, 19)
# x.insert(0, 0)
# y.insert(0, 0)
file_sol = open("saved_sol.bin","rb")
sol = pickle.load(file_sol)
file_sol.close()

fig = plt.figure()
ax = plt.axes([0,0,1,1])
margin = 200000
ax.set_xlim(min(x)-margin,max(x)+margin)
ax.set_ylim(min(y)-margin,max(y)+margin)


ax.axis("off")
ax.set_aspect("equal")

# plotArcs(x,y,ax)
plotChromosom(sol[0][1],x,y,ax)
plotCities(x,y,dataloader.data.nb_peoples, dataloader.data.names, ax)

plt.show()

