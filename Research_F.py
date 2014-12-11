from collections import namedtuple
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats.stats import pearsonr
import os.path
import pyfits
import matplotlib
import matplotlib.pyplot as plt
import math

parameters = []
master = {} #A dictionary with the key as the name and the value as a 
            #Galaxy dict with each key value pair as a variable name and value
str_params = ''
x=[]
y=[]
z=[]

def setup(files):
    global master, x, y, z
    print("""Please input the coordinate value names. Note: if you press enter without 
declaring a z value the program will continue as a 2 dimensional correlation. Also,
please ensure that all values are the exact names as written in the data file.""")
    done = False
    for file_name in files:
        try:
            if file_name.find('.fit') != -1:
                f=file_name
                param_line=pyfits.getheader(f)
                param_line_keys=param_line.keys()
                data, param_line=pyfits.getdata(f, 1, header=True)
                parameter_list=data.names
                correlations(file_name,master,parameter_list,read_fits_data)
            elif file_name.find('.txt') != -1:
                infile = open('varnamest.txt','r')
                params = infile.readlines()
                correlations(file_name,master,params,read_data)
            elif file_name.find('.tsv') != -1:
                read_tsv(file_name)
                read_data('{}.txt'.format(file_name[0:-4]), x_value, y_value, z_value)
            else:
                print("File "+file_name+" is not a supported file type\n"+
                      "Supported file types include: .fit .fits .tsv .txt")
                return
            done = True
        except KeyError as err:
            print("{} was not found in file {}".format(err,file_name))
    if not done:
        print("One or more of the specified values was not found in any given file")
        setup(files)
    return

def correlations(file_name:str, d:dict, param_list:'list of str', reader:'function(file_name,x_value,y_value,z_value)') -> None:
    '''Runs through the dictionary checkin every combination of variables. Continues if an exception is thrown.'''
    params2 = param_list
    #params = param_list[90:] #the starting index to start from in the parameter list in case we continue the process
    print('Number of parameters: ' + str(len(params2)))
    counter = 0
    corrfile = open('results.txt','w')
    for v1 in params2:
            for v2 in params2:
                try:
                    z_value = ''
                    reader(file_name, v1.strip('\n'), v2.strip('\n'), z_value)
                    correlation = corr(v1.strip('\n'),v2.strip('\n'),master)
                    if math.isnan(correlation) or abs(correlation) > 1:
                        continue
                    print('The found correlation: ' + str(correlation))
                    if(abs(correlation) > 0.2):
                        print('Correlation: ' + str(correlation) + '\t' + v1 + '\t' + v2)
                        corrfile.write(v1 + '\t' + v2 + '\t' + str(correlation) + '\n\n')
                        corrfile.flush()
                except Exception as e:
                    print(e)
                    print('Skipping variable pair ' + v1 + '\t' + v2)
                    continue
    corrfile.close()
    

def galaxy_in(data:[str], param_index:[int]):
    galaxy={}
    for index in range(len(data)):
        if param_index[index]==0:
            continue
        galaxy[parameters[param_index[index]]] = data[index]
    return galaxy

def fits_galaxy_in(data, param_index):
    global parameters
    galaxy={}
    index=0
    while True:
        try:
            galaxy[parameters[param_index[index]]] = data[index]
            index += 1
        except (IndexError):
            break
    return galaxy

def read_data(file_name: str, x_value, y_value, z_value) -> None:
    global str_params, parameters, master
    ''' Reads the data in to list vars x, y, z'''
    with open(file_name, 'r') as f:
        lines = f.readlines()
        param_line=lines[0].strip('\n').split('\t')
        lines=lines[1:]
        param_index=[0,0,0]
        x_presence=False
        y_presence=False
        z_presence=False
        for index in range(len(param_line)):
            if param_line[index]==x_value:
                x_presence=True
                param_index[0]=index
            if param_line[index]==y_value:
                y_presence=True
                param_index[1]=index
            if param_line[index]==z_value:
                z_presence=True
                param_index[2]=index
            parameters.append(param_line[index])
            str_params += param_line[index] + ' '
        if not x_presence:
            raise KeyError (x_value)
        if not y_presence:
            raise KeyError (y_value)
        if not z_presence and z_value!='':
            raise KeyError (z_value)
        sub_data=[0,0,0]
        for line in lines:
            line=line.strip('\n').split('\t')
            for index in range(len(line)):
                if parameters[index]==x_value:
                    sub_data[0]=line[index]
                elif parameters[index]==y_value:
                    sub_data[1]=line[index]
                elif parameters[index]==z_value and z_value != '':
                    sub_data[2]=line[index]
            master[line[0]] = galaxy_in(sub_data, param_index)
    print("File read in succesfully")

