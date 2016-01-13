# mantid-non-aligned-axes-symops

## To think about

1. Switch to using `SymmetryOperationFactory` for generating symmetry operation vectors instead of manually storing matrices and carring out matrix multiplication. See [here](http://docs.mantidproject.org/nightly/concepts/SymmetryGroups.html)
2. Instead of having the user to enter the space group, create a list of all symmetry operations (there are only a few dozen or so), and allow the user to select them through a GUI.
3. Normalization.


## Work in-progress

1. Handling exceptions. Would eventually need to make appropriate changes to `MantidKernal/Exception.h`.
2. Make the code more user-friendly by allowing users to select which symmetry operations they want to use through a GUI. [`VisibleWhenProperty`](http://docs.mantidproject.org/nightly/api/python/mantid/kernel/VisibleWhenProperty.html) will be useful.
3. Write test cases.

## Running the code

Load the script in Mantid, and execute it. After execution, you should see the `SpaceGroupSymOps` in the algorithm selector box under the section `PythonAlgorithms`. After you've loaded all data files and have a `MDWorkspace`, run the algorithm by double-clicking on the name.

Alternately, you can use the command-line. See [this](http://www.mantidproject.org/Running_Algorithms_With_Python) for more information.
