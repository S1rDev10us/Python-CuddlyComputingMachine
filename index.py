from random import choice,randint
from files import *
dev=False

class game:
	def __init__(self):
		self.reset()
		self.data=readjs('C:/Users/S1rDe/OneDrive/Desktop/Python/Revision-projects/2nd-project/data.json')
		self.events=self.data['events']
		self.weapons=self.data['weapons']
		self.message=self.data['messages']
		self.shorthands=self.data['shorthands']
		
		if(dev==False):
			found=True
			while(found):
				found=False
				for x in range(len(self.weapons)):
					if(self.weapons[x]['dev']):
						self.weapons.pop(x)
						found=True
						break
	#reset all variables for game start
	def reset(self):
		self.food=100
		self.health=100
		self.age=randint(25,50)

	#Look for a specific shorthand
	def short(self,short):
		for x in self.shorthands:
			if(x['short']==short):
				longhand=x['long']
				break
		return longhand

	#Check if character is alive
	def alive(self):
		return self.health>0
	
	#Get the messages for a specific section
	def messages(self,target):
		for x in self.message:
			if(x['name']==target):
				match x['type']:
					case 'string':
						return x['data']
					case 'array':
						return choice(x['data'])
					case _:
						return choice(x['data'])

	#Choose an event
	def event(self):

		return
		pass

	#Main gameplay loop
	def start(self):
		self.reset()
		print(self.messages('start'))
		while(self.alive()):
			break



runtime = game()
runtime.start()
while(input('Would you like to play again?(y/n)\n>>>').lower()=='y'):
	runtime.start()