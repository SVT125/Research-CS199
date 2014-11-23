from collections import namedtuple
import pyfits
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
        
def plot(x_key: 'key', y_key: 'key', z_key: 'key', galaxies: dict, labels=None) -> None:
        '''Plots the lists xyz in a 3D graph.'''
        fig = plt.figure()
        ax = Axes3D(fig)
        
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        z = retrieve_dict_vector(galaxies,z_key)
        
        if labels == None:
                ax.scatter(xs = x, ys = y, zs = z, zdir = 'z', label = 'ys=0, zdir = z')
        # Colors the outliers, fix for galaxy dicts
        '''
        else:
                nonanomalies_x = [element for element in x if not x[x.index(element)]]
                nonanomalies_y = [element for element in y if not y[y.index(element)]]
                nonanomalies_z = [element for element in z if not z[z.index(element)]]
                anomalies_x = [element for element in x if x[x.index(element)]]
                anomalies_y = [element for element in y if y[y.index(element)]]
                anomalies_y = [element for element in z if z[z.index(element)]]
                ax.scatter(xs = anomalies_x, ys = anomalies_y, zs = anomalies_z, c = 'red', zdir = 'z', label = 'ys=0, zdir = z')
                ax.scatter(xs = nonanomalies_x, ys = nonanomalies_y, zs = nonanomalies_z, c = 'blue',zdir = 'z', label = 'ys=0, zdir = z')
        '''
        plt.show()
        
def retrieve_dict_vector(d:dict,key:str) -> list:
        '''Returns a list of all features across every example in d given a key.'''
        vector = []
        for example_key in d.keys():
                vector.append(d[example_key][key])
        return vector









parameters = []
master = {} #A dictionary with the key as the name and the value as a 
            #Galaxy dict with each key value pair as a variable name and value
str_params = ''
x=[]
y=[]
z=[]
x_value=''
y_value=''
z_value=''

def setup():
    global master, x, y, z, file_name, x_value, y_value, z_value
    print("""Please input the coordinate value names. Note: if you press enter without 
declaring a z value the program will continue as a 2 dimensional correlation. Also,
please ensure that all values are the exact names as written in the data file.""")
    while True:
        x_value = input("What is the x coordinate value name: ").lower().strip()
        y_value = input("What is the y coordinate value name: ").lower().strip()
        z_value = input("What is the z coordinate value name: ").lower().strip()
        break
        #try:
            #assert x_value in parameters and y_value in parameters and ((z_value in parameters) or z_value==''), "One or more of your parameters was invalid"
            #print('1')
            #assert x_value!=y_value!=z_value, "Two or more of your parameters were the same"
            #break
        #except:
            #continue
        #print('yes')
    if file_name.find('.fit'):
        read_fits_data(file_name, x_value, y_value, z_value)
    elif file_name.find('.txt'):
        read_data(file_name, x_value, y_value, z_value)
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

def fits_galaxy_in(data):
    global parameters
    galaxy={}
    index=0
    while True:
        try:
            #print(data[index])
            galaxy[parameters[index]]=data[index]
            index+=1
        except (IndexError):
            #print('indexerror')
            break
    return galaxy
        

def read_data(file_name: str, x_value, y_value, z_value) -> None:
    global str_params, parameters, master
    ''' Reads the data in to list vars x, y, z'''
    with open(file_name, 'r') as f:
        lines = f.readlines()
        param_line=lines[0].strip('\n').split('\t')
        param_line[-1]=param_line[-1][:]
        lines=lines[1:]
        for p in param_line:
            parameters.append(p)
            str_params += p + ' '
        for line in lines:
            if parameters[index]==x_value:
                sub_data[0]=line[index]
            elif parameters[index]==y_value:
                sub_data[1]=line[index]
            elif parameters[index]==z_value:
                sub_data[2]=line[index]
        master[line.split('\t')[0]] = galaxy_in(line.strip('\n').split('\t'))
    print("File read in succesfully")
            
def read_fits_data(file_name: str, x_value, y_value, z_value) -> None:
    global str_params, parameters, master
    ''' Reads the data in to list vars x, y, z'''
    #with open(file_name, 'r') as f:
    f=file_name
    param_line=pyfits.getheader(f)
    param_line_keys=param_line.keys()
    data, param_line=pyfits.getdata(f, 1, header=True)
    parameters=data.names
    #for p in parameters:
        #str_params += p + ' '
    sub_data=[0,0,0]
    for line in data:
        print("Reading in galaxy "+str(line[0]))
        for index in range(len(line)):
            if parameters[index]==x_value:
                sub_data[0]=line[index]
            elif parameters[index]==y_value:
                sub_data[1]=line[index]
            elif parameters[index]==z_value:
                sub_data[2]=line[index]
        master[line[0]] = fits_galaxy_in(sub_data)
    print("File read in succesfully")

    #file="fpObjc-003172-3-0134.fit"
        #lines = f.readlines()
        #param_line=lines[0].strip('\n').split('\t')
        #param_line[-1]=param_line[-1][:]
        #lines=lines[1:]
        #for p in param_line:
            #parameters.append(p)
            #str_params += p + ' '
        #for line in lines:
            #master[line.split('\t')[0]] = galaxy_in(line.strip('\n').split('\t'))

if __name__ == '__main__':
    while True:
        try:
            file_name = input("What is the name of the file: ")
            break
        except (FileNotFoundError):
            print("Error: this file either does not exist of is not in this directory.")
            continue
    setup()
    #print(str_params) #not written
    #print('\n\n')
    print(master.items()) #check
    print('\n\n')
    print(parameters) #check
    print('\n\n')
    print(x,y,z) #check
    plot(x_value, y_value, z_value, master)