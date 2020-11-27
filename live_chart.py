import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from constants import FOUR_PLOTS_FIG_SIZE_X, FOUR_PLOTS_FIG_SIZE_Y
style.use('fivethirtyeight')

def chart_5_axes():
    """Build the chart data
    """
    fig = plt.figure(num=123456, figsize=(
        FOUR_PLOTS_FIG_SIZE_X, FOUR_PLOTS_FIG_SIZE_Y))
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):
        graph_data = open('chart_data.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        y_healthy = []
        y_infected = []
        y_dead = []
        y_healed = []
        y_quarentine = []
        for line in lines:
            if len(line) > 1:
                x, healthy, infected, dead, healed, quarentine = line.split(',')
                xs.append(int(x))
                y_healthy.append(int(healthy))
                y_infected.append(int(infected))
                y_dead.append(int(dead))
                y_healed.append(int(healed))
                y_quarentine.append(int(quarentine))

        ax1.clear()
        ax1.plot(xs, y_healthy, color="g", label="Healthy")
        ax1.plot(xs, y_infected, color='r', label="Infected")
        ax1.plot(xs, y_dead, color='k',  label="Dead")
        ax1.plot(xs, y_healed, color='y', label="Healed")
        ax1.plot(xs, y_quarentine, color='b', label="People in Quarentine")
        ax1.legend(loc='upper left')
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()




if __name__ == "__main__":
    chart_5_axes()

    