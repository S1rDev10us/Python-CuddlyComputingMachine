from random import choice,randint, choices,randrange, sample
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
		self.breakLine='+'+'-'*30+'+'
		self.emptyLine='|'+' '*30+'|'
		self.string=type("")
		self.startInv=self.data['start']
		self.startComplete=self.data['complete']
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
		self.completed=self.startComplete
		self.startAge=randint(25,50)
		self.age=self.startAge
		self.old=randint(100,150)
		self.gameTime=0
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
		events=[]
		for x in self.filterlist(self.events['events'],'place',self.location):
			if('predicate' in x.keys()):
				if(self.predicate(x['predicate'])):
					events.append(x)
			else:
				events.append(x)
		listweights=[]
		for x in events:
			if('weight' in x.keys()):
				listweights.append(x['weight'])
			else:
				match type(x['outcomes']):
					case self.number:
						listweights.append(0.25)
						pass
					case self.string:
						listweights.append(0.5)
						pass
					case self.array:
						listweights.append(1)
						pass
				
		event=choices(events,weights=listweights,k=1)[0]
		return event

	#Buyable items
	def availableItems(self):

		return

	#shop function
	def shop(self):
		self.shopLevel=self.rep/10
		shopping=True

		weatypes = [
		self.filterlist(self.weapons, "type", "me"),
		self.filterlist(self.weapons, "type", "ma"),
		self.filterlist(self.weapons, "type", "ra")
		]

		weapons = []
		samp = 0
		for i in range(len(weatypes)):
			if len(weatypes[i]) < 3:
				samp = len(weatypes[i])
			else:
				samp = 3
			weapons.append(sample(weatypes[i], samp))

		

		while(shopping):
			print(self.breakLine)
			print(self.emptyLine +'\n| Welcome to this shop, enjoy! |')
			print(self.emptyLine)
			print('|● 0 to Exit                   |')
			print('|● 1 for Weapons               |')
			print('|● 2 for Items                 |')
			print(self.emptyLine+'\n'+self.breakLine)
			print("Gold:", self.gold)

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
							print('|● 0 Back                      |')
							print('|● 1 for Melee                 |')
							print('|● 2 for Magic                 |')
							print('|● 3 for Ranged                |')
							print(self.breakLine)
							print("Gold:", self.gold)

							weaType = ""
							match self.validn(['b','m','m','r']):
								case 1:
									inweaType = 0
									weaType = "Melee"
								case 2:
									inweaType = 1
									weaType = "Magic"
								case 3:
									inweaType = 2
									weaType = "Ranged"
								case 0:
									WeaponBuy = False
								case _:
									print('Well done you broke the validator')
							if(WeaponBuy):
								passin = []
								for i in weapons[inweaType]:
									passin.append(i)
								passin.append("B")
								passin.append("L")
								FirsLoop = False

						if(WeaponBuy):
							print()
							print(self.breakLine)
							print(self.emptyLine)
							print(f'|         {weaType} weapons')
							print(self.emptyLine)
							print("|● 0 Back                      |\n|● 1 Show Lore")
							print(self.breakLine)
							for count, weapon in enumerate(weapons[inweaType]):
									print(f"|● {count+2} {weapon['name']}\n| Cost: {weapon['Cost']}")
							print(self.emptyLine)
							print(self.breakLine)
							print("Gold:", self.gold)

							selection = self.validn(passin)
							print()
							match selection:
								case 0:
									FirsLoop = True
								case 1:
									inLore = True
									weaLore = []
									for i in weapons[inweaType]:
										if('loreData' in i.keys()):weaLore.append(i["name"] + ": " + i["loreData"])
										else:weaLore.append(i["name"] + ": " + "No lore for this item")
									while(inLore):
										print(self.breakLine)
										print(self.emptyLine)
										print(f'|         {weaType} weapons')
										print("|            Lore              |\n|● 0 Back                      |")
										print(self.emptyLine)
										for weapon in weaLore:
												print("|●",self.strpara(weapon, menumode=True))
										print(self.emptyLine)
										print(self.breakLine)
										print("Gold:", self.gold)
										match self.validn('b'):
											case 0:
												inLore = False
											case _:
												print("you broke the validator")
								case _:
									# TODO allow buying weapons
									self.gold -= weapons[inweaType][selection-2]['Cost']
									self.weapons.remove(weapons[inweaType][selection-2])
									self.inventory["weapons"].append(weapons[inweaType][selection-2])
									weapons[inweaType].pop(selection-2)
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


	# every 30 characters, replaces a space with a newline
	def strpara(self, string, menumode=False):
		out = ""
		placenl = False
		for i, val in enumerate(string):
			if (i+1)%30 == 0:
				placenl = True
			if val == " " and placenl:
				out += "\n"
				if menumode:
					out += "|  "
				placenl = False
				continue
			else:
				pass
			out += val
		return out


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
		self.eventNonRandomManager(event)
	def eventNonRandomManager(self,event):
		print(event['text'])
		if(event['outcomes']=='shop'):
			self.shop()
		elif(type(event['outcomes'])==type(0)):
			if(self.confirm()):
				self.location=event['outcomes']
				print('\n'+self.messages('welcome')%self.locationf()['name'])
				if('complete' in self.locationf().keys()):self.completed.append(self.locationf()['complete'])
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
	def recursiveEventManager (self,event):
		if(event['output']=='shop'):
			self.shop()
		elif(type(event['output'])==type(0)):
			if(self.confirm()):
				self.location=event['outcomes']
				print('\n'+self.messages('welcome')%self.locationf()['name'])
				if('complete' in self.locationf().keys()):self.completed.append(self.locationf()['complete'])
				getch()
				print('\n'*2)
	#What to do at the end of an event
	def eventOutcome(self,outcome):
		if(type(outcome['output'])==self.string):
			print('\n'+outcome['output'])
			self.statEffectsRand(outcome)
			if('complete' in outcome.keys()):self.completed.append(outcome['complete'])
			if('inventory' in outcome.keys()):
				print('outcome')
				for x in outcome['inventory'].keys():
					for z in outcome['inventory'][x]:
						self.inventory[x].append(z)
					pass
		else:
			if(type(outcome['output'])==self.dict):self.eventOutcome(outcome['output'][f"{str(self.predicate(outcome['output']['predicate'])).lower()}"])
			else:self.recursiveEventManager(outcome['output'][f"{str(self.predicate(outcome['output']['predicate'])).lower()}"])
		pass
	#completed, checks if a condition is done
	def complete(self,check):
		return check in self.completed
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
		check =list(condition.keys())[0]
		match check:
			case 'has':
				for z in self.inventory:
					for x in self.inventory[z]:
						for y in condition[check]:
							if(y in x):
								if(x[y]==condition[check][y]):
									return True
						if(len(condition[check].keys())<1):
							raise Exception(f"The predicate did not have any values\nThe predicate was {condition}")
				return False
			case 'rep':
				if(condition[check]['greater']):
					if(condition[check]['rep']<self.rep):return True
				else:
					if(condition[check]['rep']>self.rep):return True
				pass
			case 'gold':
				if(condition[check]['greater']):
					if(condition[check]['gold']<self.gold):return True
				else:
					if(condition[check]['gold']>self.gold):return True
				pass
			case 'health':
				if(condition[check]['greater']):
					if(condition[check]['health']<self.health):return True
				else:
					if(condition[check]['health']>self.health):return True
				pass
			case 'reference':
				return self.predicate(self.predicates[condition[check]])
				pass
			case 'complete':
				return self.complete(condition['complete'])
				pass
			case 'not':
				return (not self.predicate(condition[check]))
				pass
			case 'chance':
				precision = 1/0.001
				chance= randrange(0, floor(1*precision), 1)/precision
				outcome=chance < condition[check]
				return outcome
				pass
			case _:
				raise Exception(f"The predicate {check} is not supported\nThe entire predicate is:\n{condition}")
		return False
	#statistics
	def stats(self):
		for x in self.inventory.keys():
			print('\n'+self.breakLine)
			print(x+'\n')
			
			for z in self.inventory[x]:
				print(f"● {z['name']}")
				if('loreData' in z.keys()):
					print('Lore: '+z['loreData'])
				if('type' in z.keys()):
					print('Type: '+self.short(z['type']))
		print(self.breakLine)
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
		self.statEffects(self.locationf())
		if(self.gold<0):
			self.health+=floor(self.gold/10)
			print('You were mugged by the gangs that you are indebted to')
			getch()
	#start an event based on an id (dev only)
	def eventFromId(self,id):
		self.eventNonRandomManager(self.filterlist(self.events['events'],'id',id)[0])
		self.stats()
	#affect health, gold and rep based on dictionary
	def statEffects(self,thing):
		if('gold' in thing.keys()):self.gold+=thing['gold']
		if('rep' in thing.keys()):self.rep+=thing['rep']
		if('health' in thing.keys()):
			if(thing['health']=='kill'):
				self.health=0
			else:
				self.health+=thing['health']
	def statEffectsRand(self,outcome):
		if('gold' in outcome.keys()):
			if(outcome['gold']>0):
				self.gold+=outcome['gold']+randint(0,floor(outcome['gold']/10))
			else:
				self.gold+=outcome['gold']+randint(floor(outcome['gold']/10),0)
		if('rep' in outcome.keys()):
			if(outcome['rep']>0):
				self.gold+=outcome['rep']+randint(0,floor(outcome['rep']/10))
			else:
				self.gold+=outcome['rep']+randint(floor(outcome['rep']/10),0)
		if('health' in outcome.keys()):
			if(outcome['health']=='kill'):
				self.health=0
			else:
				if(outcome['health']>0):
					self.health+=outcome['health']+randint(0,floor(outcome['health']/10))
				else:
					self.health+=outcome['health']+randint(floor(outcome['health']/10),0)
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
# runtime.gold = 99999999999999999
# runtime.shop()
runtime.start()
print('Would you like to play again?')
while(runtime.confirm()):
	runtime.start()
	print('Would you like to play again?')
