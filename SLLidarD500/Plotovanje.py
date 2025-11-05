import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def sredjivanjePlot(x, y):
    plt.cla()
    plt.scatter(x, y)

ani = FuncAnimation(plt.gcf(), sredjivanjePlot, interval=100)
plt.show()
    
    

