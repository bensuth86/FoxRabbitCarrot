import matplotlib.pyplot as plt
from matplotlib import style

# Live graph displays population over duration of ecosys simulation
def record_population(turns, rbbts, foxes):
    "append population count to corresp list every turn"
    Time.append(turns)  # x-axis turns passed
    R_pop.append(rbbts)  # y-axis rabbit population
    F_pop.append(foxes)  # y-axis fox population


def plot_population():

    fig = plt.figure(1)
    plt.xlabel('Time (s)')
    plt.ylabel('Population')
    plt.plot(Time, R_pop, 'b', label="rbbt_population")
    plt.plot(Time, F_pop, 'r', label="fox_poplation")
    plt.legend(loc="upper right")
    plt.show(block=True)

# matplotlib axis
Time = []
R_pop = []
F_pop = []
