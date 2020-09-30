import sys
import numpy as np
from scipy import signal
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True

# one dimmensional random walk

def random_walk(N):
    """
    N: int, number of steps to take
    """
    np.random.seed(23)
    # can make one step forward or backward 
    steps = np.array([-1, 1]) 
    # forward or backward steps are equally probable 
    prob = 0.5  
    # generate N-random values for the walks
    random_positions = np.random.choice(steps, N, prob)
    # get random walk 
    random_walk = np.cumsum(random_positions)
    return np.arange(N)+1, random_walk

# generate 1D random walk of N steps
N = 100000
x, random_walk = random_walk(N)


# normalize the random walk
random_walk = (1/np.sqrt(N))*random_walk

# lets always start from origin
random_walk = np.concatenate((np.zeros(1), random_walk))
x = np.concatenate((np.zeros(1), x))

plt.scatter(x, random_walk, s=1.5, c='r', alpha=1,
            label = r"Steps = {}".format(N))
plt.xlabel(r'Random Steps Taken')
plt.ylabel(r'Random Walk (Normalized)')
plt.title(r'One dimensional random walk')
plt.legend()
plt.show()