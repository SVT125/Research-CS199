from collections import namedtuple
import os.path
import pyfits
from scipy.stats.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

master = {}
parameters = []
str_params = ''
x=[]
y=[]
z=[]

def correlation_finder():
    file_name = input('File name: ')
    if file_name.find('.tsv') != -1:
        correlation_tsv(file_name)
    elif file_name.find('.fits') != -1:
        #correlation_fits()
        pass
    elif file_name.find('.txt') != -1:
        correlation_txt(file_name)
    else:
        print('File type unsupported.')

def correlation_tsv(file_name:str):
    global master
    outfile = open('tsv_correlations.txt','w')
    parameter_list = read_tsv(file_name)
    print(parameter_list)
    print('The number of variables: ' + str(len(parameter_list)))
    counter = 0
    for i in range(len(parameter_list)):
        counter += 1
        print('The current variable:' + str(counter))
        for j in range(len(parameter_list)):
            read_data('spiralgalaxies.txt', parameter_list[i], parameter_list[j],'')
            print('Checkpoint')
            for k,v in master.items():
                print(k)
            correlation = corr(parameter_list[i], parameter_list[j],master)
            print(correlation)
            if correlation > 0.5:
                outfile.write('{:s} {:s} {:d}'.format(parameter_list[i], parameter_list[j],correlation))
    outfile.close()

def correlation_txt(file_name:str):
    infile = open('spiralgalaxies.txt','r')
    parameter_list = infile.readline().strip('\n').split('\t')
    infile.close()
    outfile = open('tsv_correlations.txt','w')
    print(parameter_list)
    print('The number of variables: ' + str(len(parameter_list)))
    counter = 0
    for var1 in parameter_list:
        counter += 1
        print('The current variable:' + str(counter))
        for var2 in parameter_list:
            read_data('spiralgalaxies.txt', var1, var2,'')
            print('Checkpoint')
            
            correlation = corr(var1,var2,master)
            print(correlation)
            if correlation > 0.5:
                outfile.write('{:s} {:s} {:d}'.format(var1,var2,correlation))
    outfile.close()
            
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
            print(sub_data)
            print(param_index)
            print(line[0])
            master[line[0]] = galaxy_in(sub_data, param_index)
    print("File read in succesfully")
    

def read_tsv(filename:'str') -> 'list of str':
    '''Reads the TSV file and writes the spiral galaxy subset to file (for later use).'''
    '''Writes the file by printing the variable names first, then separate by a line of asterisks.'''
    with open(filename, 'r') as f:
        lines = []
        first_line = f.readline().split("\t") # read in the variable 
        information = {key: [] for key in first_line} # dictionary of variable lists (galaxies horizontally)
        n = 0
        for line in f:
            n+=1
            if n >= 1000: #REMOVE LATER
                print('Temporary cut for testing.')
                break
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
            for name in first_line:
                outfile.write(information[key][index] + '\t')
            outfile.write('\n') 
        outfile.close()
        return first_line

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

def files(number: int):
    result = []
    if number == 1:
        result.append(input("What is the name of the file: "))
    elif number > 1:
        result = []
        result.append(input("What is the name of the first file: "))
        for i in range(number-1):
            result.append(input("What is the name of the next file: "))
    for file in result:
        if not os.path.isfile(file):
            raise FileNotFoundError
    print("Files to be use: "+str(result))
    return result

def corr(x_key: 'key', y_key: 'key', galaxies: dict) -> float:
        '''Takes two lists of x,y to calculate the 2D Pearson correlation.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        correlations = pearsonr(x,y)
        return correlations[0]

def retrieve_dict_vector(d:dict,key:str) -> 'list of float':
        '''Returns a list of all features across every example in d given a key.'''
        vector = []
        for example_key in d.keys():
                print('Passed key: ' + key)
                print('Current key: ' + example_key)
                vector.append(float(d[example_key][key]))
        return vector


correlation_finder()
