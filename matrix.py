class V:
    def __init__(self, L):
        self.as_list = [[x] if isinstance(x, complex) else [float(x)] for x in L]
        self.as_dict = {k:v for (k,v) in list(enumerate(L))}
        
    def __repr__(self):
        from texttools import lprint
        M=0
        for row in range(len(self.as_list)):
            for col in range(len(self.as_list[row])):
                if len(str(round(abs(self.as_list[row][col]), 2))) > M:
                    M=len(str(round(abs(self.as_list[row][col]), 2)))
                else:
                    pass
        combined = ''
        for sublist in self.as_list:
            pretty = lprint([round(x,2) for x in sublist], M)
            combined += pretty + '\n'*2
        return combined
        
    def __len__(self):
        return len(self.as_list)
        
    def __getitem__(self, i):
        return self.as_list[i][0]
    
    def __iter__(self):
        for x in self.as_list:
            yield x[0]
            
    def __setitem__(self, i, value):
        if i < 0: print('ERROR: Index cannot be negative!')
        else:
            self.as_dict[i] = value
            try:
                self.as_list[i] = [value]
            except IndexError:
                if i == len(self.as_list):
                    self.as_list.append([value])
                elif i > len(self.as_list):
                    zeros = i - len(self.as_list)
                    for x in range(zeros):
                        self.as_list.append([0])
                    self.as_list.append([value])
                    
    def __eq__(self, other):
        if self.as_dict == other.as_dict:
            return True
        else:
            return False
            
    def __contains__(self, entry):
        if entry in self.as_list:
            return True
        else:
            return False
    
    #Returns position index of first non-zero element (if zero vector, returns one more than the number of elements)
    def first_nonzero(self):
        for i in range(len(self.as_list)):
            if abs(self.as_list[i][0]) >= .0000000001:
                pos = i
                return pos
            else:
                pass  
        return len(self.as_list)+1 
    
    #Returns first non-zero element 
    def leading_entry(self):
        if self.first_nonzero() == len(self.as_list)+1:
            return 0 
        else:
            return self.as_list[self.first_nonzero()][0]
    
    #Returns 2-norm (i.e. square root of the sum of squared elements)
    def norm2(self):
        import math
        return math.sqrt(sum([v[0]**2 for v in self.as_list]))
    
    #Returns normalized vector (i.e. 2-norm equals 1)
    def normalize(self):
        return V([(1/self.norm2())*element for element in self])
    
    #Returns vector transpose as a single row matrix 
    def transpose(self):
        global M 
        return M([[x[0] for x in self.as_list]])
            
    #Addition of two vectors 
    def __add__(self, other):
        if len(self) != len(other): print('ERROR: Cannot add - dimensions do not match')
        else:
            return V([x[0]+y[0] for (x,y) in list(zip(self.as_list, other.as_list))])
    __radd__ = __add__   #Same left-to-right as right-to-left (commutative)
    
    #Vector subtraction 
    def __sub__(self, other):
        if len(self) != len(other): print('ERROR: Cannot add - dimensions do not match')
        else:
            return V([x[0]-y[0] for (x,y) in list(zip(self.as_list, other.as_list))])
        
    #Scalar multiplication and vector-matrix multiplication 
    def __mul__(self, other):
        global M
        if isinstance(other, int) or isinstance(other, float):
            return V([x[0]*other for x in self.as_list])
        elif isinstance(other, M):
            if len(other.as_list) == 1:   #Outer product is default when other is a 1xn matrix 
                return M([x for x in self.as_list])*other 
            elif len(self) != len(other.as_list):
                print('ERROR: Cannot multiply - dimensions do not match')
            else:
                return self.transpose()*other
        elif isinstance(other, V):   #Inner product is default when other is a vector 
            return self.inner(other) 
    
    #Inner product 
    def inner(self, other):
        global M
        if isinstance(other, V) and len(self)==len(other):
            return self.transpose()*M([x for x in other.as_list])
        elif not isinstance(other, V):
            print('ERROR: The argument must be a vector')
        elif len(self) != len(other):
            print('ERROR: Inner product requires that dimensions match') 
    
    #Outer product        
    def outer(self, other):
        global M
        if isinstance(other, V) and len(self)==len(other):
            return M([x for x in self.as_list])*other.transpose()
        elif not isinstance(other, V):
            print('ERROR: The argument must be a vector')
        elif len(self) != len(other):
            print('ERROR: Outer product requires that dimensions match') 
        
    


