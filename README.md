# mantid-non-aligned-axes-symops

## To think about

1. Do we continue to use C++ STL for storing matrices and vectors, or incorporate Mantid's own `V3D` and `Matrix` classes, or use external libraries like `Boost` or `Eigen`? I guess to answer this we need to determine whether the required Mantid classes are optimized, or/and is it really worth it to use external libraries just for matrix multiplication.

## Running the code

Make sure your compiler supports `C++11` or `C++0x`. Run the code using the makefile.
```
$ make all
$ make clean
```
