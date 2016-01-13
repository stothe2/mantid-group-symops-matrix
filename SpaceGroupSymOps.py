from mantid.kernel import *
from mantid.api import *

from collections import defaultdict
from numpy import array
from numpy import dot

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


class SpaceGroupSymOps(PythonAlgorithm):

	def PyInit(self):
		# Input properties
		self.declareProperty('SpaceGroup', 198, IntBoundedValidator(lower=1, upper=230))
		self.declareProperty('AxisAligned', False)
		self.declareProperty('NormalizedBasisVectors', True)
		self.declareProperty('BasisVector0', 'a,unit,1,1,0,0', StringMandatoryValidator())
		self.declareProperty('BasisVector1', 'b,unit,0,0,1,0', StringMandatoryValidator())
		self.declareProperty(FloatArrayProperty(name='OutputExtents',
												values=[-5,8,-5,8],
												validator=FloatArrayLengthValidator(4)))
		self.declareProperty(FloatArrayProperty(name='OutputBins',
												values=[50,50],
												validator=FloatArrayLengthValidator(2)))
		self.declareProperty(FloatArrayProperty(name='Translation',
												values=[0,0,0,0],
												validator=FloatArrayLengthValidator(4)))
		self.declareProperty(WorkspaceProperty(name='InputWorkspace',
												defaultValue='',
												direction=Direction.Input))

		# Output properties
		self.declareProperty(WorkspaceProperty(name='BinnedWorkspace',
												defaultValue='',
												direction=Direction.Output))

	def PyExec(self):
		sgNumber = self.getProperty("SpaceGroup").value
		mdws = self.getProperty("InputWorkspace").value
		basis0 = self.getProperty("BasisVector0").value
		basis1 = self.getProperty("BasisVector1").value
		axisAligned = self.getProperty("AxisAligned").value
		normalizeBasisVectors = self.getProperty("NormalizedBasisVectors").value
		outputExtents = self.getProperty("OutputExtents").value
		outputBins = self.getProperty("OutputBins").value
		translation = self.getProperty("Translation").value

		binned_ws = BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
					BasisVector0=basis0, BasisVector1=basis1,
					NormalizeBasisVectors=normalizeBasisVectors, Translation=translation,
					OutputExtents=outputExtents, OutputBins=outputBins)

		unit0, basisVec0 = self.__destringify(basis0)
		unit1, basisVec1 = self.__destringify(basis1)


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

		self.setProperty("BinnedWorkspace", binned_ws)


	def category(self):
		return 'PythonAlgorithms'

	def __destringify(self, basis):
		temp = basis.split(',')
		unit = temp[0:2]
		temp = temp[2:-1]
		return unit, array([int(temp[0]), int(temp[1]), int(temp[2])])


# Register algorithm with Mantid
AlgorithmFactory.subscribe(SpaceGroupSymOps)