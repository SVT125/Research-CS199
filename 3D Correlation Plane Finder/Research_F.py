from collections import namedtuple
import os.path
import pyfits
from scipy.stats.stats import pearsonr
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    while True:
        x_value = input("What is the x coordinate value name: ").strip()
        y_value = input("What is the y coordinate value name: ").strip()
        z_value = input("What is the z coordinate value name: ").strip()
        break
    done = False
    for file_name in files:
        try:
            if file_name.find('.fit') != -1:
                read_fits_data(file_name, x_value, y_value, z_value)
            elif file_name.find('.txt') != -1:
                infile = open('varnamest.txt','r')
                params = infile.readlines()
                params2 = params
                params = params[90:]
                print('Number of parameters: ' + str(len(params)))
                counter = 0
                corrfile = open('results.txt','w')
                for v1 in params:
                        for v2 in params2:
                            try:
                                read_data(file_name, v1.strip('\n'), v2.strip('\n'), z_value)
                                correlation = corr(v1.strip('\n'),v2.strip('\n'),master)
                                if(abs(correlation) > 0.2):
                                    print('Correlation: ' + str(correlation) + '\t' + v1 + '\t' + v2)
                                    corrfile.write(v1 + '' + v2 + '' + str(correlation) + '\n\n')
                                    corrfile.flush()
                            except Exception as e:
                                print(e)
                                print('Skipping... ' + str(counter))
                                counter += 1
                                continue
                corrfile.close()
            elif file_name.find('.tsv') != -1:
                read_tsv(file_name)
                read_data('{}.txt'.format(file_name[0:-4]), x_value, y_value, z_value)
            else:
                print("File "+file_name+" is not a supported file type\n"+
                      "Supported file types include: .fit .fits .tsv .txt")
                return
            for k,v in sorted(master.items()):
                x.append(v[x_value])
                y.append(v[y_value])
                if z_value != '':
                    z.append(v[z_value])
            done = True
        except KeyError as err:
            print("{} was not found in file {}".format(err,file_name))
    if not done:
        print("One or more of the specified values was not found in any given file")
        setup(files)
    print('Correlation: ' + str(corr(x_value,y_value,master)))
    return

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
    print(parameter_list)
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
    for line in data and galaxy_count <= 100:
        galaxy_count += 1
        print("Reading in galaxy "+str(line[32]))
            #if parameters[index]==x_value:
        sub_data[0]=line[x_value]
            #elif parameters[index]==y_value:
        sub_data[1]=line[y_value]
            #elif parameters[index]==z_value:
        if z_value != '':
            sub_data[2]=line[z_value]
        master[line[32]] = fits_galaxy_in(sub_data, param_index)
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

def plot(x_key:'key',y_key:'key', galaxies:dict, labels=None) -> None:
        '''Plots the lists xy in a 2D graph.'''
        x = retrieve_dict_vector(galaxies,x_key)
        y = retrieve_dict_vector(galaxies,y_key)
        plt.scatter(x,y)
        if labels != None:
                pass #outliers with labels
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
    while True:
        try:
            check = int(input("How many files will be used? "))
            if check >=1:
                file = files(check)
                setup(file)
                break
            else:
                print("Number of files must be 1 or more")
                continue
            break
        except (ValueError):
            print("Error: you must input an integer greater than 0")
            continue
        except (FileNotFoundError):
            print("Error: one or more of the specified files either does not exist of is not in this directory")
            continue
        
    #print(str_params) #not written
    #plot(x_value, y_value, z_value, master)