class M:

    def __init__(self, L):
        from vectors import Vec 
        
        self.as_list = [[x if isinstance(x, complex) else float(x) for x in sub] for sub in L]
        
        self.rows = len(self.as_list)
        self.cols = len(self.as_list[0])
        
        self.rowvecs = [Vec(row) for row in self.as_list]
        self.colvecs = [Vec([self.rowvecs[i][j] for i in range(len(self.rowvecs))]) for j in range(len(self.rowvecs[0]))]
        
        self.indices = list(range(len(self.rowvecs)))
        self.nonzeros = [vec.first_nonzero() for vec in self.rowvecs]
        
    def __repr__(self):
        from texttools import lprint
        M=0
        for row in range(len(self.as_list)):
            for col in range(len(self.as_list[row])):
                if len(str(round(abs(self.as_list[row][col]), 2))) > M:
                    M=len(str(round(abs(self.as_list[row][col]), 2)))
                else:
                    pass
        combined = ''
        for sublist in self.as_list:
            pretty = lprint([round(x,2) for x in sublist], M)
            combined += pretty + '\n'*2
        return combined 
        
    def __getitem__(self, i):
        return self.as_list[i]
    
    def __iter__(self):
        for x in self.as_list:
            yield x 
            
    def transpose(self):
        return M([col.as_list for col in self.colvecs])      
        
    def is_square(self):
        if self.rows == self.cols:
            return True 
        else:
            return False 
            
    def diag(self):
        if self.is_square():
            return [self.as_list[i][i] for i in range(len(self.as_list))]
        else:
            return False
                
    def trace(self):
        if self.is_square():
            return sum(self.diag())
            
    #Returns Frobenius norm (i.e. sqrt of the sum of squared entries)
    def norm(self):        
        from math import sqrt
        return sqrt(sum([row.mag()**2 for row in self.rowvecs]))
                
    def __add__(self, other):
        if (self.rows == other.rows) and (self.cols == other.cols):
            summed = [[self.as_list[i][j] + other.as_list[i][j] for j in range(len(self.as_list[0]))] for i in range(len(self.as_list))]
        return M(summed) 

    def __mul__(self, other):
        from vectors import Vec 
        global M
        
        #Scalar product 
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return M([[other*element for element in sub] for sub in self.as_list])
    
        #Matrix-vector multiplication 
        if isinstance(other, Vec):
            if len(other) == len(self.as_list[0]):
                product = [sum([x*y for (x,y) in list(zip(self.as_list[i], other.as_list))]) for i in range(len(self.as_list))]
                return Vec(product)
            else:
                print('ERROR: Number of columns in matrix must match vector length')
        
        #Matrix-matrix multiplication
        if isinstance(other, M):
            if self.cols == other.rows:
                return M([[self.rowvecs[i]*other.colvecs[j] for j in range(other.cols)] for i in range(self.rows)])
        
    def __pow__(self, other):
        exp = M(self.as_list)
        for n in range(other-1):
            exp *= self 
        return exp 
        
    #Multiply a row by a scalar 
    def scale_row(self, row, scalar):
        self.rowvecs[row-1]*=scalar
        for i in range(len(self.colvecs)):
            self.colvecs[i][row-1]*=scalar 
        self.as_list = [vec.as_list for vec in self.rowvecs]
    
    #Multiply a row by a scalar and add the product to another row 
    def scale_and_combine(self, scalar, r1, r2):
        self.rowvecs[r2-1]+=(scalar*self.rowvecs[r1-1])
        for i in range(len(self.colvecs)):
            self.colvecs[i][r2-1]+=self.colvecs[i][r1-1]*scalar 
        self.as_list = [vec.as_list for vec in self.rowvecs]
    
    #Swap two rows 
    def swap(self, r1, r2):
        from vectors import Vec 
        copied = Vec(self.rowvecs[r1-1]) 
        self.rowvecs[r1-1] = self.rowvecs[r2-1]
        self.rowvecs[r2-1] = copied
        for i in range(len(self.colvecs)):
            copieditem = self.colvecs[i][r1-1]
            self.colvecs[i][r1-1] = self.colvecs[i][r2-1]
            self.colvecs[i][r2-1] = copieditem 
        self.as_list = [vec.as_list for vec in self.rowvecs]
    
    #Returns an identity matrix of the same dimension as the given matrix.
    def id(self):
        return M([[1 if j==i else 0 for j in range(len(self.as_list[i]))] for i in range(len(self.as_list))])
    
    #Rearranges the rows of the matrix so that leading non-zero entries are descending ("upside-down staircase")
    #Returns a modified identity matrix with corresponding row swaps.
    def descending(self):
        from vectors import Vec 
        by_first_nonzero = list(zip(self.nonzeros, [nested for nested in self.as_list], [id_row for id_row in self.id()]))
        self.as_list = [nest for (ind, nest, id_row) in sorted(by_first_nonzero)]
        new_identity = M([id_row for (ind, nest, id_row) in sorted(by_first_nonzero)])
        self.rowvecs = [Vec(row) for row in self.as_list]
        self.colvecs = [Vec([self.rowvecs[i][j] for i in range(len(self.rowvecs))]) for j in range(len(self.rowvecs[0]))]
        self.indices = list(range(len(self.rowvecs)))
        self.nonzeros = [vec.first_nonzero() for vec in self.rowvecs]
        return new_identity
    
    #Looks for repeating rows and turns each repeat into a zero vector.  
    def elim_repeats(self):
        from vectors import Vec 
        past = [] 
        for l in range(len(self.as_list)):
                if self.as_list[l] in past:
                    self.as_list[l] = [0*x for x in self.as_list[l]]
                else:
                    past.append(self.as_list[l])
        self.rowvecs = [Vec(row) for row in self.as_list]
        self.colvecs = [Vec([self.rowvecs[i][j] for i in range(len(self.rowvecs))]) for j in range(len(self.rowvecs[0]))]
        self.indices = list(range(len(self.rowvecs)))
        self.nonzeros = [vec.first_nonzero() for vec in self.rowvecs]
     
    #Returns matrix in echelon form using Gaussian reduction.
    def echelon(self):
        i=0;column=0
        offlimits = []
        new = M(self.as_list) 
        while i<len(new.as_list):
            
            new.elim_repeats()
            
            row = new.as_list[i]
            try:
                if new.as_list[i][column] != 0 and new.as_list[i] not in offlimits:
                    pivot = new.as_list[i][column]
                    for k in new.as_list[i+1:]:
                        if k not in offlimits:
                            multiplier = (-1*k[column])/(new.as_list[i][column])
                            new.scale_and_combine(multiplier, new.as_list.index(new.as_list[i])+1, new.as_list.index(k)+1)
                        else:
                            pass 
                    
                    offlimits.append(new.as_list[i])
                    column += 1
                    i += 1
                    
                elif row[column] != 0 and row in offlimits:
                    i += 1 
                    
                elif row[column] == 0:
                    start = 1
                    while new.as_list.index(row)<len(new.as_list):

                        try:
                            row = new.as_list[i+start]
                            if row[column] != 0 and row not in offlimits:
                                pivot = new.as_list[i+start][column]
                                for k in new.as_list[i+start+1:]:
                                    if k not in offlimits:
                                        multiplier = (-1*k[column])/(new.as_list[i+start][column])
                                        new.scale_and_combine(multiplier, new.as_list.index(row)+1, new.as_list.index(k)+1)
                                    else:
                                        pass 
                                column += 1
                                i = 0
                                offlimits.append(row)
                                break
                            elif row[column] != 0 and row in offlimits and new.as_list.index(row)<len(new.as_list)-1:
                                start += 1 
                                continue 
                            elif row[column] != 0 and row in offlimits and new.as_list.index(row)==len(new.as_list)-1 and column<len(row)-1:
                                column += 1
                                break 
                            elif (row[column] == 0) and new.as_list.index(row)<len(new.as_list)-1:
                                start += 1
                                continue
                            elif (row[column] == 0) and (new.as_list.index(row)==len(new.as_list)-1) and (column<len(row)-1):
                                column += 1 
                                break
                           

                        except IndexError:
                            i+=1
                            break
                else:
                    break 
            except IndexError:
                break
        
        return new 
    
    #Returns the matrix inverse.
    def inverse(self):
        from vectors import Vec 
        i=0;column=0
        offlimits = []
        invofflimits = []
        new = M(self.as_list)
        
        #prevents unnecessary row swapping if all rows begin with nonzero entries 
        if sum(new.nonzeros) == 0:
            inv = new.id()
        else:
            inv = new.descending() 

        while i<len(new.as_list):
                
            new.elim_repeats()
            
            row = new.as_list[i]
            try:
            
                if new.as_list[i][column] != 0 and new.as_list[i] not in offlimits:
                    multipliers = [] 
                    for k in new.as_list[i+1:]:
                        if k not in offlimits:
                            multiplier = (-1*k[column])/(new.as_list[i][column])
                            new.scale_and_combine(multiplier, new.as_list.index(new.as_list[i])+1, new.as_list.index(k)+1)
                            multipliers.append(multiplier)
                        else:
                            pass 
                    
                    
                    for (m, v) in list(zip(multipliers, inv.as_list[i+1:])):
                        if v not in invofflimits:
                            inv.scale_and_combine(m, inv.as_list.index(inv.as_list[i])+1, inv.as_list.index(v)+1)                    
                        else:
                            pass
                    
                    offlimits.append(new.as_list[i]); invofflimits.append(inv.as_list[i])
                    column += 1
                    i += 1
                                       
                elif row[column] != 0 and row in offlimits:
                    i += 1 
                    
                elif row[column] == 0:
                    start = 1
                    while new.as_list.index(row)<len(new.as_list):

                        try:
                            row = new.as_list[i+start]
                            if row[column] != 0 and row not in offlimits:
                                multipliers = [] 
                                for k in new.as_list[i+start+1:]:
                                    if k not in offlimits:
                                        multiplier = (-1*k[column])/(new.as_list[i+start][column])
                                        new.scale_and_combine(multiplier, new.as_list.index(row)+1, new.as_list.index(k)+1)
                                        multipliers.append(multiplier)
                                        
                                    else:
                                        pass 
                                
                                for (m, v) in list(zip(multipliers, inv.as_list[i+start+1:])):
                                    if v not in invofflimits:
                                        inv.scale_and_combine(m, inv.as_list.index(inv.as_list[i])+1, inv.as_list.index(v)+1)                                
                                   
                                    else:
                                        pass
                                
                                column += 1
                                i = 0
                                offlimits.append(row); invofflimits.append(inv.as_list[i+start])
                                break
                            elif row[column] != 0 and row in offlimits and new.as_list.index(row)<len(new.as_list)-1:
                                start += 1 
                                continue 
                            elif row[column] != 0 and row in offlimits and new.as_list.index(row)==len(new.as_list)-1 and column<len(row)-1:
                                column += 1
                                break 
                            elif (row[column] == 0) and new.as_list.index(row)<len(new.as_list)-1:
                                start += 1
                                continue
                            elif (row[column] == 0) and (new.as_list.index(row)==len(new.as_list)-1) and (column<len(row)-1):
                                column += 1 
                                break
                           

                        except IndexError:
                            i+=1
                            break
                else:
                    break 
            except IndexError:
                break
        
        i = len(new.as_list)-1; column = new.rowvecs[-1].first_nonzero()
               
        while i >= 0:
            
            multinv = (1/new.as_list[i][column])
            new.scale_row(i+1, multinv)
            inv.scale_row(i+1, multinv)
            
            multipliers = [] 
            for k in new.as_list[:i]:
                multiplier = (-1*k[column]) 
                new.scale_and_combine(multiplier, i+1, new.as_list.index(k)+1)
                multipliers.append(multiplier)
                

            for (m, v) in list(zip(multipliers, inv.as_list[:i])):
                inv.scale_and_combine(m, inv.as_list.index(inv.as_list[i])+1, inv.as_list.index(v)+1)
            
            i -= 1 
            column = new.rowvecs[i].first_nonzero()
          
        return inv    
    #Returns the rank of the matrix.
    def rank(self):
        new = self.echelon() 
        independent = 0
        for row in new.rowvecs:
            if row.first_nonzero() < len(row):
                independent += 1 
            else:
                pass 
        return independent
    
    #Determinant function - takes account of row swaps by changing the sign of the determinant.
    def det(self):
        from vectors import Vec 
        if self.is_square():
            
            descend = Vec(self.echelon().indices)
            displaced = descend - Vec(self.echelon().nonzeros)
            if max([abs(x) for x in displaced])%2 == 0:
                
                product = 1 
                for element in [vec.leading_entry() for vec in self.echelon().rowvecs]:
                    product *= element 
                return product 
                
            elif max([abs(x) for x in displaced])%2 == 1:
            
                product = 1 
                for element in [vec.leading_entry() for vec in self.echelon().rowvecs]:
                    product *= element 
                return -1*product 
        else:
            print('Determinant does not exist for non-square matrices')
    
    #Returns the row,col minor of the matrix by deleting the specified row and column.
    def minor(self, row, col):
        new = M([[n for n in self.as_list[i] if not n is self.as_list[i][col-1]] for i in range(len(self.as_list)) if not self.as_list[i] is self.as_list[row-1]])
        return new 
    
    #Returns the row,col cofactor of the matrix.
    def cofactor(self, row, col):
        return ((-1)**(row+col))*self.minor(row,col).det() 
    
    #Returns the matrix adjoint to a given square matrix.
    def adjoint(self):
        adj = M([[self.cofactor(r+1,c+1) for r in range(len(self.as_list))] for c in range(len(self.as_list[0]))])
        return adj 
            
            


#Factors an input matrix A into an orthogonal matrix Q and an upper-triangular matrix R       
def QR(A):
    from vectors import proj_line, Vec
    I = M([[1 if j==i else 0 for j in range(A.cols)] for i in range(A.cols)])
    
    basis = []
    basis.append(A.colvecs[0])
    for i in range(len(A.colvecs[1:])):
        projs = []
        for b in range(len(basis)):
            projection = proj_line(A.colvecs[1:][i], basis[b])[0]
            coeff = proj_line(A.colvecs[1:][i], basis[b])[1]
            projs.append(projection)
            
            I.scale_and_combine(coeff*-1, b+1, i+2)
            
        orthogonalized = A.colvecs[1:][i]
        for projection in projs:
            orthogonalized -= projection
        basis.append(orthogonalized)
    
    for i in range(len(basis)):
        norm = basis[i].mag()
        
        I.scale_row(i+1, 1/norm)
        
    Q = A*I.transpose()
    R = I.transpose().inverse()
    product = Q*R
    
    return A,Q,R
