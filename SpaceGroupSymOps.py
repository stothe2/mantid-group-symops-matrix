from mantid.kernel import *
from mantid.api import *
from mantid.geometry import SymmetryOperationFactory

from collections import defaultdict
from numpy import array
from numpy import dot
import re

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
		(143, array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])),
		(143, array([[0, -1, 0], [1, -1, 0], [0, 0, 1]])),
		(198, array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])),
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
		(143, array([0,0,0,0])),
		(143, array([0,0,0,0])),
		(198, array([0,0,0,0])),
		(198, array([0.5,0,0.5,0])),
		(198, array([0,0.5,0.5,0])),
		(198, array([0,0,0,0]))]
dict_t = defaultdict(list)
for k, v in t:
	dict_t[k].append(v)

# Symmetry operation list
symList = ['x,y,z',
	'x,y,-z',
	'x,-y,z',
	'x,-y,-z',
	'-x,y,z',
	'-x,y,-z',
	'-x,-y,z',
	'-x,-y,-z',
	'x,z,y',
	'x,z,-y',
	'x,-z,y',
	'x,-z,-y',
	'-x,z,y',
	'-x,z,-y',
	'-x,-z,y',
	'-x,-z,-y',
	'y,x,z',
	'y,x,-z',
	'y,-x,z',
	'y,-x,-z',
	'-y,x,z',
	'-y,x,-z',
	'-y,-x,z',
	'-y,-x,-z',
	'y,z,x',
	'y,z,-x',
	'y,-z,x',
	'y,-z,-x',
	'-y,z,x',
	'-y,z,-x',
	'-y,-z,x',
	'-y,-z,-x',
	'z,x,y',
	'z,x,-y',
	'z,-x,y',
	'z,-x,-y',
	'-z,x,y',
	'-z,x,-y',
	'-z,-x,y',
	'-z,-x,-y',
	'z,y,x',
	'z,y,-x',
	'z,-y,x',
	'z,-y,-x',
	'-z,y,x',
	'-z,y,-x',
	'-z,-y,x',
	'-z,-y,-x',
	'x,x-y,z',
	'x,x-y,-z',
	'-x,-x+y,z',
	'-x,-x+y,-z',
	'y,-x+y,z',
	'y,-x+y,-z',
	'-y,x-y,z',
	'-y,x-y,-z',
	'x-y,x,z',
	'x-y,x,-z',
	'x-y,-y,z',
	'x-y,-y,-z',
	'-x+y,y,z',
	'-x+y,y,-z',
	'-x+y,-x,z',
	'-x+y,-x,-z',
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
		self.declareProperty('Axis Aligned', False, 'Perform binning aligned with the axes of the input MDEventWorkspace?')
		self.declareProperty('AlignedDim0', 'h,-3,3,1', StringMandatoryValidator(), 'Format: \'name,limits,bins\'')
		self.declareProperty('AlignedDim1', 'k,-3,3,1', StringMandatoryValidator(), 'Format: \'name,limits,bins\'')
		self.declareProperty(FloatArrayProperty(name='Output Bins',
												values=[50,50],
												validator=FloatArrayLengthValidator(2)),
			'The number of bins for each dimension of the OUTPUT workspace')
		self.declareProperty(FloatArrayProperty(name='Output Extents',
												values=[-5,8,-5,8],
												validator=FloatArrayLengthValidator(4)),
			'The minimum, maximum edges of space of each dimension of the OUTPUT workspace, as a comma-separated list')
		self.declareProperty(FloatArrayProperty(name='Translation',
												values=[0,0,0,0],
												validator=FloatArrayLengthValidator(4)),
			'Coordinates in the INPUT workspace that corresponds to (0,0,0) in the OUTPUT workspace')
		self.declareProperty('Normalise Basis Vectors', True, 'Normalize the given basis vectors to unity')
		self.declareProperty('BasisVector0', '', 'Format: \'name,units,x,y,z,dE\'. Leave blank for None.')
		self.declareProperty('BasisVector1', '', 'Format: \'name,units,x,y,z,dE\'. Leave blank for None.')
		self.declareProperty('BasisVector2', '', 'Format: \'name,units,x,y,z,dE\'. Leave blank for None.')
		self.declareProperty('BasisVector3', '', 'Format: \'name,units,x,y,z,dE\'. Leave blank for None.')
		self.declareProperty(WorkspaceProperty(name='Input Workspace',
												defaultValue='',
												direction=Direction.Input), 'An input MDWorkspace')


		self.setPropertySettings('AlignedDim0',VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsNotDefault))
		self.setPropertySettings('AlignedDim1', VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsNotDefault))
		self.setPropertySettings('Output Bins', EnabledWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('Output Extents', EnabledWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('Translation', EnabledWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('Normalise Basis Vectors', EnabledWhenProperty('Axis Aligned',PropertyCriterion.IsDefault))
		self.setPropertySettings('BasisVector0', VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('BasisVector1', VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('BasisVector2', VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))
		self.setPropertySettings('BasisVector3', VisibleWhenProperty('Axis Aligned', PropertyCriterion.IsDefault))

		align_grp = 'Axis-Aligned Binning'
		self.setPropertyGroup('Axis Aligned', align_grp)
		self.setPropertyGroup('AlignedDim0', align_grp)
		self.setPropertyGroup('AlignedDim1', align_grp)

		nonalign_grp = 'Non Axis-Aligned Binning'
		self.setPropertyGroup('Output Bins', nonalign_grp)
		self.setPropertyGroup('Output Extents', nonalign_grp)
		self.setPropertyGroup('Translation', nonalign_grp)
		self.setPropertyGroup('Normalise Basis Vectors', nonalign_grp)
		self.setPropertyGroup('BasisVector0', nonalign_grp)
		self.setPropertyGroup('BasisVector1', nonalign_grp)
		self.setPropertyGroup('BasisVector2', nonalign_grp)
		self.setPropertyGroup('BasisVector3', nonalign_grp)

		# ------------------------- Output properties ------------------------
		self.declareProperty(WorkspaceProperty(name='Binned Workspace',
												defaultValue='',
												direction=Direction.Output), 'A name for the output MDHistoWorkspace')

	def PyExec(self):
		sgNumber = self.getProperty('Space Group').value
		mdws = self.getProperty('Input Workspace').value
		Adim0 = self.getProperty('AlignedDim0').value
		Adim1 = self.getProperty('AlignedDim1').value
		basis0 = self.getProperty('BasisVector0').value
		basis1 = self.getProperty('BasisVector1').value
		basis2 = self.getProperty('BasisVector2').value
		basis3 = self.getProperty('BasisVector3').value
		axisAligned = self.getProperty('Axis Aligned').value
		normalizeBasisVectors = self.getProperty('Normalise Basis Vectors').value
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

		# Create a logger to store all errors and other information related to this particular algorithm
		log = Logger("SpaceGroupSymOps_log")

		# Change value of empty basis vectors to None to follow BinMD argument rules
		if len(basis0) is 0:
			log.fatal("Error: At least two basis vectors need to be defined. Cannot bin!")
		if len(basis1) is 0:
			log.fatal("Error: At least two basis vectors need to be defined. Cannot bin!")
		if len(basis2) is 0:
			basis2 = None
		if len(basis3) is 0:
			basis3 = None

		if axisAligned == True:
			translation = [0,0,0,0]
			basis0, extent0, bins0 = self.ConvertToNonAA(Adim0)
			basis1, extent1, bins1 = self.ConvertToNonAA(Adim1)
			basis2 = None
			basis3 = None

			outputExtents = [float(extent0[0]),float(extent0[1]),float(extent1[0]),float(extent1[1])]
			outputBins = [int(bins0),int(bins1)]

		binned_ws = BinMD(InputWorkspace=mdws, AxisAligned=False,
			BasisVector0=basis0, BasisVector1=basis1,
			BasisVector2=basis2, BasisVector3=basis3,
			NormalizeBasisVectors=normalizeBasisVectors, Translation=translation,
			OutputExtents=outputExtents, OutputBins=outputBins)
		
		if symChoice == "Symmetry Operations":
			binned_ws = self._symmetrize_by_generators(mdws, False, basis0, basis1, basis2, basis3,
				normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
				int(numOp), symOp1, symOp2, symOp3, symOp4, symOp5)
		else:
			binned_ws = self._symmetrize_by_sg(mdws, False, basis0, basis1, basis2, basis3,
				normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
				sgNumber)
		
		self.setProperty("Binned Workspace", binned_ws)


	def category(self):
		return 'PythonAlgorithms'


	def _symmetrize_by_sg(self, mdws, axisAligned, basis0, basis1, basis2, basis3,
		normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
		sgNumber):

		unit0, basisVec0 = self._destringify(basis0)
		unit1, basisVec1 = self._destringify(basis1)
		unit2, basisVec2 = self._destringify(basis2)
		unit3, basisVec3 = self._destringify(basis3)

		for index, item in enumerate(dict_sg[sgNumber]):
			basisVec0_str = None
			basisVec1_str = None
			basisVec2_str = None
			basisVec3_str = None

			if basisVec0 is not None:
				newBasisVec0 = dot(item, basisVec0)
				basisVec0_str = unit0[0] + ',' + unit0[1] + ',' + str(newBasisVec0[0]) \
							+ ',' + str(newBasisVec0[1]) + ',' + str(newBasisVec0[2]) + ',' + '0'
			if basisVec1 is not None:
				newBasisVec1 = dot(item, basisVec1)
				basisVec1_str = unit1[0] + ',' + unit1[1] + ',' + str(newBasisVec1[0]) \
							+ ',' + str(newBasisVec1[1]) + ',' + str(newBasisVec1[2]) + ',' + '0'
			if basisVec2 is not None:
				newBasisVec2 = dot(item, basisVec2)
				basisVec2_str = unit2[0] + ',' + unit2[1] + ',' + str(newBasisVec2[0]) \
							+ ',' + str(newBasisVec2[1]) + ',' + str(newBasisVec2[2]) + ',' + '0'
			if basisVec3 is not None:
				newBasisVec3 = dot(item, basisVec3)
				basisVec3_str = unit3[0] + ',' + unit3[1] + ',' + str(newBasisVec3[0]) \
							+ ',' + str(newBasisVec3[1]) + ',' + str(newBasisVec3[2]) + ',' + '0'
	
			newTranslation = translation + dict_t[sgNumber][index]

			binned_ws += BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
				BasisVector0=basisVec0_str, BasisVector1=basisVec1_str,
				BasisVector2=basisVec2_str, BasisVector3=basisVec3_str,
				NormalizeBasisVectors=normalizeBasisVectors, Translation=newTranslation,
				OutputExtents=outputExtents, OutputBins=outputBins)
		
		return binned_ws


	def _symmetrize_by_generators(self, mdws, axisAligned, basis0, basis1, basis2, basis3,
		normalizeBasisVectors, translation, outputExtents, outputBins, binned_ws,
		numOp, symOp1, symOp2, symOp3, symOp4, symOp5):
		
		unit0, basisVec0 = self._destringify(basis0)
		unit1, basisVec1 = self._destringify(basis1)
		unit2, basisVec2 = self._destringify(basis2)
		unit3, basisVec3 = self._destringify(basis3)

		symOpList = [symOp1, symOp2, symOp3, symOp4, symOp5]
		for i in range(numOp):
			basisVec0_str = None
			basisVec1_str = None
			basisVec2_str = None
			basisVec3_str = None

			s, newTranslation = self._get_symop_and_translation(symOpList[i])

			symOp = SymmetryOperationFactory.createSymOp(s)

			if basisVec0 is not None:
				coordinatesPrime0 = symOp.transformCoordinates(basisVec0)
				basisVec0_str = unit0[0] + ',' + unit0[1] + ',' + str(coordinatesPrime0.getX()) \
							+ ',' + str(coordinatesPrime0.getY()) + ',' + str(coordinatesPrime0.getZ()) + ',' + '0'
			if basisVec1 is not None:
				coordinatesPrime1 = symOp.transformCoordinates(basisVec1)
				basisVec1_str = unit1[0] + ',' + unit1[1] + ',' + str(coordinatesPrime1.getX()) \
							+ ',' + str(coordinatesPrime1.getY()) + ',' + str(coordinatesPrime1.getZ()) + ',' + '0'
			if basisVec2 is not None:
				coordinatesPrime2 = symOp.transformCoordinates(basisVec2)
				basisVec2_str = unit2[0] + ',' + unit2[1] + ',' + str(coordinatesPrime2.getX()) \
							+ ',' + str(coordinatesPrime2.getY()) + ',' + str(coordinatesPrime2.getZ()) + ',' + '0'
			if basisVec3 is not None:
				coordinatesPrime3 = symOp.transformCoordinates(basisVec3)
				basisVec3_str = unit3[0] + ',' + unit3[1] + ',' + str(coordinatesPrime3.getX()) \
							+ ',' + str(coordinatesPrime3.getY()) + ',' + str(coordinatesPrime3.getZ()) + ',' + '0'

			# Factor in for the original translation reading
			newTranslation += translation

			binned_ws += BinMD(InputWorkspace=mdws, AxisAligned=axisAligned,
				BasisVector0=basisVec0_str, BasisVector1=basisVec1_str,
				BasisVector2=basisVec2_str, BasisVector3=basisVec3_str,
				NormalizeBasisVectors=normalizeBasisVectors, Translation=newTranslation,
				OutputExtents=outputExtents, OutputBins=outputBins)

		return binned_ws


	def _destringify(self, basis):
		# Account for empty basis vectors
		if basis is None:
			return None, None

		temp = basis.split(',')
		unit = temp[0:2]
		temp = temp[2:-1]
		return unit, array([int(temp[0]), int(temp[1]), int(temp[2])])


	def _get_symop_and_translation(self, symOp):
		s_list = symOp.split(",")
		
		x_translation = 0
		y_translation = 0
		z_translation = 0
		
		for i, item in enumerate(s_list):
			if len(item) > 2:
				if i == 0:
					index = re.search("[xyz]", item).start()
					x_translation = item[index+1:]
					x_coord = item[:index+1]
					try:
						num, denom = x_translation.split('/')
						x_translation = float(num) / float(denom)
					except:
						x_translation = 0
						x_coord = item
				elif i == 1:
					index = re.search("[xyz]", item).start()
					y_translation = item[index+1:]
					y_coord = item[:index+1]
					try:
						num, denom = y_translation.split('/')
						y_translation = float(num) / float(denom)
					except:
						y_translation = 0
						y_coord = item
				elif i == 2:
					index = re.search("[xyz]", item).start()
					z_translation = item[index+1:]
					z_coord = item[:index+1]
					try:
						num, denom = z_translation.split('/')
						z_translation = float(num) / float(denom)
					except:
						z_translation = 0
						z_coord = item
			else:
				if i == 0:
					x_coord = item
				elif i == 1:
					y_coord = item
				elif i == 2:
					z_coord = item

		s = x_coord + ',' + y_coord + ',' + z_coord
		t = [x_translation, y_translation, z_translation, 0]

		return s, t


	def ConvertToNonAA(self,AlignedInput):
		temp = AlignedInput.split(',')
		name = temp[0]
		extent = temp[1:3]
		numbins = temp[3]

		#Build basis vector
		if name == 'h':
			BVect = 'h,rlu,1,0,0,0'
		elif name == 'k':
			BVect = 'k,rlu,0,1,0,0'
		elif name == 'l':
			BVect = 'l,rlu,0,0,1,0'
		elif name == 'E':
			BVect = 'E,eV,0,0,0,1'

		return BVect, extent, numbins


# Register algorithm with Mantid
AlgorithmFactory.subscribe(SpaceGroupSymOps)
