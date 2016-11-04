class Data:
    def __init__(self, path, labels=False):
        from matrix import GenMat
        if type(path) == dict:
            self.as_dict = path
            self.var_names = [name for name in self.as_dict.keys()]
            self.numrows = len(self.as_dict[self.var_names[0]])  
            self.numcols = len(self.var_names)
            self.matrix = GenMat([self.as_dict[name] for name in self.var_names])
            
        else:
        
            datafile = open(path)
            chopped = [line.split(',') for line in datafile.readlines()]
        
            self.columns = [[chopped[i][j].strip() for i in range(len(chopped))] for j in range(len(chopped[0]))]
        
            if labels:
                self.var_names = [name.strip() for name in chopped[0]]
                for col in self.columns:
                    del col[0]
            else:
                self.var_names = input('Enter variable names separated by commas without spaces in between (match order to dataset):\t').split(',')
        
            self.as_dict = {name:col for (name, col) in list(zip(self.var_names, self.columns))}
        
            self.numrows = len(self.as_dict[self.var_names[0]])  
            self.numcols = len(self.var_names)
            
            self.matrix = GenMat([self.as_dict[name] for name in self.var_names])
    
    #Pull out an entire column 
    def __getitem__(self, var):
        return self.as_dict[var]
        
    def __setitem__(self, new_var, new_data):
        if new_var in self.as_dict:
            self.as_dict[new_var] = new_data
        else:
            self.var_names.append(new_var)
            self.as_dict[new_var] = new_data 
           
    #Leave specified variables as string variables (rest are converted to numeric format)    
    def as_string(self, *vars):
        for var in self.var_names:
            if var not in vars:
                self.as_dict[var] = ['--' if x=='' else float(x) for x in self.as_dict[var]]
            else:
                self.as_dict[var] = ['--' if x=='' else x for x in self.as_dict[var]]
    
    #Remove observations with missing values 
    def rm(self):
        missing_count = 0 
        for i in range(len(self.var_names)):
            count = 0
            for x in self.as_dict[self.var_names[i]]:
                if x == '--':
                    for i in range(len(self.var_names)):
                        del self.as_dict[self.var_names[i]][count]
                    count += 1
                    missing_count += 1 
                else:
                    count += 1 
                    pass 
                    
        self.numrows = len(self.as_dict[self.var_names[0]])
        print('%r observations removed due to missing data on one or more variables' % missing_count)
    
    #Returns a subset of the data containing all data points for which a variable (col) has a given value 
    def subset(self, var, value):
        sbset = self.as_dict.copy()
        count = len(sbset[var])
        for i in range(count):
            if sbset[var][i] != value:
                for name in [name for name in self.var_names if not name == var]:
                    del sbset[name][i]
                    count -= 1 
            else: 
                pass
        return sbset 
        
    def __repr__(self):
        out = open('c:/users/will/desktop/output.txt', 'w')
        for x in range(self.numrows):
            for n in range(len(self.var_names)):
                if x == 0:
                    if n == len(self.var_names)-1:
                        out.write('%r\n' %self.var_names[n])
                        for n in range(len(self.var_names)):
                            if n == len(self.var_names)-1:
                                out.write('%r\n' %self.as_dict[self.var_names[n]][x])
                            else:
                                out.write('%r\t' %self.as_dict[self.var_names[n]][x])
                    else:
                        out.write('%r\t' %self.var_names[n])
                elif x == self.numrows-1:
                    if n == len(self.var_names)-1:
                        out.write('%r\n' %self.as_dict[self.var_names[n]][x])
                        out.close()
                    else:
                        out.write('%r\t' %self.as_dict[self.var_names[n]][x])
                else:
                    if n == len(self.var_names)-1:
                        out.write('%r\n' %self.as_dict[self.var_names[n]][x])
                    else:
                        out.write('%r\t' %self.as_dict[self.var_names[n]][x])
           
        return 'Data sent to desktop' 
    
    #Creates a level:label dictionary for all unique levels of a factor variable 
    #If toggle is set to True, displays the entries in the factor column as their assigned labels 
    def factor(self, var, toggle=False):
        levels = set() 
        pairs = []
        for obs in self.as_dict[var]:
            levels.add(obs)
        for level in levels:
            label = input('Enter label for level = %r\t' %level)
            pairs.append((level, label))
            
        as_dict = {k:v for (k,v) in pairs}
        
        if toggle:
            self[var] = [as_dict[x] for x in self[var]]
            
        return as_dict 




        
        
                    
                
   
                
       
