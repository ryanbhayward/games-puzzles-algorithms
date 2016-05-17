#!/usr/bin/env python

from cffi import FFI
ffi = FFI()

ffi.cdef(
    '''
    unsigned int compute_base_offset(
        const unsigned int * dimensions,
        unsigned int num_dimensions,
        const unsigned int * indices,
        unsigned int num_indices
    );
    unsigned int length(
        const unsigned int * dimensions,
        unsigned int num_dimensions
    );
    unsigned int compute_base_offset_for_slice(
        const unsigned int * dimensions,
        unsigned int num_dimensions,
        const unsigned int * indices,
        unsigned int num_indices,
        unsigned int* ignored_dimensions_products
    );
    '''
)

ffi.set_source("games_puzzles_algorithms._hyper_cube_indexer",
    '''
    static unsigned int _compute_base_offset(
        const unsigned int * dimensions,
        unsigned int num_dimensions,
        const unsigned int * indices,
        unsigned int num_indices,
        unsigned int num_ignored_dimensions,
        unsigned int products
    ) {
        unsigned int base_offset = indices[0] * products;
        unsigned int i = 0;
        for (; i < num_dimensions - num_ignored_dimensions - 1; ++i) {
            products *= dimensions[num_ignored_dimensions + i];
            base_offset += (indices[i + 1] * products);
        }
        return base_offset;
    }
    unsigned int compute_base_offset_for_slice(
        const unsigned int * dimensions,
        unsigned int num_dimensions,
        const unsigned int * indices,
        unsigned int num_indices,
        unsigned int* ignored_dimensions_products
    ) {
        unsigned int num_ignored_dimensions = num_dimensions - num_indices;
        unsigned int products = 1;
        unsigned int i = 0;
        for (; i < num_ignored_dimensions; ++i) {
            products *= dimensions[i];
        }
        ignored_dimensions_products[0] = products;
        return _compute_base_offset(
            dimensions,
            num_dimensions,
            indices,
            num_indices,
            num_ignored_dimensions,
            products
        );
    }
    unsigned int compute_base_offset(
        const unsigned int * dimensions,
        unsigned int num_dimensions,
        const unsigned int * indices,
        unsigned int num_indices
    ) {
        unsigned int num_ignored_dimensions = num_dimensions - num_indices;
        unsigned int products = 1;
        unsigned int i = 0;
        for (; i < num_ignored_dimensions; ++i) {
            products *= dimensions[i];
        }
        return _compute_base_offset(
            dimensions,
            num_dimensions,
            indices,
            num_indices,
            num_ignored_dimensions,
            products
        );
    }
    unsigned int length(
        const unsigned int * dimensions,
        unsigned int num_dimensions
    ) {
        unsigned int _len = 1;
        unsigned int i = 0;
        for (; i < num_dimensions; ++i) {
            _len *= dimensions[i];
        }
        return _len;
    }
    '''
)


if __name__ == "__main__":
    ffi.compile()
