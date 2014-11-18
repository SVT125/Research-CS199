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
        '''Reads the data in to list vars x, y, z'''
        with open(file_name, 'r') as f:
                lines = f.readlines()
        	for line in lines:
                        variables = line.split('\t')
                        x.append(variables[0])
                        y.append(variables[1])
                        z.append(variables[2])

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








#I could not figure out how to add a new file so here is my beta-ish data organization script:
#It takes a file and a set of 2 or 3 variable names and creates a master dict of all galaxies
#and then 2 or 3 lists of every value corresponding to the given variable name.
#It also creates a list and string list of variable names (parameters).
from collections import namedtuple

parameters = []
master = {} #A dictionary with the key as the name and the value as a 
	    #Galaxy dict with each key value pair as a variable name and value
str_params = ''
x=[]
y=[]
z=[]

def setup():
    global master, x, y, z
    print("""Please input the coordinate value names. Note: if you press enter without 
declaring a z value the program will continue as a 2 dimensional correlation. Also,
please ensure that all values are the exact names as written in the data file.""")
    while True:
        x_value = input("What is the x coordinate value name: ").lower().strip()
        y_value = input("What is the y coordinate value name: ").lower().strip()
        z_value = input("What is the z coordinate value name: ").lower().strip()
        try:
            assert x_value in parameters and y_value in parameters and ((z_value in parameters) or z_value==''), "One or more of your parameters was invalid"
            assert x_value!=y_value!=z_value, "Two or more of your parameters were the same"
            break
        except:
            continue
    for k,v in sorted(master.items()):
        x.append(v[x_value])
        y.append(v[y_value])
        if z_value != '':
            z.append(v[z_value])
    return

def galaxy_in(data:[str]):
    galaxy={}
    for item_index in range(len(data)):
        try:
            galaxy[parameters[item_index]] = int(data[item_index])
        except:
            galaxy[parameters[item_index]] = data[item_index]
    return galaxy

def read_data(file_name: str) -> None:
    global str_params
    ''' Reads the data in to list vars x, y, z'''
    with open(file_name, 'r') as f:
        lines = f.readlines()
        param_line=lines[0].split('\t')
        param_line[-1]=param_line[-1][:-1]
        lines=lines[1:]
        for p in param_line:
            parameters.append(p)
            str_params += p + ' '
        for line in lines:
            master[line.split('\t')[0]] = galaxy_in(line.split('\t'))

if __name__ == '__main__':
    while True:
        try:
            file = input("What is the name of the file: ")
            read_data(file)
            break
        except:
            print("Error: this file either does not exist of is not in this directory.")
            continue
    setup()
    print(str_params)
    print(sorted(master))
    print(parameters)
    print(x,y,z)
    
"""
Sample output using the following file Data.txt:
name    radius    majaxis    minaxis
x    5    1    10
y    10    1    20
z    100    1    200

What is the name of the file: Data.txt
Please input the coordinate value names. Note: if you press enter without 
declaring a z value the program will continue as a 2 dimensional correlation. Also,
please ensure that all values are the exact names as written in the data file.
What is the x coordinate value name: radius
What is the y coordinate value name: majaxis
What is the z coordinate value name: minaxis
name radius majaxis minaxis 
{'y': {'majaxis': 1, 'radius': 10, 'name': 'y', 'minaxis': 20}, 'x': {'majaxis': 1, 'radius': 5, 'name': 'x', 'minaxis': 10}, 'z': {'majaxis': 1, 'radius': 100, 'name': 'z', 'minaxis': 200}}
['name', 'radius', 'majaxis', 'minaxis']
[5, 10, 100] [1, 1, 1] [10, 20, 200]
"""
