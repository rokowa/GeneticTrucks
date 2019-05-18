import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from multiprocessing import Process
import matplotlib.animation as animation

class SolutionsPlot :
    
    def __init__(self, pop) :
        self.fig = plt.figure()
        self.ax = self.fig.gca()
        self.ax.autoscale(True)
        
        self.pop = pop
        
        self.x_datas = []
        self.y_datas = []
        
        self.plots = []
    
    def add_gen(self) :
        self.x_datas.append([])
        self.y_datas.append([])
        
        line, = self.ax.plot(fmt="-o")
        self.plots.append(line)
    
    def add_point(self, x, y) :
        self.x_datas[-1].append(x)
        self.y_datas[-1].append(x)
    
    def update(self, frame) :
        
        print(len(self.pop))
        
        i_start = len(self.x_datas)-1
        colors = cm.rainbow(np.linspace(0, 1, len(self.pop)))
        
        for i,gen in self.pop[i_start:-1] :
            if(i > 0) :
                self.add_gen()
            j_start = len(self.x_datas[-1])
            for chrom in gen[j_start:-1] :
                self.add_point(chrom.get_fitness_score()[0], chrom.get_fitness_score()[1])
            self.plots[-1].set_data(self.x_datas[-1], self.y_datas[-1])
        
        for i,line in self.plots :
            line.set_color(colors[i])

        
        return self.plots
        #~ self.ax.canvas.draw()

    def show(self) :
        ani = animation.FuncAnimation(self.fig, self.update, interval=40,blit=True)
        plt.show()
        
    def start(self) :
        p = Process(target=self.show)
        p.start()
        
