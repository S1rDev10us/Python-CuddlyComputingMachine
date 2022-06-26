from json import loads, dumps, dump
def read(filen):
	f = open(filen, "r")
	filecont = (f.read())
	f.close()
	return filecont
def readjs(filen):
	f = open(filen, "r")
	filecont = loads(f.read())
	f.close()
	return filecont
def write(content,filen):
	f = open(filen, "w")
	f.write(content)
	f.close()
def writejs(jsonf,filen):
	f = open(filen, "w")
	f.write(dumps(jsonf))
	f.close()
def overwritejs(json, file):
	file.seek(0)
	dump(json, file, indent=4)