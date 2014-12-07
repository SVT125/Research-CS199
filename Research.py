from collections import namedtuple
import os.path
#import pyfits
#from mpl_toolkits.mplot3d import Axes3D
#from scipy.stats.stats import pearsonr
#import matplotlib
#import matplotlib.pyplot as plt

#todo:  find actual correlaations and the files associated with them, check for same galaxy names across files
#       make tsv file read in, in this file
#       find interesting correlations
#       make it so you can read multiple files, assume all galaxy names are consistent (see 1)
#       clean this file up


def read_tsv(filename:'str') -> None:
        '''Reads the TSV file and writes the spiral galaxy subset to file (for later use).'''
        '''Writes the file by printing the variable names first, then separate by a line of asterisks.'''
        f = open(filename,"r")
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
        f.close()

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


parameters = []
master = {} #A dictionary with the key as the name and the value as a 
            #Galaxy dict with each key value pair as a variable name and value
str_params = ''
x=[]
y=[]
z=[]

def setup(files):
    global master, x, y, z, file_name
    print("""Please input the coordinate value names. Note: if you press enter without 
declaring a z value the program will continue as a 2 dimensional correlation. Also,
please ensure that all values are the exact names as written in the data file.""")
    while True:
        x_value = input("What is the x coordinate value name: ").strip()
        y_value = input("What is the y coordinate value name: ").strip()
        z_value = input("What is the z coordinate value name: ").strip()
        break
    for file_name in files:
        try:
            if file_name.find('.fit') != -1:
                read_fits_data(file_name, x_value, y_value, z_value)
            elif file_name.find('.txt') != -1:
                read_data(file_name, x_value, y_value, z_value)
            elif file_name.find('.tsv') != -1:
                read_tsv(file_name)
                read_data('{}.txt'.format(file_name[0:-4]), x_value, y_value, z_value)
            for k,v in sorted(master.items()):
                x.append(v[x_value])
                y.append(v[y_value])
                if z_value != '':
                    z.append(v[z_value])
        except KeyError as err:
            print("{} was not found in file {}".format(err,file_name))
            setup(files)
    return

def galaxy_in(data:[str], param_index:[int]):
    galaxy={}
    for index in range(len(data)):
        try:
            galaxy[parameters[param_index[index]]] = int(data[index])
        except:
            galaxy[parameters[param_index[index]]] = data[index]
    return galaxy

def fits_galaxy_in(data, param_index): #working on this now
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
            line=line[:-1].split('\t')
            for index in range(len(line)):
                if parameters[index]==x_value:
                    sub_data[0]=line[index]
                elif parameters[index]==y_value:
                    sub_data[1]=line[index]
                elif parameters[index]==z_value:
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
    for line in data:
        print("Reading in galaxy "+str(line[0]))
        line=line[:-1].split('\t')
        for index in range(len(line)):
            if parameters[index]==x_value:
                sub_data[0]=line[index]
            elif parameters[index]==y_value:
                sub_data[1]=line[index]
            elif parameters[index]==z_value:
                sub_data[2]=line[index]
        master[line[0]] = fits_galaxy_in(sub_data, param_index)
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
    print(result)
    return result

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
    print()
    print(master.items()) #check
    print()
    print(parameters) #check
    print()
    print(x,y,z) #check
    #plot(x_value, y_value, z_value, master)
