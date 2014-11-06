from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt

x = []
y = []
z = []
variables = [] # names of variables
galaxy_counter = [] # fill in with counters per galaxy
threshold = 0.01 # wat

def run(threshold: float) -> None:
        '''Increments galaxy_counter for correlations above threshold for permutations of all variables'''
        for i in range(len(variables)):
                for j in range(len(variables)):
                        print('lelele') # increment counter, retrieve vars from indices, calculate corr

def read_data(file_name: str) -> None:
	''' Reads the data in to list vars x, y, z'''
        with open(file_name, 'r') as f:
                lines = f.readlines()
        	for line in lines:
                        vars = line.split('\t')
                        x.append(vars[0])
                        y.append(vars[1])
                        z.append(vars[2])

def corr(x: float, y: float) -> float:
        '''Takes a pair of values to return the Pearson correlation.'''
	return pearsonr(x,y)
	
def plot(x:'list of float', y: 'list of float', z: 'list of float', labels=None:'list of bool') -> None:
	'''Plots the lists xyz in a 3D graph.'''
	fig = plt.figure()
	ax = Axes3D(fig)
	if labels == None:
                ax.scatter(xs = x, ys = y, zs = z, zdir = 'z', label = 'ys=0, zdir = z')
        else:   
                nonanomalies_x = [element for element in x if not x[x.index(element)]]
                nonanomalies_y = [element for element in y if not y[y.index(element)]]
                nonanomalies_z = [element for element in z if not z[z.index(element)]]
                anomalies_x = [element for element in x if x[x.index(element)]]
                anomalies_y = [element for element in y if y[y.index(element)]]
                anomalies_y = [element for element in z if z[z.index(element)]]
                ax.scatter(xs = anomalies_x, ys = anomalies_y, zs = anomalies_z, c = 'red', zdir = 'z', label = 'ys=0, zdir = z')
                ax.scatter(xs = nonanomalies_x, ys = nonanomalies_y, zs = nonanomalies_z, c = 'blue',zdir = 'z', label = 'ys=0, zdir = z')
	plt.show()
