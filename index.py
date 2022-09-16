from os.path import abspath
from os import listdir
from game import game
from PythonHelper import files

games:list[dict[str,any]]=[]
config=files.readjs('./config.json')
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
    games.append({"loc":abspath(gameLocation+file),"id":Id})
del file
for file in enumerate(games):
    file=games[file[0]]
    data=files.readjs(file['loc'])
    file['version']=data['version']
    # file['data']=



print(games)