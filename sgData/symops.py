import io
from mantid.geometry import SpaceGroupFactory
from mantid.geometry import PointGroupFactory

def unique_symops():
	f = open("symops_from_bilbao.txt", "r")
	symops = set()
	for line in f:
		line = line.rstrip("\n")
		if line not in symops:
			symops.add(line)
			print line
	f.close()


def extract_from_dump():
	f = open("symops-dump.txt")
	for line in f:
		if line[0:5] == "<xyz>":
			print line[5:-8]
	f.close()


def compare_symops():
	f = open("unique_symops_from_mantid.txt", "r")
	mantidSymOps = set()
	for line in f:
		line = line.rstrip("\n")
		mantidSymOps.add(line)
	f.close()
	
	f = open("unique_symops_from_bilbao.txt", "r")
	bilbaoSymOps = set()
	for line in f:
		line = line.rstrip("\n")
		bilbaoSymOps.add(line)
	f.close()

	for e in mantidSymOps - bilbaoSymOps:
		print e

def format():
	f = open("SymmetryList.txt", "r")
	for line in f:
		line = line.rstrip("\n")
		print "'" + line + "',"
	f.close()


def check_registered_sg():
	pg = PointGroupFactory.getAllPointGroupSymbols()
	for item in pg:
		print "'" + item + "',"


def sg_test():
	hmsymbol = str(SpaceGroupFactory.subscribedSpaceGroupSymbols(198))[2:-2] #Eliminate quotes and brackets
	sg = SpaceGroupFactory.createSpaceGroup(hmsymbol) 
	pg = PointGroupFactory.createPointGroupFromSpaceGroup(sg)
	SymOps = pg.getSymmetryOperations()

	for j, op in enumerate(SymOps):
	    coordinatesPrime = op.transformCoordinates(coordinates)
	    print coordinatesPrime


#extract_from_dump()
#unique_symops()
#compare_symops()
#format()
#check_registered_sg()