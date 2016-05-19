'''This script defines a class Vec used to represent and model the properties of n-vectors. 
Inspired by Philip Klein's code found in Coding the Matrix: Linear Algebra through Computer
Science Applications. It also defines a function for calculating the angle between any two
n-vectors'''

class Vec:
    
    #Vector has a dictionary form and a list form 
    def __init__(self, L):
        self.as_dict = {k:v for (k,v) in list(enumerate(L))}
        self.as_list = list(self.as_dict.values())
        
    #Vector presents as Vec[v1, v2, . . ., vn]   
    def __repr__(self):
        return 'Vec%r' %(self.as_list)
            
    def __len__(self):
        return len(self.as_list)
    
    def __getitem__(self, i):
        return self.as_dict[i]
        
    #Does not allow negative index assignments 
    #If index is within length of vector, substitutes new value in place of old value 
    #If index is +1 the length of the vector, appends new value onto the end of vector 
    #If index is >+1 the length of the vector, fills in gap with zeros 
    def __setitem__(self, i, value):
        if i < 0: print('ERROR: Index cannot be negative!')
        else:
            self.as_dict[i] = value
            try:
                self.as_list[i] = value
            except IndexError:
                if i == len(self.as_list):
                    self.as_list.append(value)
                elif i > len(self.as_list):
                    zeros = i - len(self.as_list)
                    for x in range(zeros):
                        self.as_list.append(0)
                    self.as_list.append(value)
    
    #Tests whether two vectors have the same entries in the same positions 
    def __eq__(self, other):
        if self.as_dict == other.as_dict:
            return True
        else:
            return False 
    
    #Vector membership test 
    def __contains__(self, entry):
        if entry in self.as_list:
            return True
        else:
            return False 
        
    #Returns magnitude (aka. length, norm, etc.) of the vector in n-dimensional space     
    def mag(self):
        import math
        return math.sqrt(sum([v**2 for v in self.as_list]))
        
    #Addition of two vectors 
    def __add__(self, other):
        if len(self) != len(other): print('ERROR: Cannot add vectors of different lengths')
        else:
            summed = [x+y for (x,y) in list(zip(self.as_list, other.as_list))]
            return Vec(summed)
    __radd__ = __add__   #Same left-to-right as right-to-left (commutative)
    
    #Subtraction of two vectors 
    def __sub__(self, other):
        if len(self) != len(other): print('ERROR: Cannot subtract vectors of different lengths')
        else:
            minused = [x-y for (x,y) in list(zip(self.as_list, other.as_list))]
            return Vec(minused)
        
    #Multiplication     
    def __mul__(self, other):
        
        #Scalar-vector multiplication ([kv1, kv2, . . ., kvn])
        if isinstance(other, int) or isinstance(other, float):
            product = [other*v for v in self.as_list]
            return Vec(product)
        
        #Vector-vector multiplication (returns dot product)
        elif isinstance(other, Vec):
            if len(self) != len(other): print('ERROR: Cannot multiply vectors of different lengths')
            else:
                dotproduct = sum([x*y for (x,y) in list(zip(self.as_list, other.as_list))])
                return dotproduct 
    __rmul__ = __mul__

#Calculates the angle between any two n-vectors in n-dimensional space      
def angle(vector1, vector2):
    from math import acos, degrees
    arccos = acos((vector1*vector2)/(vector1.mag()*vector2.mag()))
    return '%r radians; %r degrees' %(arccos, degrees(arccos))

    

        


    