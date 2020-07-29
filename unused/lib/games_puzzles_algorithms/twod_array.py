

class TwoDArray(object):
    """
    A class representing a 2D array.
    The first index is the row number, and the second is the column number.
    """
    
    def __init__(self, dimensions, oned_list=None):
        """
        Initialize the 2D array.
        dimensions should be a tuple with the number of rows and then columns.
        oned_list is a list to initialize the the values of the 2D array with.
        Items are copied from oned_list to the first row going from left to
        right, repeating for subsequent rows. If oned_list is None all array
        elements are initialized to 0.
        """
        self.num_rows = dimensions[0]
        self.num_cols = dimensions[1]
        if self.num_rows < 1 or self.num_cols < 1:
            raise ValueError('Error: invalid dimensions')
        if (oned_list is not None
            and len(oned_list) != self.num_rows * self.num_cols):
            raise ValueError('Error: incompatible dimensions and list')
        self.matrix = []
        i = 0
        for row_num in range(self.num_rows):
            row = []
            for col_num in range(self.num_cols):
                if oned_list is not None:
                    row.append(oned_list[i])
                    i += 1
                else:
                    row.append(0)
            self.matrix.append(row)
            
    def __setitem__(self, indeces, value):
        self.matrix[indeces[0]][indeces[1]] = value
        
    def __getitem__(self, indeces):
        return self.matrix[indeces[0]][indeces[1]]
    
    def size(self):
        return (self.num_rows, self.num_cols)
    
    def __eq__(self, other):
        if self.num_rows != other.num_rows:
            return False
        if self.num_cols != other.num_cols:
            return False
        for row in range(self.num_rows):
            if self.matrix[row] != other.matrix[row]:
                return False
        
        return True
    
    def flatten(self):
        """Return a flattened 1D representation of the array as a list."""
        result = []
        for row in self.matrix:
            result.extend(row)
            
        return result