def read_fits_data(file_name: str, x_value, y_value, z_value) -> None:
    global str_params, parameters, master
    ''' Reads the data in to list vars x, y, z'''
    #with open(file_name, 'r') as f:
    f=file_name
    param_line=pyfits.getheader(f)
    param_line_keys=param_line.keys()
    data, param_line=pyfits.getdata(f, 1, header=True)
    parameter_list=data.names
    #print(parameter_list)
    param_index=[0,0,0]
    x_presence=False
    y_presence=False
    z_presence=False
    for index in range(len(parameter_list)):
        if parameter_list[index]==x_value:
            x_presence=True
            param_index[0]=index
        if parameter_list[index]==y_value:
            y_presence=True
            param_index[1]=index
        if parameter_list[index]==z_value:
            z_presence=True
            param_index[2]=index
        parameters.append(parameter_list[index])
        str_params += parameter_list[index] + ' '
    if not x_presence:
        raise KeyError (x_value)
    if not y_presence:
        raise KeyError (y_value)
    if not z_presence and z_value!='':
        raise KeyError (z_value)
    sub_data=[0,0,0]
    galaxy_count = 0
    for line in data:
        galaxy_count += 1
        #print("Reading in galaxy "+str(line[32]))
            #if parameters[index]==x_value:
        sub_data[0]=line[x_value]
            #elif parameters[index]==y_value:
        sub_data[1]=line[y_value]
            #elif parameters[index]==z_value:
        if z_value != '':
            sub_data[2]=line[z_value]
        master[line[32]] = fits_galaxy_in(sub_data, param_index)
        if galaxy_count >= 1000:
            break
    print("File read in succesfully")
    if z_value != '':
        print_galaxies(master)

def read_tsv(filename:'str') -> None:
    '''Reads the TSV file and writes the spiral galaxy subset to file (for later use).'''
    '''Writes the file by printing the variable names first, then separate by a line of asterisks.'''
    with open(filename, 'r') as f:
        lines = []
        first_line = f.readline().split("\t") # read in the variable 
        information = {key: [] for key in first_line} # dictionary of variable lists (galaxies horizontally)
        n = 0
        for line in f:
            n+=1
            if n%100000==0:
                print("Copying line",n)
            spl = line.split("\t")
            for i in range(0,len(first_line)):
                word = first_line[i]
                information[word].append(spl[i])
        l = [information[quan] for quan in ["P_CS","diskAxisRatio"]]#data to work with of the quantities
        indices = []
        number = [0.8,0.5]
        for i in range(len(l[0])):
            to_return = True #Will be flipped off if one of the two quantities is off
            for j in range(len(l)):
                num = abs(float(l[j][i]))
                if num <= number[j]:
                    to_return = False
            if to_return == True:
                indices.append(i)
        # Print the file, each line a galaxy with its variables split by whitespace.
        outfile = open('spiralgalaxies.txt','w')
        for name in first_line:
            outfile.write(name + '\t')
        outfile.write('\n')
        for index in indices:
            for key in information.keys():
                outfile.write(information[key][index] + '\t')
            outfile.write('\n') 
        outfile.close()

def corr(x_key: 'key', y_key: 'key', galaxies: dict) -> float:
        '''Takes two lists of x,y to calculate the 2D Pearson correlation.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        correlations = pearsonr(x,y)
        return correlations[0]

def plot(x_key:'key',y_key:'key', galaxies:dict, labels=None) -> None:
        '''Plots the lists xy in a 2D graph.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        plt.scatter(x,y)
        plt.show()

def retrieve_dict_vector(d:dict,key:str) -> 'list of float':
        '''Returns a list of all features across every example in d given a key.'''
        vector = []
        for example_key in d.keys():
                vector.append(float(d[example_key][key]))
        return vector

def print_galaxies(d:dict) -> None:
    '''Prints the dictionary of galaxies in a txt file for PCA.'''
    outfile = open('examples.txt','w')
    for galaxy_key in d.keys():
        line = ''
        for variable_key in d[galaxy_key].keys():
            line += str(d[galaxy_key][variable_key]) + ' '
        outfile.write(line + '\n')
    outfile.close()

if __name__ == '__main__':
    setup(input('Name of file: '))

    #plot(x_value, y_value, z_value, master)
