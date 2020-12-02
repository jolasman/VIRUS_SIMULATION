import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import constants
style.use('fivethirtyeight')


def chart_5_subplot():
    """Build the chart data
    """
    fig = plt.figure(num=123456, figsize=(
        constants.FOUR_PLOTS_FIG_SIZE_X, constants.FOUR_PLOTS_FIG_SIZE_Y))
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):
        graph_data = open(constants.CHART_DATA, 'r').read()
        lines = graph_data.split('\n')
        xs = []
        y_healthy = []
        y_infected = []
        y_dead = []
        y_healed = []
        y_quarantine = []
        for line in lines:
            if len(line) > 1:
                x, healthy, infected, dead, healed, quarantine = line.split(
                    ',')
                xs.append(int(x))
                y_healthy.append(int(healthy))
                y_infected.append(int(infected))
                y_dead.append(int(dead))
                y_healed.append(int(healed))
                y_quarantine.append(int(quarantine))

        ax1.clear()
        ax1.plot(xs, y_healthy, color="g", label="Healthy")
        ax1.plot(xs, y_infected, color='r', label="Infected")
        ax1.plot(xs, y_dead, color='k',  label="Dead")
        ax1.plot(xs, y_healed, color='y', label="Healed")
        ax1.plot(xs, y_quarantine, color='b', label="People in Quarentine")
        ax1.legend(loc='upper left')
        ax1.set_xlabel('Days')
        ax1.set_ylabel('Agents')
        fig.suptitle('Simulation cumulative values in real-time', fontsize=16)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()


if __name__ == "__main__":
    chart_5_subplot()
