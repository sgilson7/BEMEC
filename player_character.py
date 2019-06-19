import random
import randomgenerator
import basicfight
from collections import OrderedDict
import math
import mapmodule
import weapon
class PlayerCharacter(object):

	def __init__(self, name, chartype, level):
		self.name = name
		if not name:
			self.name = randomgenerator.RandomAssetGenerator('basic_name', 3).generate_random_title()
		self.chartype = chartype
		self.level = level
		self.maxhealth = 0
		self.maxmana = 0
		self.health = 0
		self.mana = 0
		self.weapon = None
		self.combat_arts = {}
		self.avaialable_combat_arts = None
		self.maxstat = 100
		self.strength = 1
		self.intelligence = 1
		self.dexterity = 1
		if self.chartype == 1:
			self.maxhealth = 10
			self.maxmana = 10
			self.health = self.maxhealth
			self.mana = self.maxmana
			#weapon_formula_wand = lambda s, d, i, h, m, r: i
			#weapon_formula_readable = 'i'
			#self.weapon = weapon.Weapon('Basic Wand', weapon_formula_wand, weapon_formula_readable, 1, (0, 0, 0))
			self.combat_arts = {}
			#2 : ('Minor Mana Flare', 2, lambda s, d, i, h, m: 1.2 * m )
			self.avaialable_combat_arts = OrderedDict([
				(2 , ('MinorManaFlare', 2, lambda s, d, i, h, m, r: 1.2 * m * r)),
				(3, ('ManaBurn', 2, lambda s, d, i ,h, m, r: i + (1.1 * m * r)))])
			# in format name, mana cost, damage function
			# damage function in order: str, dex, int, health, mana, random element

		self.exp = 0
		self.reward = random.randint(self.level * 50, self.level * 150)
		self.nextlevel = 100

		for i in range(self.level - 1):
			r = random.randint(0, 2)
			if r == 0:
				self.strength = self.strength + 1
			elif r == 1:
				self.dexterity = self.dexterity + 1
			elif r == 2:
				self.intelligence = self.intelligence + 1
			self.maxhealth += self.strength

		self.health = self.maxhealth

		self.random_weapon()

	def random_weapon(self):
		random_generator = randomgenerator.RandomAssetGenerator('weapon', 3)
		random_weapon = random_generator.generate_random_weapon(self.level)
		self.equip_weapon(random_weapon)


	def equip_weapon(self, weapon):
		self.weapon = weapon
		buffs = self.weapon.equip()
		self.strength += buffs[0]
		self.intelligence += buffs[1]
		self.dexterity += buffs[2]

	def unequip_weapon(self):
		buffs = self.weapon.unequip()
		self.strength += buffs[0]
		self.intelligence += buffs[1]
		self.dexterity += buffs[2]
		self.weapon = None


	def level_up(self):
		print("Congratulations! You have leveled up!\n")
		self.print_stats()
		choice = input("Choose S: +1 Strength\nI: +1 Intelligence\nD: +1 Dexterity\n")
		if choice == 's':
			self.strength = self.strength + 1
		elif choice == 'i':
			self.intelligence = self.intelligence + 1
		else:
			self.dexterity = self.dexterity + 1
		self.level = self.level + 1
		self.maxhealth += 5
		self.health = self.maxhealth
		self.check_combat_art_add()

	def check_combat_art_add(self):
		thresholds = [2, 3]
		if self.level in thresholds:
			combat_art = self.avaialable_combat_arts[self.level]
			self.combat_arts[combat_art[0]] = (combat_art[1], combat_art[2])
			print('Congratulations! You learned %s!' %combat_art[0])
			self.print_combat_arts()

	def print_combat_arts(self):
		print('Current Combat Arts:')
		# counter = 0
		for combat_art in self.combat_arts:
			# print('%d: %s' % (counter, combat_art))
			print(combat_art)

	def check_can_level(self):
		while self.exp > self.nextlevel:
			self.level_up()
			self.nextlevel = self.nextlevel * 2

	def add_exp(self, exp):
		self.exp = self.exp + exp
		self.check_can_level()

	def get_weapon_stats(self):
		if self.weapon:
			self.weapon.print_weapon_stats()

	def get_needed_stats(self):
		return self.strength, self.dexterity, self.intelligence, self.health, self.mana, random.random()

	def print_stats(self):
		print(self.name)
		print("Max Health: " + str(self.maxhealth) + " Current Health: " + str(self.health))
		print("Max Mana: " + str(self.maxmana) + " Current Mana:  "+ str(self.mana))
		print("Level: " + str(self.level) + " Strength: " + str(self.strength) + " Int: " + str(self.intelligence) + " Dex: " + str(self.dexterity) + '\n')
		self.get_weapon_stats()

	def print_health(self):
		print(self.name + ':' + str(self.health) + '/' + str(self.maxhealth))

	def calculate_dodge(self):
		r = random.randint(0, self.maxstat)
		if r <= self.dexterity:
			return False
		return True

	def calculate_mitigated_damage(self):
		return 1 - (self.strength * random.random() / self.maxstat)

	def lose_health(self, loss):
		damage = loss * self.calculate_mitigated_damage()
		mitigation = loss - damage
		new_health =  float(self.health) -  damage
		if self.calculate_dodge():
			print('%s mitigated %f damage!' %(self.name, mitigation))
			self.health = new_health
			return False
		print('%s dodged the attack!' %(self.name))

	def calculate_base_damage(self):
		s, i, d, h, m, r = self.get_needed_stats()
		damage = self.weapon.get_damage_formula()(s, i, d, h, m, r)
		# print(damage)
		return damage

	def calculate_combat_art_damage(self, ca):
		attack = self.combat_arts[ca]
		mana_cost = attack[0]
		if mana_cost <= self.mana:
			self.mana = self.mana - mana_cost
		else:
			print('You didnt have enough mana for that!')
			return 0
		damage = attack[1](self.strength, self.dexterity, self.intelligence, self.health, self.mana, random.random())
		print('%s used %s!' %(self.name, ca))
		return damage

	def is_dead(self):
		return self.health <= 0

	def heal(self, healing):
		self.health = self.health + healing
		if self.health > self.maxhealth:
			self.health = self.maxhealth
	def full_heal(self):
		self.health = self.maxhealth

def slap_combat(player1, player2):
	while not player1.is_dead() and not player2.is_dead():
		player2.lose_health(player1.calculate_base_damage())
		player1.lose_health(player2.calculate_base_damage())
		player1.print_health()
		player2.print_health()

def main():
	#cur_map = mapmodule.MapModule(5)
	#cur_map.print_map()
	print("Time to start the game!")
	name = input("What is your name?")
	chartype = int(input("What character type are you? (1 only)"))
	yourcharacter = PlayerCharacter(name, chartype, 1)
	yourcharacter.print_stats()
	yourcharacter.add_exp(800)
	yourcharacter.print_stats()
	game_player = mapmodule.GamePlayer(5, yourcharacter)
	game_player.walk_map()
	game_player.print_map()
	name_generator = randomgenerator.RandomAssetGenerator('basic_name', 3)
	enemycharacter = PlayerCharacter(name_generator.generate_random_title(), 1, 3)
	# slap_combat(yourcharacter, enemycharacter)
	fight_module = basicfight.BasicCombatModule(yourcharacter, enemycharacter)
	fight_module.fight()


 

if __name__ == '__main__':
	main()