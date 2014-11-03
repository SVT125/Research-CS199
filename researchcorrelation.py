from mpl_toolkits.mplot3d import Axes3D
from scipy import scipy.stats.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt

x = []
y = []
z = []
variables = [] # names of variables
galaxy_counter = [] # fill in with counters per galaxy
threshold = 0.01 # wat

def run(threshold: float) -> None:
        '''Increments galaxy_counter for correlations above threshold for
        permutations of all variables'''
        for i in range(len(variables)):
                for j in range(len(variables)):
                        # increment counter, retrieve vars from indices, calculate corr
        

# Will assume returns nothing as it will modify global vars
def read_data(file_name: str) -> None:
	''' Reads the data in to list vars x, y, z
        with open(file_name, 'r') as f: #Increases efficiency and removes need for f.close() by auto closing, even if there is an error
        	lines = f.readlines() # look in docs to loop over all lines
        	for line in lines:
                vars = line.split('\t')
                	x.append(vars[0])
                	y.append(vars[1])
                	z.append(vars[2])

# TODO - To take a triple of values instead, won't just be single lined.
def corr(x: float, y: float) -> float:
        '''Takes a pair of values to return the Pearson correlation.'''
	return pearsonr(x,y)
	
def plot(x:'list of float', y: 'list of float', z: 'list of float') -> None:
	'''Plots the lists xyz in a 3D graph.'''
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.plot(xs = x, ys = y, zs = z, zdir = 'z', label = 'ys=0, zdir = z')
	plt.show()
