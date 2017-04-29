""" A module designed to provide useful operations involving matrices that may
    be used in a manner similar to that of MATLAB. 
    Author: Marc Katzef
    Date: 24/3/2016
"""


class Array:
    def __init__(self, rowNumber, columnNumber, entryList=[]):   
        """Initializes an object of class Array. The given rowNumber and 
        columnNumber determine the dimensions of the array. entryList determines
        the values to be placed in the array from left to right and top to
        bottom. If no entryList is provided, all entries are set to 0. The given
        entryList must be of length (rowNumber * columnNumber)"""
        self.matrix = []
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        
        if len(entryList) == 0:
            entryList = [0] * rowNumber * columnNumber

        if len(entryList) != rowNumber * columnNumber:
            raise ValueError('Given array does not conform to given dimensions')
        else:
            for row in range(rowNumber):
                currentRow = []
                for column in range(columnNumber):
                    currentRow.append(entryList[row * columnNumber + column])
                self.matrix.append(currentRow)
    
    
    def __repr__(self):
        """Presents an array in a 2D grid with each number to two decimal
        places, and of column widths determined by the widest in this format"""
        entryLengths = []
        for row in self.matrix:
            for entry in row:
                entryLengths.append(len('{:.2f}'.format(entry)))
        
        template = '{:>' + str(max(entryLengths) + 2) + '.2f}'
        returnString = ''
        for row in self.matrix:
            counter = 1
            for entry in row:
                text = template.format(entry)
                if counter == self.columnNumber:
                    returnString += text + '\n'
                else:
                    returnString += text
                counter += 1
                
        return returnString[:-1]
    
    
    def getEntry(self, row, column):
        """Gets the value of the entry of the array at location row, column"""
        return self.matrix[row][column]
        
        
    def changeEntry(self, row, column, newValue):
        """Sets the value of the entry of the array at location row, column to
        newValue"""
        newRow = self.matrix[row]
        newRow[column] = newValue
        self.matrix[row] = newRow


    def vectorMult(self, vector1, vector2):
        """Multiplies the corresponding entries of each of the two given vectors
        to produce a new vector. Used as a helper function for __mul__.
        The given vectors must be of the same length"""
        products = []
        for i in range(len(vector1)):
            products.append(vector1[i] * vector2[i])
        return sum(products)
    
        
    def __mul__(self, other):
        """Carries out matrix multiplication with other and self to produce a
        new array. The inner dimensions of self and other must be the same"""
        if isinstance(other, Array):
            leftInnerDim = self.columnNumber
            rightInnerDim = other.rowNumber
            if leftInnerDim != rightInnerDim:
                raise ValueError('Given arrays do not conform for matrix multiplication')
            
            result = Array(self.rowNumber, other.columnNumber)
            for row in range(result.rowNumber):
                for column in range(result.columnNumber):
                    multRow = self.matrix[row]
                    multColumn = [row[column] for row in other.matrix]
                    result.changeEntry(row, column, self.vectorMult(multRow, multColumn))
                    
        else:
            result = Array(self.rowNumber, self.columnNumber)
            for row in range(self.rowNumber):
                for column in range(self.columnNumber):
                    newValue = self.matrix[row][column] * other
                    result.changeEntry(row, column, newValue)           

        return result
    
    
    def __sub__(self, other):
        """Subtracts the value of each entry of array 'other' from the value of
        each corresponding entry of 'self' to produce a new array.
        The dimensions of self and other must be the same"""
        if isinstance(other, Array):
            if self.rowNumber != other.rowNumber or self.columnNumber != other.columnNumber:
                raise ValueError('Arrays do not conform for matrix subtraction')
                
            result = Array(self.rowNumber, self.columnNumber)
            for row in range(self.rowNumber):
                for column in range(self.columnNumber):
                    newValue = self.matrix[row][column] - other.matrix[row][column]
                    result.changeEntry(row, column, newValue)
        
        else:
            result = Array(self.rowNumber, self.columnNumber)
            for row in range(self.rowNumber):
                for column in range(self.columnNumber):
                    newValue = self.matrix[row][column] - other
                    result.changeEntry(row, column, newValue)            
            
        return result
    
    
    def deepCopy(self):
        """Returns a new identical array"""
        matrixAsList = []
        for row in self.matrix:
            for entry in row:
                matrixAsList.append(entry)
                
        return Array(self.rowNumber, self.columnNumber, matrixAsList)
    
    
    def INFnorm(self):
        """Returns the largest absolute row sum of the array"""
        absRowSums = []
        for row in range(self.rowNumber):
            absRowSum = 0
            for column in range(self.columnNumber):
                absRowSum += abs(self.matrix[row][column])
            absRowSums.append(absRowSum)
            
        return max(absRowSums)
    
    
    def ONEnorm(self):
        """Returns the largest aboslute column sum of the array"""
        absColumnSums = [0] * self.columnNumber
        for row in range(self.rowNumber):
            for column in range(self.columnNumber):
                absColumnSums[column] += abs(self.matrix[row][column])
                
        return max(absColumnSums)
    
    
    def transposeOf(self):
        """Returns the transpose of the array"""
        transposedArray = Array(self.columnNumber, self.rowNumber)
        for row in range(self.rowNumber):
            for column in range(self.columnNumber):
                transposedArray.changeEntry(column, row, self.matrix[row][column])
                
        return transposedArray
    
    
    def __rsub__(self, other):
        return (self - other) * -1

        
    def __add__(self, other):
        return self - (other * -1)

    
    __radd__ = __add__
    
    
    __rmul__ = __mul__
    
    
    
