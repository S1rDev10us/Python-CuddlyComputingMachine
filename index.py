from random import choice,randint, choices
from files import *
from os import path, system
from math import floor
#from msvcrt import getch
#from time import sleep
#from keyboard import wait as getch
dev=False
def getch():
	system('pause')
class game:
	def __init__(self):
		self.data=readjs(path.abspath('data.json'))
		self.events=self.data['events']
		self.weapons=self.data['weapons']
		self.message=self.data['messages']
		self.shorthands=self.data['shorthands']
		self.breakLine='-'*32
		self.emptyLine='|'+' '*30+'|'
		self.string=type("")
		self.startInv=self.data['start']
		self.array=type([])
		self.dict=type({})
		self.predicates=self.data['predicates']
		self.number=type(0)
		if(not dev):
			remove_list=self.filterlist(self.weapons,'dev',True)
			self.weapons=[i for i in self.weapons if i not in remove_list]
		self.reset()
	#reset all variables for game start
	def reset(self):
		self.inventory=self.startInv
		self.startAge=randint(25,50)
		self.age=self.startAge
		self.old=randint(100,150)
		self.gameTime=0
		self.food=100
		self.health=100
		self.gold=0
		self.location=0
		self.rep=0
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
			if(x==short):
				return self.shorthands[x]
		raise Exception(f"Shorthand \"{short}\" was not found")

	#Check if character is alive
	def alive(self):
		alive=self.health>0
		if(self.age>=self.old):
			alive=False
			print('\n'*5+self.messages('retire') % self.age)
		elif(self.health<=0):
			print('\n'*5+self.messages('death'))
		return alive
	
	#Get the messages for a specific section
	def messages(self,target):
		for x in self.message:
			if(x==target):
				match type(self.message[x]):
					case self.string:
						return self.message[x]
					case self.array:
						return choice(self.message[x])
					case _:
						return choice(self.message[x])
		raise Exception(f"Message \"{target}\" was not found")
	#Choose an event
	def event(self):
		events=self.filterlist(self.events['events'],'place',self.location)
		listweights=[]
		for x in events:
			if('weight' in x.keys()):
				listweights.append(x['weight'])
			else:
				listweights.append(1)
		event=choices(events,weights=listweights,k=1)[0]
		return event

	#Buyable items
	def availableItems(self):

		return

	#shop function
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
				case 1:
					WeaponBuy = True
					FirsLoop = True
					while(WeaponBuy):
						if(FirsLoop):
							print(self.breakLine)
							print(self.emptyLine)
							print('|         Weapons shop         |')
							print(self.emptyLine)
							print('|● 0 Back           		      |')
							print('|● 1 for Melee                 |')
							print('|● 2 for Magic                 |')
							print('|● 3 for Ranged                |')
							print(self.breakLine)

							weapons = []
							weaType = ""
							match self.validn(['b','m','m','r']):
								case 1:
									weapons = self.filterlist(self.weapons, "type", "me")
									weaType = "Melee"
								case 2:
									weapons = self.filterlist(self.weapons, "type", "ma")
									weaType = "Magic"
								case 3:
									weapons = self.filterlist(self.weapons, "type", "ra")
									weaType = "Ranged"
								case 0:
									WeaponBuy = False
								case _:
									print('Well done you broke the validator')
							if(WeaponBuy):
								passin = weapons
								passin.append("B")
								passin.append("L")
								FirsLoop = False

						# TODO pick three random weapons instead of the whole list
						if(WeaponBuy):
							print(self.breakLine)
							print(self.emptyLine)
							print(f'|         {weaType} weapons')
							print(self.emptyLine)
							print("|● 0 Back\n|● 1 Show Lore")
							for count, weapon in enumerate(weapons):
									if weapon == "B" or weapon == "L":#<<<<|
										pass#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|<--temp fix
									else:#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
										print("|● " + str(count+2) + " " + weapon["name"])
							print(self.emptyLine)
							print(self.breakLine)
							slection = self.validn(passin)
							match slection:
								case 0:
									FirsLoop = True
								case 1:
									print("this function is a work in progress")
								case _:
									print("this function is a work in progress")

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
					print('Well done I guess, you broke the validator?')
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
			self.eventOutcome(outcome)
			getch()
	#What to do at the end of an event
	def eventOutcome(self,outcome):
		if(type(outcome['output'])==self.string):
			print('\n'+outcome['output'])
			if('gold' in outcome):
				if(outcome['gold']>0):
					self.gold+=outcome['gold']+randint(0,floor(outcome['gold']/10))
				else:
					self.gold+=outcome['gold']+randint(floor(outcome['gold']/10),0)
			if('rep' in outcome):
				if(outcome['rep']>0):
					self.gold+=outcome['rep']+randint(0,floor(outcome['rep']/10))
				else:
					self.gold+=outcome['rep']+randint(floor(outcome['rep']/10),0)
			if('health' in outcome):
				if(outcome['health']>0):
					self.health+=outcome['health']+randint(0,floor(outcome['health']/10))
				else:
					self.health+=outcome['health']+randint(floor(outcome['health']/10),0)
		else:
			if(self.predicate(outcome['output']['predicate'])):
				outcome=outcome['output']['true']
			else:
				outcome=outcome['output']['false']
				pass
			print('\n'+outcome['output'])
			if('gold' in outcome):
				if(outcome['gold']>0):
					self.gold+=outcome['gold']+randint(0,floor(outcome['gold']/10))
				else:
					self.gold+=outcome['gold']+randint(floor(outcome['gold']/10),0)
			if('rep' in outcome):
				if(outcome['rep']>0):
					self.gold+=outcome['rep']+randint(0,floor(outcome['rep']/10))
				else:
					self.gold+=outcome['rep']+randint(floor(outcome['rep']/10),0)
			if('health' in outcome):
				if(outcome['health']>0):
					self.health+=outcome['health']+randint(0,floor(outcome['health']/10))
				else:
					self.health+=outcome['health']+randint(floor(outcome['health']/10),0)
			pass
		pass
	#predicate system
	def predicate(self,condition):
		if(type(condition)==self.array):
			z=0
			for x in condition:
				if(self.singlePredicate(x)):
					z+=1
			if(z==len(condition)):
				return True
		else:
			return self.singlePredicate(condition)
		return False
	#code for one predicate
	def singlePredicate(self,condition):
		match condition['condition']:
			case 'has':
				for z in self.inventory:
					for x in self.inventory[z]:
						for y in condition['predicate']:
							if(y in x):
								if(x[y]==condition['predicate'][y]):
									return True
						if(len(condition['predicate'].values())<1):
							raise Exception(f"The predicate did not have any values\nThe predicate was {condition}")
				return False
			case 'rep':
				if(condition['greater']):
					if(condition['rep']<self.rep):return True
				else:
					if(condition['rep']>self.rep):return True
				pass
			case 'predicate':
				return self.predicate(self.predicates[condition['predicate']])
			case _:
				raise Exception(f"The predicate {condition['condition']} is not supported\nThe entire predicate is:\n{condition}")
		return False
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