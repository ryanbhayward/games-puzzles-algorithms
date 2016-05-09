#!/usr/bin/env python3

import pycuber as pc
from pycuber.solver import CFOPSolver

if __name__ == "__main__":
    # Create a Cube object
    mycube = pc.Cube()

    # Randomizing
    rand_alg = pc.Formula().random()
    mycube(rand_alg)

    print(mycube)

    solver = CFOPSolver(mycube)
    solution = solver.solve()

    print(mycube)
