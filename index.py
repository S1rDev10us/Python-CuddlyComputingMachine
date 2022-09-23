from os.path import abspath
from os import listdir
from game import game
from PythonHelper import files
from PythonHelper.logger import Logger

logger=Logger(Logger.INFO)

games:list[dict[str,any]]=[]

#create empty config file if it doesn't exist
if(not 'config.json' in listdir('./')):
	files.writejs({},'./config.json')

config=files.readjs('./config.json')

if(not 'games' in config):
	config['games']=files.FolderPicker(Force=False,Title="Pick a game directory")
	if(config['games']==None):raise Exception("The game directory was not specified")

if(not 'saves' in config):
	config['saves']=files.FolderPicker(Force=False,Title="Pick a savegame directory")
	if(config['saves']==None):raise Exception("The savegame directory was not specified")

#Save config file
files.writejs(config,'./config.json')

gameLocation:str=config['games']
gameLocationFiles=listdir(gameLocation)
saveLocation:str=config['saves']
saveLocationFiles=listdir(saveLocation)


for file in gameLocationFiles:
	if(not file.endswith('.json')):continue
	if(file in saveLocationFiles):continue
	files.writejs({},abspath(f"{saveLocation}\\{file}"))
	pass
del file

for file in gameLocationFiles:
	logger.log.debug(file)
	if(not file.endswith('.json')):continue
	logger.log.debug('file passed tests')
	Id=''
	
	for i in file.split('.')[:-1]:Id+=i
	games.append({"loc":abspath(f"{gameLocation}\\{file}"),"id":Id})
del file
for file in enumerate(games):
	file=games[file[0]]
	data=files.readjs(file['loc'])
	file['version']=data['version']
	# file['data']=



logger.log.debug(games)
tempList={}
for x in games:
	tempList[x['version']['name']]=x['version']['name'] in tempList
for x,y in enumerate(games):
	Id=y['id']
	newLine='\n'
	if('author'in y['version']):
		Author=y['version']['author']
	if('version' in y['version']):
		version=y['version']['version']
	if('link'in y['version']):
		link=y['version']['link']
	print(f"{x}: {y['version']['name']}{f'{newLine}   #{Id}' if tempList[y['version']['name']] else ''}{f'{newLine}   V {version}'if 'version' in y['version']else ''}{f'{newLine}By: {Author}'if ('author' in y['version']) else''}{f'{newLine}Website: {link}'if ('link' in y['version']) else''}")
	del Id



def ValidNumber(Max:int,Min:int=0) -> int:
	outcome=input('>>>')
	f=True
	outcomed=True
	while(outcomed):
		if(f!=True):
			outcome=input('Please enter a valid number\n>>>')
		f=False
		if(outcome.isdigit()):
			outcome=int(outcome)
			if(outcome>=Min and outcome<=Max):break
	return outcome


gameChoice=ValidNumber(len(games)-1)

runtime=game(games[gameChoice]['loc'],f"{saveLocation}\\{games[gameChoice]['id']}.json")
runtime.start()