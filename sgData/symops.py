import sys, io


def unique_symops():
	f = open("symops_from_bilbao.txt", "r")
	symops = set()
	for line in f:
		if line not in symops:
			symops.add(line)
			sys.stdout.write(line)
	f.close()


def extract_from_dump():
	f = open("symops-dump.txt")
	for line in f:
		if line[0:5] == "<xyz>":
			print line[5:-8]
	f.close()

#extract_from_dump()
#unique_symops()