import mantid
from mantid.simpleapi import *
from mantid.api import * 
import time
execfile("/home/sachi/scripts/SpaceGroupSymOps.py")
#execfile("/Users/etotheipiplusone/Documents/git/mantid-non-aligned-axes-symops/SpaceGroupSymOps.py")


def get_path(numbers):
	return ["/export/scratch0/ggm/data/SNS/SEQ/IPTS-13291/shared/autoreduce/SEQ_" + str(number) + "_autoreduced.nxs" for number in numbers]
	#return ["/Users/etotheipiplusone/Documents/git/mantid-symmetrization/autoreduce/SEQ_" + str(number) + "_autoreduced.nxs" for number in numbers]


def get_background(runs_bg, UBmatrix):
	datafile = ",".join(get_path(runs_bg))
	mate_bg = Load(Filename=datafile) # Output is an Event Workspace

	LoadIsawUB(InputWorkspace=mate_bg, FileName=UBmatrix) # Load UB Matrix
	SetGoniometer(mate_bg, Axis0="DataRot,0,1,0,1", Axis1="0,0,1,0,1") # Set Goniometer

	mdws = ConvertToMD(InputWorkspace=mate_bg, OutputWorkspace='mde_bg', dEAnalysisMode='Direct', QDimensions='Q3D', Q3DFrames='HKL', QConversionScales='HKL',
                       OverwriteExisting=True) # Output is an MDEvent Workspace
	merge_bg = MergeMD(InputWorkspaces=mdws) # Merge all background files
	return merge_bg


# Some constants
AVERAGE_BACKGROUND = True # Account for background noise?
COMPRESS_BACKGROUND = False # Not used for now


# Signal runs
run_sg1 = range(79412,79436)
run_sg2 = range(79438,79462)
run_sg3 = range(79463,79556)
run_sg4 = range(79557,79597)
run_sg5 = range(79599,79607)
runs_sg = run_sg1+run_sg2+run_sg3+run_sg4+run_sg5
#runs_sg = range(79412, 79416)

# Background run
runs_bg = range(79616,79649,1)


# Clear any workspaces
mtd.clear()


datafile = ",".join(get_path(runs_sg))
UBmatrix = "/home/sachi/data/ubmatrix13291.mat"
#datafile = "/Users/etotheipiplusone/Documents/git/mantid-symmetrization/autoreduce/SEQ_79470_autoreduced.nxs"
#UBmatrix = "/Users/etotheipiplusone/Documents/git/mantid-symmetrization/data/ubmatrix13291.mat"


# Load signal files
start = time.time()
mate_sg = Load(Filename=datafile) # Output is an Event Workspace
finish = time.time()
print "Loading datafiles took %.2f seconds" % (finish-start)

# Load UB Matrix
LoadIsawUB(InputWorkspace=mate_sg, FileName=UBmatrix)

# Set Goniometer
start = time.time()
SetGoniometer(mate_sg, Axis0="CCR22Rot,0,1,0,1", Axis1="0,0,1,0,1")
finish = time.time()
print "Setting goniometer took %.2f seconds" % (finish-start)

start = time.time()
mdws = ConvertToMD(InputWorkspace=mate_sg, OutputWorkspace='mde_sg', dEAnalysisMode='Direct', QDimensions='Q3D', Q3DFrames='HKL', QConversionScales='HKL',
                       OverwriteExisting=True) # Output is an MDEvent Workspace
finish = time.time()
print "MD workspace generation took %.2f seconds" % (finish-start)

merge_sg = MergeMD(InputWorkspaces=mdws) # Merge all signal files
if AVERAGE_BACKGROUND:
	merge_bg = get_background(runs_bg, UBmatrix)
	merge_sg = merge_sg - merge_bg


#print (AlgorithmFactoryImpl.Instance()).exists("SpaceGroupSymOps")
#print S.isExecuted()
#print S.orderedProperties()

#S = Algorithm.fromString("SpaceGroupSymOps")
# For some reason the above line doesn't work on Unix, so use the following instead
S = SpaceGroupSymOps()

# Initialize
S.initialize()

# Set property values
S.setProperty("InputWorkspace", merge_sg)
S.setProperty("SymmetrizationBy", "Space Group")
S.setProperty("SpaceGroup", "198")
S.setProperty("AxisAligned", False)
#S.setProperty("OutputBins", [50,50,1,1])
S.setProperty("OutputBins", [170,200,1,250]) # Same as Guy's settings
#S.setProperty("OutputExtents", [-5,5,-5,5,-0.5,0.5,6,10])
S.setProperty("OutputExtents", [-6,6,-5,5,-0.05,0.05,-3,58]) # Same as Guy's settings
S.setProperty("BasisVector0", "a,unit,1,1,0,0")
S.setProperty("BasisVector1", "b,unit,0,0,1,0")
S.setProperty("BasisVector2", "c,unit,1,-1,0,0")
S.setProperty("BasisVector3", "E,unit,0,0,0,1")
S.setProperty("Binned Workspace", "outputWS")

#Execute
start = time.time()
S.execute()
finish = time.time()
print "SpaceGroupSymOps execution took %.2f seconds" % (finish-start)
