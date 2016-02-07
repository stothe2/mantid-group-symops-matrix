from mantid.kernel import *
from mantid.api import *
from mantid.geometry import SymmetryOperationFactory

from collections import defaultdict
from numpy import array
from numpy import dot
from math import modf # to split number into int and decimal parts

# Space group matrices without translation column
sg = [	(1, array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])), # Triclinic
		(2, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(3, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])), # Monoclinic
		(4, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(5, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(6, array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(7, array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(8, array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(9, array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(10, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(10, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(11, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(11, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(12, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(12, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(13, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(13, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(14, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(14, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(15, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(15, array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(16, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])), # Orthorhombic
		(16, array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])),
		(17, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(17, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(18, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(18, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(19, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(19, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(20, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(20, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(21, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(21, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(22, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(22, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(23, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(23, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(198, array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])),
		(198, array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])),
		(198, array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]))]
dict_sg = defaultdict(list)
for k, v in sg:
	dict_sg[k].append(v)

# Translation vectors
t = [	(1, array([0,0,0,0])), # Triclinic
		(2, array([0,0,0,0])),
		(3, array([0,0,0,0])), # Monoclinic
		(4, array([0,0.5,0,0])),
		(5, array([0,0,0,0])),
		(6, array([0,0,0,0])),
		(7, array([0,0,0.5,0])),
		(8, array([0,0,0,0])),
		(9, array([0,0,0.5,0])),
		(10, array([0,0,0,0])),
		(10, array([0,0,0,0])),
		(11, array([0,0.5,0,0])),
		(11, array([0,0,0,0])),
		(12, array([0,0,0,0])),
		(12, array([0,0,0,0])),
		(13, array([0,0,0.5,0])),
		(13, array([0,0,0,0])),
		(14, array([0,0.5,0.5,0])),
		(14, array([0,0,0,0])),
		(15, array([0,0,0.5,0])),
		(15, array([0,0,0,0])),
		(16, array([0,0,0,0])), # Orthorhombic
		(16, array([0,0,0,0])),
		(17, array([0,0,0.5,0])),
		(17, array([0,0,0.5,0])),
		(18, array([0,0,0,0])),
		(18, array([0.5,0.5,0,0])),
		(19, array([0.5,0,0.5,0])),
		(19, array([0,0.5,0.5,0])),
		(20, array([0,0,0.5,0])),
		(20, array([0,0,0.5,0])),
		(21, array([0,0,0,0])),
		(21, array([0,0,0,0])),
		(22, array([0,0,0,0])),
		(22, array([0,0,0,0])),
		(23, array([0,0,0,0])),
		(23, array([0,0,0,0])),
		(198, array([0.5,0,0.5,0])),
		(198, array([0,0.5,0.5,0])),
		(198, array([0,0,0,0]))]
dict_t = defaultdict(list)
for k, v in t:
	dict_t[k].append(v)

# Symmetry operation list
symList = ['x,y,z',
	'-x,-y,-z',
	'-x,y,-z',
	'-x,y+1/2,-z',
	'x+1/2,y+1/2,z',
	'x,-y,z',
	'x,-y,z+1/2',
	'-x,y,-z+1/2',
	'-x,y+1/2,-z+1/2',
	'-x,-y,z',
	'-x,-y,z+1/2',
	'-x+1/2,y+1/2,-z',
	'-x+1/2,-y,z+1/2',
	'x,y+1/2,z+1/2',
	'x+1/2,y,z+1/2',
	'x+1/2,y+1/2,z+1/2',
	'x+1/2,-y,z',
	'x,-y+1/2,z+1/2',
	'x+1/2,-y,z+1/2',
	'x+1/2,-y+1/2,z',
	'x+1/2,-y+1/2,z+1/2',
	'x,-y+1/2,z',
	'x+1/4,-y+1/4,z+1/4',
	'-x+1/2,-y+1/2,z',
	'-x+1/2,y,-z+1/2',
	'-x+1/2,y,-z',
	'-x+1/2,-y,z',
	'-x+1/2,y+1/2,-z+1/2',
	'-x+1/2,-y+1/2,z+1/2',
	'-x,-y+1/2,z+1/2',
	'-x,-y+1/2,z',
	'-x+3/4,-y+3/4,z',
	'-x+3/4,y,-z+3/4',
	'-y,x,z',
	'-y,x,z+1/4',
	'-y,x,z+1/2',
	'-y,x,z+3/4',
	'-y,x+1/2,z+1/4',
	'y,-x,-z',
	'-y+1/2,x,z',
	'-y,x+1/2,z+1/2',
	'-y+3/4,x+1/4,z+1/4',
	'-y+1/2,x+1/2,z',
	'-y+1/2,x+1/2,z+1/4',
	'-x+1/2,y+1/2,-z+1/4',
	'-y+1/2,x+1/2,z+1/2',
	'-y+1/2,x+1/2,z+3/4',
	'-x+1/2,y+1/2,-z+3/4',
	'-x+1/2,y,-z+3/4',
	'-y+1/2,x,z+1/2',
	'-y+1/4,x+3/4,z+1/4',
	'-y,x-y,z',
	'-y,x-y,z+1/3',
	'-y,x-y,z+2/3',
	'x+2/3,y+1/3,z+1/3',
	'-y,-x,-z',
	'y,x,-z',
	'-y,-x,-z+2/3',
	'-y,-x,-z+1/3',
	'-y,-x,z',
	'y,x,z',
	'-y,-x,z+1/2',
	'y,x,z+1/2',
	'-y,-x,-z+1/2',
	'y,x,-z+1/2',
	'x,y,-z',
	'y,x,-z+1/3',
	'y,x,-z+2/3',
	'x,y,-z+1/2',
	'z,x,y',
	'y+1/2,x+1/2,-z+1/2',
	'y+3/4,x+1/4,-z+3/4',
	'y+1/4,x+3/4,-z+3/4',
	'y+3/4,x+1/4,-z+1/4',
	'y+1/2,x+1/2,z+1/2',
	'y+1/4,x+1/4,z+1/4',
	'y+1/2,x+1/2,-z',
	'-x+3/4,-y+1/4,z+1/2',
	'-x+1/4,y+1/2,-z+3/4',
	'y+3/4,x+1/4,-z+1/2',
	'-x+1/4,-y+3/4,z+1/2',
	'-x+3/4,y+1/2,-z+1/4',
	'y+3/4,x+1/4,-z',
]

class SpaceGroupSymOps(PythonAlgorithm):

	def PyInit(self):
		# ------------------------- Input properties -------------------------

		# Space group and symmetry properties
		self.declareProperty('Symmetrization by', 'Space Group', validator=StringListValidator(['Space Group', 'Symmetry Operations']))
		self.declareProperty('Space Group', 198, IntBoundedValidator(lower=1, upper=230),
			doc='Space group number as given in International Tables for Crystallography, Vol. A')
		self.declareProperty('Number of symmetry operations', '1', validator=StringListValidator(['1', '2', '3', '4', '5']))
		self.declareProperty('Symmetry operation 1', 'x,y,z', validator=StringListValidator(symList))
		self.declareProperty('Symmetry operation 2', 'x,y,z', validator=StringListValidator(symList))
		self.declareProperty('Symmetry operation 3', 'x,y,z', validator=StringListValidator(symList))
		self.declareProperty('Symmetry operation 4', 'x,y,z', validator=StringListValidator(symList))
		self.declareProperty('Symmetry operation 5', 'x,y,z', validator=StringListValidator(symList))

		self.setPropertySettings('Space Group', VisibleWhenProperty('Symmetrization by', PropertyCriterion.IsEqualTo, 'Space Group'))
		self.setPropertySettings('Number of symmetry operations', VisibleWhenProperty('Symmetrization by', PropertyCriterion.IsEqualTo, 'Symmetry Operations'))
		self.setPropertySettings('Symmetry operation 1', VisibleWhenProperty('Symmetrization by', PropertyCriterion.IsEqualTo, 'Symmetry Operations'))
		self.setPropertySettings('Symmetry operation 2', VisibleWhenProperty('Number of symmetry operations', PropertyCriterion.IsMoreOrEqual, '2'))
		self.setPropertySettings('Symmetry operation 3', VisibleWhenProperty('Number of symmetry operations', PropertyCriterion.IsMoreOrEqual, '3'))
		self.setPropertySettings('Symmetry operation 4', VisibleWhenProperty('Number of symmetry operations', PropertyCriterion.IsMoreOrEqual, '4'))
		self.setPropertySettings('Symmetry operation 5', VisibleWhenProperty('Number of symmetry operations', PropertyCriterion.IsMoreOrEqual, '5'))

		sym_grp = 'Symmetrization options'
		self.setPropertyGroup('Symmetrization by', sym_grp)
		self.setPropertyGroup('Space Group', sym_grp)
		self.setPropertyGroup('Number of symmetry operations', sym_grp)
		self.setPropertyGroup('Symmetry operation 1', sym_grp)
		self.setPropertyGroup('Symmetry operation 2', sym_grp)
		self.setPropertyGroup('Symmetry operation 3', sym_grp)
		self.setPropertyGroup('Symmetry operation 4', sym_grp)
		self.setPropertyGroup('Symmetry operation 5', sym_grp)

		# Binning properties
		self.declareProperty('BasisVector0', 'a,unit,1,1,0,0', StringMandatoryValidator(), 'Format: \'name,units,x,y,z\'')
		self.declareProperty('BasisVector1', 'b,unit,0,0,1,0', StringMandatoryValidator(), 'Format: \'name,units,x,y,z\'')
		self.declareProperty('Axis Aligned', False, 'Perform binning aligned with the axes of the input MDEventWorkspace?')
		self.declareProperty('Normalized Basis Vectors', True, 'Normalize the given basis vectors to unity')
		self.declareProperty(FloatArrayProperty(name='Output Extents',
												values=[-5,8,-5,8],
												validator=FloatArrayLengthValidator(4)),
			'The minimum, maximum edges of space of each dimension of the OUTPUT workspace, as a comma-separated list')
		self.declareProperty(FloatArrayProperty(name='Output Bins',
												values=[50,50],
												validator=FloatArrayLengthValidator(2)),
			'The number of bins for each dimension of the OUTPUT workspace')
		self.declareProperty(FloatArrayProperty(name='Translation',
												values=[0,0,0,0],
												validator=FloatArrayLengthValidator(4)),
			'Coordinates in the INPUT workspace that corresponds to (0,0,0) in the OUTPUT workspace')
		self.declareProperty(WorkspaceProperty(name='Input Workspace',
												defaultValue='',
												direction=Direction.Input), 'An input MDWorkspace')

		bin_grp = 'Binning parameters'
		self.setPropertyGroup('BasisVector0', bin_grp)
		self.setPropertyGroup('BasisVector1', bin_grp)
		self.setPropertyGroup('Axis Aligned', bin_grp)
		self.setPropertyGroup('Normalized Basis Vectors', bin_grp)
		self.setPropertyGroup('Output Extents', bin_grp)
		self.setPropertyGroup('Output Bins', bin_grp)
		self.setPropertyGroup('Translation', bin_grp)

		# ------------------------- Output properties ------------------------
		self.declareProperty(WorkspaceProperty(name='Binned Workspace',
												defaultValue='',
												direction=Direction.Output), 'A name for the output MDHistoWorkspace')

	def PyExec(self):
		sgNumber = self.getProperty('Space Group').value
		mdws = self.getProperty('Input Workspace').value
		basis0 = self.getProperty('BasisVector0').value
		basis1 = self.getProperty('BasisVector1').value
		axisAligned = self.getProperty('Axis Aligned').value
		normalizeBasisVectors = self.getProperty('Normalized Basis Vectors').value
		outputExtents = self.getProperty('Output Extents').value
		outputBins = self.getProperty('Output Bins').value
		translation = self.getProperty('Translation').value
		symChoice = self.getProperty('Symmetrization by').value
		numOp = self.getProperty('Number of symmetry operations').value
		symOp1 = self.getProperty('Symmetry operation 1').value
		symOp2 = self.getProperty('Symmetry operation 2').value
		symOp3 = self.getProperty('Symmetry operation 3').value
		symOp4 = self.getProperty('Symmetry operation 4').value
		symOp5 = self.getProperty('Symmetry operation 5').value

		binned_ws = BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
					BasisVector0=basis0, BasisVector1=basis1,
					NormalizeBasisVectors=normalizeBasisVectors, Translation=translation,
					OutputExtents=outputExtents, OutputBins=outputBins)

		if symChoice == "Symmetry Operations":
			binned_ws = self._symmetrize_by_generators(mdws, axisAligned, basis0, basis1,
				normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
				int(numOp), symOp1, symOp2, symOp3, symOp4, symOp5)
		else:
			binned_ws = self._symmetrize_by_sg(mdws, axisAligned, basis0, basis1,
				normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
				sgNumber)

		self.setProperty("Binned Workspace", binned_ws)


	def category(self):
		return 'PythonAlgorithms'


	def _symmetrize_by_sg(self, mdws, axisAligned, basis0, basis1,
		normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
		sgNumber):

		unit0, basisVec0 = self._destringify(basis0)
		unit1, basisVec1 = self._destringify(basis1)

		for index, item in enumerate(dict_sg[sgNumber]):
			newBasisVec0 = dot(item, basisVec0)
			newBasisVec1 = dot(item, basisVec1)

			basisVec0_str = unit0[0] + ',' + unit0[1] + ',' + str(newBasisVec0[0]) \
							+ ',' + str(newBasisVec0[1]) + ',' + str(newBasisVec0[2]) + ',' + '0'
			basisVec1_str = unit1[0] + ',' + unit1[1] + ',' + str(newBasisVec1[0]) \
							+ ',' + str(newBasisVec1[1]) + ',' + str(newBasisVec1[2]) + ',' + '0'
			newTranslation = translation + dict_t[sgNumber][index]

			binned_ws += BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
						BasisVector0=basisVec0_str, BasisVector1=basisVec1_str,
						NormalizeBasisVectors=normalizeBasisVectors, Translation=newTranslation,
						OutputExtents=outputExtents, OutputBins=outputBins)
		return binned_ws


	def _symmetrize_by_generators(self, mdws, axisAligned, basis0, basis1,
		normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
		numOp, symOp1, symOp2, symOp3, symOp4, symOp5):
		
		unit0, basisVec0 = self._destringify(basis0)
		unit1, basisVec1 = self._destringify(basis1)

		symOpList = [symOp1, symOp2, symOp3, symOp4, symOp5]
		for i in range(numOp):
			symOp = SymmetryOperationFactory.createSymOp(symOpList[i])
			
			# x-value
			coordinates, newTranslation = self._get_coordinates_with_translation([0, 1, 0], symOp)
			newTranslation += translation # Factor in for the original translation reading
			x0_value = dot(coordinates, basisVec0)
			x1_value = dot(coordinates, basisVec1)

			# y-value
			coordinates = self._get_coordinates([0, 1, 0], symOp)
			y0_value = dot(coordinates, basisVec0)
			y1_value = dot(coordinates, basisVec1)

			# z-value
			coordinates = self._get_coordinates([0, 0, 1], symOp)
			z0_value = dot(coordinates, basisVec0)
			z1_value = dot(coordinates, basisVec1)

			# Combine values x,y,z values obtained above for new basis vectors
			basisVec0_str = unit0[0] + ',' + unit0[1] + ',' + str(x0_value) \
							+ ',' + str(y0_value) + ',' + str(z0_value) + ',' + '0'
			basisVec1_str = unit1[0] + ',' + unit1[1] + ',' + str(x1_value) \
							+ ',' + str(y1_value) + ',' + str(z1_value) + ',' + '0'

			binned_ws += BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
						BasisVector0=basisVec0_str, BasisVector1=basisVec1_str,
						NormalizeBasisVectors=normalizeBasisVectors, Translation=newTranslation,
						OutputExtents=outputExtents, OutputBins=outputBins)
		return binned_ws


	def _destringify(self, basis):
		temp = basis.split(',')
		unit = temp[0:2]
		temp = temp[2:-1]
		return unit, array([int(temp[0]), int(temp[1]), int(temp[2])])


	def _get_coordinates(self, coordinates, symOp):
		''' Split coordinates into int (basis) and decimal (translation) parts,
		but return only int part 
		'''
		coordinatesPrime = symOp.transformCoordinates(coordinates)
		newCoordinatesPrime = []
			
		splitNum = modf(coordinatesPrime.getX()) # 1st number
		newCoordinatesPrime.append(splitNum[1])
			
		splitNum = modf(coordinatesPrime.getY()) # 2nd number
		newCoordinatesPrime.append(splitNum[1])
			
		splitNum = modf(coordinatesPrime.getZ()) # 3rd number
		newCoordinatesPrime.append(splitNum[1])

		return newCoordinatesPrime

	def _get_coordinates_with_translation(self, coordinates, symOp):
		''' Split coordinates into int (basis) and decimal (translation) parts,
		and return both int and translation parts 
		'''
		coordinatesPrime = symOp.transformCoordinates(coordinates)
		newCoordinatesPrime = []
		newTranslation = []
		
		splitNum = modf(coordinatesPrime.getX()) # 1st number
		newCoordinatesPrime.append(splitNum[1])
		newTranslation.append(splitNum[0])
		
		splitNum = modf(coordinatesPrime.getY()) # 2nd number
		newCoordinatesPrime.append(splitNum[1])
		newTranslation.append(splitNum[0])
		
		splitNum = modf(coordinatesPrime.getZ()) # 3rd number
		newCoordinatesPrime.append(splitNum[1])
		newTranslation.append(splitNum[0])

		newTranslation.append(0) # Add energy dimension to the translation vector
		
		return newCoordinatesPrime, newTranslation


# Register algorithm with Mantid
AlgorithmFactory.subscribe(SpaceGroupSymOps)