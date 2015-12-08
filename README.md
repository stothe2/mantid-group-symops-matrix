# mantid-non-aligned-axes-symops

## To think about

1. Do we continue to use C++ STL for storing matrices and vectors, or incorporate Mantid's own `V3D` and `Matrix` classes, or use external libraries like `Boost` or `Eigen`? I guess to answer this we need to determine whether the required Mantid classes are optimized, or/and is it really worth it to use external libraries just for matrix multiplication.
2. Are `multimaps` the most efficient way of storing space group information? Mantid's source code uses macros, but working with a list of matrices in macros over-complicates things unnecessarily.
3. Is the user-defined basis vector always going to of type `int`, or possibility of `float`?
4. Normalization.


## Work in-progress

1. Handling exceptions. Would eventually need to make appropriate changes to `MantidKernal/Exception.h`.
2. Create Python interface.
3. Make the code more user-friendly by allowing highest possible abstraction for the user: implementation should automatically handle all parts of data processing--symmetrization, binning and adding workspaces, normalization.
4. Define constants.

## Running the code

Make sure your compiler supports `C++11` or `C++0x`. Run the code using the makefile.
```
$ make all
$ make clean
```
