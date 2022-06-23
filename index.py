from random import choice,randint
from files import *
from os import path, system
#from msvcrt import getch
#from time import sleep
#from keyboard import wait as getch
dev=True
def getch():
	system('pause')
class game:

	def __init__(self):
		self.reset()
		self.data=readjs(path.abspath('data.json'))
		self.events=self.data['events']
		self.weapons=self.data['weapons']
		self.message=self.data['messages']
		self.shorthands=self.data['shorthands']
		self.breakLine='-'*32
		self.emptyLine='|'+' '*30+'|'
		self.string=type("")
		self.array=type([])
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
		self.gameTime=0
		self.food=100
		self.health=100
		self.startAge=randint(25,50)
		self.age=self.startAge
		self.old=randint(100,150)
		self.location=0
		self.gold=0
		self.rep=0
		self.inventory = {
			"items": [],
			"weapons": [],
			"accessories": []
		}
	#confirmation function
	def confirm(self):
		x=input('y/n:')
		while(not (x=='y' or x =='n')):
			x=input('y/n:')
		return x=='y'
	#get a formatted location
	def locationf(self):
		return self.events["places"][self.location]
	
	#Look for a specific shorthand
	def short(self,short):
		for x in self.shorthands:
			if(x['short']==short):
				longhand=x['long']
				break
		return longhand

	#Check if character is alive
	def alive(self):
		alive=self.health>0
		if(self.age>=self.old):
			alive=False
			print('\n'*5+self.messages('retire') % self.age)
		elif(self.health<=0):
			print('\n'*5+self.messages('lose'))
		return alive
	
	#Get the messages for a specific section
	def messages(self,target):
		for x in self.message:
			if(x['name']==target):
				match type(x['data']):
					case self.string:
						return x['data']
					case self.array:
						return choice(x['data'])
					case _:
						return choice(x['data'])

	#Choose an event
	def event(self):
		return choice(self.filterlist(self.events['events'],'place',self.location))

	#Buyable items
	def availableItems(self):

		return

	# displays a shop with multiple options
	# and allows to by things
	def shop(self):
		self.shopLevel=self.rep/10
		shopping=True

		while(shopping):

			print(self.breakLine)
			print(self.emptyLine +'\n| Welcome to this shop, enjoy! |')
			print(self.emptyLine)
			print('|● 0 to Exit                   |')
			print('|● 1 for Weapons               |')
			print('|● 2 for Items                 |')
			print(self.emptyLine+'\n'+self.breakLine)

			number=self.validn(['e','w','i'])
			match number:
				# weapons menu
				# allows to choose between
				# three types of weapon  
				case 1:

					print(self.breakLine)
					print(self.emptyLine)
					print('|         Weapons shop         |')
					print(self.emptyLine)
					print('|● 0 for Melee                 |')
					print('|● 1 for Magic                 |')
					print('|● 2 for Ranged                |')
					print(self.breakLine)

					WeaponOut = ""
					opt = self.validn(['m','m','r'])
					weaType = ""
					# the following cases will store all the weapons of a given type
					# in a list, then output the items in a menu format where the items
					# can be selected in a menu format
					match opt:
						case 0:
							weapons = self.filterlist(self.weapons, "type", "me")
							weaType = "Melee"
						case 1:
							weapons = self.filterlist(self.weapons, "type", "ma")
							weaType = "Magic"
						case 2:
							weapons = self.filterlist(self.weapons, "type", "ra")
							weaType = "Ranged"
						case _:
							print('Well done you broke the validator')
					print(self.breakLine+'\n'+self.emptyLine)
					print(f'|         {weaType} weapons')
					for count, weapon in enumerate(weapons):
						WeaponOut += "|● " + str(count) + " " + weapon["name"] +'\n'
					print(self.breakLine)
				case 2:
					pass
				case 0:
					shopping=False
					print(self.breakLine)
					print(self.emptyLine)
					print("|     Thanks for shopping!     |")
					print(self.emptyLine)
					print(self.breakLine)
					pass
				case _:
					print('Well done i guess, you broke the validator?')
					pass
			
	#valid number
	def validn(self,check):
		outcome=input('>>>')
		f=True
		outcomed=True
		while(outcomed):
			if(f!=True):
				outcome=input('Please enter a valid number\n>>>')
			f=False
			if(outcome.isdigit()):
				try:
					check[int(outcome)]
					outcomed=False
				except:
					pass
		return int(outcome)

	#check if a variable exists
	def exists(self,exists):
		return exists!=None

	#run the event
	def eventManager(self):
		event=self.event()
		print(event['text'])
		if(event['outcomes']=='shop'):
			self.shop()
		elif(type(event['outcomes'])==type(0)):
			if(self.confirm()):
				self.location=event['outcomes']
				print('\n'+self.messages('welcome')%self.locationf()['name'])
				getch()
				print('\n'*2)
		else:
			print('Do you?')
			for x in range(len(event['outcomes'])):
				print(f"{str(x)}: {event['outcomes'][x]['name']}")
			outcome=self.validn(event["outcomes"])
			outcome=event["outcomes"][int(outcome)]
			print('\n'+outcome['output'])
			if(self.exists(outcome['gold'])):self.gold+=outcome['gold']+randint(0,int(outcome['gold']/10))
			if(self.exists(outcome['rep'])):self.rep+=outcome['rep']+randint(0,int(outcome['rep']/10))
			if(self.exists(outcome['health'])):self.health+=outcome['health']+randint(0,int(outcome['health']/10))
			getch()
	#predicate system
	def predicate(self,condition):
		if(type(condition)==self.array):
			z=0
			for x in condition:
				match x['condition']:
					case 'has':
						pass
					case 'rep':
						if(x['greater']):
							if(x['rep']<self.rep):
								z+=1
						pass
			if(z==len(condition)):
				pass
		else:
			pass

	#statistics
	def stats(self):
		print('\nYou now have:')
		print(f'●{self.gold} gold')
		print(f'●{self.rep} reputation')
		print(f'●{self.health} health')
		print(f'●{self.age} age\n')
	#filter function
	def filterlist(self,thelist,key,value):
		newlist=[]
		for x in thelist:
			if(x[key]==value):
				newlist.append(x)
		return newlist
	#environmental things such as slow damage from heat in hell
	def environmentalEffects(self):
		self.gold+=self.locationf()['gold']
		self.rep+=self.locationf()['rep']
		self.health+=self.locationf()['health']
	#Main gameplay loop
	def start(self):
		self.reset()
		print(self.messages('start')+'\n')
		print(self.messages('welcome')%self.locationf()['name'])
		getch()
		print('\n'*2)
		while(self.alive()):
			self.eventManager()
			self.environmentalEffects()
			self.gameTime+=1
			if(self.age!=self.startAge+self.gameTime//10):
				self.age=self.startAge+self.gameTime//10
				print(f'\nHappy Birthday, you are now {self.age}!')
				getch()
			self.stats()
				
		







runtime = game()
runtime.start()
print('Would you like to play again?')
while(runtime.confirm()):
	runtime.start()
	print('Would you like to play again?')