# mantid-non-aligned-axes-symops

## To think about

1. Do we continue to use C++ STL for storing matrices and vectors, or incorporate Mantid's own `V3D` and `Matrix` classes, or use external libraries like `Boost` or `Eigen`?
2. Normalization.


## Work in-progress

1. Handling exceptions. Would eventually need to make appropriate changes to `MantidKernal/Exception.h`.
2. Make the code more user-friendly by allowing users to select which symmetry operations they want to use through a GUI.
3. Write test cases.

## Running the code

Load the script in Mantid, and execute it. After execution, you should see the `SpaceGroupSymOps` in the algorithm selector box under the section `PythonAlgorithms`. After you've loaded all data files and have a `MDWorkspace`, run the algorithm by double-clicking on the name.

Alternately, you can use the command-line. See [this](http://www.mantidproject.org/Running_Algorithms_With_Python) for more information.
