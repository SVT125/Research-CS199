from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt

def corr(x_key: 'key', y_key: 'key', z_key: 'key', galaxies: dict) -> float:
        '''Takes three lists of x,y,z to calculate the 3D Pearson correlation.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        z = retrieve_dict_vector(galaxies,z_key)
        return ((pearsonr(x,z)**2 + pearsonr(y,z)**2 - 2 * pearsonr(x,z) * pearsonr(y,z) * pearsonr(x,y))/(1-pearsonr(x,y))**2)** .5
        
def plot(x_key:'key',y_key:'key', galaxies:dict, labels=None) -> None:
        '''Plots the lists xy in a 2D graph.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        plt.scatter(x,y)
        if labels != None:
                pass #outliers with labels
        plt.show()
  
        
def plot(x_key: 'key', y_key: 'key', z_key: 'key', galaxies: dict, labels=None) -> None:
        '''Plots the lists xyz in a 3D graph.'''
        fig = plt.figure()
        ax = Axes3D(fig)
        
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        z = retrieve_dict_vector(galaxies,z_key)
        # Colors the outliers, fix for galaxy dicts
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
        
def retrieve_dict_vector(d:dict,key:str) -> list:
        '''Returns a list of all features across every example in d given a key.'''
        vector = []
        for example_key in d.keys():
                vector.append(d[example_key][key])
        return vector

