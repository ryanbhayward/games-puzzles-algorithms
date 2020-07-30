from games_puzzles_algorithms.twod_array import TwoDArray
import unittest

class TestTwoDArray(unittest.TestCase):
    
    def setUp(self):
        self.size1 = 2
        self.size2 = 3
    
    def test_init(self):
        array = TwoDArray((self.size1, self.size2))
        self.assertEqual(array.num_rows, self.size1)
        self.assertEqual(array.num_cols, self.size2)
        for i in range(self.size1):
            for j in range(self.size2):
                self.assertEqual(array.matrix[i][j], 0)
                
    def test_init_list(self):
        init_list = range(self.size1 * self.size2)
        array = TwoDArray((self.size1, self.size2), init_list)
        self.assertEqual(array.num_rows, self.size1)
        self.assertEqual(array.num_cols, self.size2)
        for i in range(self.size1):
            for j in range(self.size2):
                self.assertEqual(array.matrix[i][j], i * self.size2 + j)
                
    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            array = TwoDArray((0, 0))
            
    def test_invalid_list(self):
        init_list = []
        with self.assertRaises(ValueError):
            array = TwoDArray((self.size1, self.size2), init_list)
                
    def test_get_item(self):
        init_list = range(self.size1 * self.size2)
        array = TwoDArray((self.size1, self.size2), init_list)
        for i in range(self.size1):
            for j in range(self.size2):
                self.assertEqual(array[(i, j)], i * self.size2 + j)
                
    def test_set_item(self):
        array = TwoDArray((self.size1, self.size2))
        for i in range(self.size1):
            for j in range(self.size2):
                self.assertEqual(array[(i, j)], 0)
                array[(i, j)] = i * self.size2 + j
                self.assertEqual(array[(i, j)], i * self.size2 + j)
                
    def test_size(self):
        array = TwoDArray((self.size1, self.size2))
        self.assertEqual(array.size(), (self.size1, self.size2))
        
    def test_eq_true(self):
        a = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        b = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        self.assertTrue(a == b)
        
    def test_eq_dif_rows(self):
        a = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        b = TwoDArray((10, self.size2), range(10 * self.size2))
        self.assertFalse(a == b)
        
    def test_eq_dif_cols(self):
        a = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        b = TwoDArray((self.size1, 10), range(self.size1 * 10))
        self.assertFalse(a == b)
        
    def test_eq_dif_values(self):
        a = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        b = TwoDArray((self.size1, self.size2), range(self.size1 * self.size2))
        b[(0, 0)] = 100
        self.assertFalse(a == b)
        
    def test_flatten(self):
        init_list = range(self.size1 * self.size2)
        array = TwoDArray((self.size1, self.size2), init_list)
        oned = array.flatten()
        for i in init_list:
            self.assertEqual(oned[i], i)

  
if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit:
        pass
