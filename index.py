from os.path import abspath
from os import listdir
from game import game
from PythonHelper import files

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
    print(file)
    if(not file.endswith('.json')):continue
    print('file passed tests')
    Id=''
    
    for i in file.split('.')[:-1]:Id+=i
    games.append({"loc":abspath(f"{gameLocation}\\{file}"),"id":Id})
del file
for file in enumerate(games):
    file=games[file[0]]
    data=files.readjs(file['loc'])
    file['version']=data['version']
    # file['data']=



print(games)