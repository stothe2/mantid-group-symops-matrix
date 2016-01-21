import io


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

#extract_from_dump()
#unique_symops()
compare_symops()