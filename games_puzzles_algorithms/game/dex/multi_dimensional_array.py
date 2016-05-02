from __future__ import unicode_literals
from future.utils import bytes_to_native_str
from array import array
from .hyper_cube_indexer import HyperCubeIndexer


class MultiDimensionalArray():
    ''' Arranged in the same order as +dimensions+. So it is contiguous in the
        first dimension.
    '''
    def __init__(self, dimensions, initial_elem=0, elem_type='B'):
        self.indexer = HyperCubeIndexer(dimensions)
        self.data = array(elem_type, [initial_elem]*len(self.indexer))

    def __setitem__(self, indices, value):
        self.data[self.indexer(indices)] = value

    def __getitem__(self, indices):
        return self.data[self.indexer(indices)]

    def raw(self):
        return (self.data, self.indexer.raw())
