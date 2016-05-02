from ._hyper_cube_indexer import ffi, lib
from array import array

class HyperCubeIndexer():
    ''' Arranged in the same order as +dimensions+. So it is contiguous in the
        first dimension.
    '''
    def __init__(self, dimensions):
        self.dimensions = ffi.new("unsigned int[]", dimensions)
        self.indices = ffi.new("unsigned int[]", len(dimensions))

    def slice(self, indices):
        ignored_dimensions_products = ffi.new("unsigned int*")
        num_indices = len(indices)
        num_dimensions = len(self.dimensions)

        for i in range(num_indices):
            self.indices[i] = indices[i]

        base_offset = lib.compute_base_offset_for_slice(
            self.dimensions,
            num_dimensions,
            self.indices,
            num_indices,
            ignored_dimensions_products
        )
        return slice(
            base_offset, base_offset + ignored_dimensions_products[0]
        )

    def __call__(self, indices):
        num_indices = len(indices)
        num_dimensions = len(self.dimensions)

        if num_indices < num_dimensions:
            return self.slice(indices)
        else:
            for i in range(num_indices):
                self.indices[i] = indices[i]

            return lib.compute_base_offset(
                self.dimensions,
                num_dimensions,
                self.indices,
                num_indices
            )

    def __len__(self):
        return lib.length(self.dimensions, len(self.dimensions))

    def num_dimensions(self):
        return len(self.dimensions)

    def raw(self):
        return array('I', bytes(ffi.buffer(self.dimensions)))
