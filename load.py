from files import *
from os import listdir, path
print(path.abspath('extensions/'))
for x in listdir(path.abspath('extensions/')):
	print(x)