def solve(A, b):
    """Returns the solution 'x' to the system of linear equations 'A*x = b' 
    using the Jacobi iterative method"""
    guessLength = A.columnNumber
    initialGuess = Array(guessLength, 1, [1] * guessLength)
    
    A, b = scramble(A, b)
    
    copy = initialGuess.deepCopy()
    tolerance = 1 * 10 ** -15
    error = 1
    counter = 0
    while error > tolerance and counter < 100:
        for row in range(guessLength):
            currentVar = b.matrix[row][0]
            for column in range(A.columnNumber):
                if column != row:
                    currentVar -= A.matrix[row][column] * initialGuess.matrix[column][0]
            
            currentVar /= A.matrix[row][row]
            initialGuess.changeEntry(row, 0, currentVar)
        
        counter += 1
        error = (initialGuess - copy).INFnorm() / initialGuess.INFnorm()
        copy = initialGuess.deepCopy()
    
    return initialGuess


def scramble(A, b):
    """Rearranges the rows of matrix/array A such there are no diagonal
    entries with value zero"""
    diagonals = []
    for row in range(A.rowNumber):
        diagonals.append(A.matrix[row][row])
    if 0 not in diagonals:
        return A, b
    
    if len(set([str(row) for row in A.matrix])) < A.rowNumber or [0] * A.columnNumber in A.matrix:
        raise ValueError('Given matrix A is defective')

    rowOptions = []
    for row in range(A.rowNumber):
        rowOptions.append([])
    for row in range(A.rowNumber):
        for column in range(A.columnNumber):
            if A.matrix[row][column] != 0:
                rowOptions[column].append(row)
    
    master = []
    optionTree = []
    while len(master) < A.rowNumber:
        nextOptions = rowOptions[len(master)][:]
        for number in master:
            if number in nextOptions:
                nextOptions.remove(number)
        if len(nextOptions) == 0:
            master.pop()
            continue
        else:
            optionTree.append(nextOptions)
            
        if len(optionTree) == 0:
            raise ValueError('Given matrix A is defective')
        
        master.append(optionTree[len(master)].pop())
            
    resultA = Array(A.rowNumber, A.rowNumber)
    for index in range(len(master)):
        resultA.matrix[index] = A.matrix[master[index]]
        
    resultb = Array(A.rowNumber, 1)
    for index in range(len(master)):
        resultb.matrix[index] = b.matrix[master[index]]
        
    return resultA, resultb
    

def lsSolve(A, b):
    return solve(A.transposeOf() * A, A.transposeOf() * b)


def main():
    A = Array(2,2,[0,1,1,0])
    b = Array(2,1,[1,-3.012465])
    print(solve(A, b))


if __name__ == '__main__':
    main()
    
