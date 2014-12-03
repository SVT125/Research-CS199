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

read_tsv('SF5+PetroRads+GZ1+Banerji+photoz.tsv')
