import random
from enum import Enum
import basicfight
import player_character
import randomgenerator
class Tiles(Enum):
	PLAINS=0
	LAKE=1
	FOREST=2
	VILLAGE=3
	CAVE=4

class MapModule(object):
	def __init__(self, len):
		self.len = len
		self.map = self.generate_map(self.len)
		self.tile_rep = \
		{Tiles.PLAINS: '#'
		,Tiles.LAKE: 'O'
		,Tiles.FOREST: '!'
		,Tiles.VILLAGE: 'T'
		,Tiles.CAVE: '?'}

	def generate_map(self, len):
		a_map = []
		for i in range(0, len):
			sub_map = []
			for i in range(0, len):
				randomtile = random.choice(list(Tiles))
				sub_map.append(randomtile)
			a_map.append(sub_map)
		return a_map

	def get_tile(self, tile):
		return self.tile_rep[tile]


	def print_map(self):
		for sub in self.map:
			print_format = []
			for tile in sub:
				print_format.append(self.get_tile(tile))
			print(''.join(print_format))

	def print_map_player(self, player_loc):
		sub = self.map[0]
		print(player_loc)
		#print(sub)
		for j in range(0, self.len):
			print_format = []
			tile = self.map[j]
			for k in range(0, self.len):
				rep = tile[k]
				# print((j, k))
				if (j, k) == player_loc:
					#print('HIT')
					print_format.append('+')
				else:
					print_format.append(self.get_tile(rep))

			print(''.join(print_format))

	def at_position(self, player_loc):
		pos = self.map[player_loc[0]][player_loc[1]]
		return pos


class Direction(Enum):
	UP=0
	RIGHT=1
	DOWN=2
	LEFT=3

class GamePlayer(object):
	def __init__(self, map_size, player):
		self.map_size = map_size
		self.player = player
		self.map = MapModule(self.map_size)
		self.player_loc = (random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1))
		random_quest_gen = randomgenerator.RandomAssetGenerator('quest_name', 3)
		dest_loc = (random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1))
		self.quest = random_quest_gen.generate_random_quest(self.player.level, dest_loc)
		# self.map.print_map_player(self.player_loc)

	def move_player(self, direction):
		if direction == Direction.LEFT:
			self.player_loc = (self.player_loc[0], self.player_loc[1] - 1)
		elif direction == Direction.DOWN:
			self.player_loc = (self.player_loc[0] + 1, self.player_loc[1])
		elif direction == Direction.RIGHT:
			self.player_loc = (self.player_loc[0], self.player_loc[1] + 1)
		else:
			self.player_loc = (self.player_loc[0] - 1, self.player_loc[1])

	def take_player_movement(self):
		self.print_map()
		while True:
			try:
				choice = int(input('U=0, R=1, D=2, L=3'))
				for direction in list(Direction):
					# print(direction.value)
					# print(direction.value == choice)
					if direction.value == choice:
						self.move_player(direction)
						break
				return 
			except Exception:
				continue

	def evaluate_quest_completion(self):
		quest_complete = self.quest.check_quest_completion(self.player_loc)
		if quest_complete:
			self.quest = quest_complete[1]
			self.offer_loot(1, quest_complete[0])

	def offer_loot(self, offer, s_weapon=None):
		random_gen = randomgenerator.RandomAssetGenerator('weapon', 3)
		random_weapons = []
		self.player.print_stats()
		print('Choose a new weapon!')
		if s_weapon:
			random_weapons.append(s_weapon)
		else:
			for i in range(0, offer):
					_r = random_gen.generate_random_weapon(self.player.level)
					random_weapons.append(_r)
		for i in range(0, len(random_weapons)):
			print('----Weapon %d ----' % i)
			_w = random_weapons[i]
			_w.print_weapon_stats()

		while True:
			try:
				choice = int(input('Choose a new weapon, or stay with your weapon by pressing %d' % offer))
				break
			except Exception:
				print('Invalid Choice!')
				continue

		if choice == offer:
			return
		new_weapon = random_weapons[choice]
		self.player.unequip_weapon()
		self.player.equip_weapon(new_weapon)
		self.player.print_stats()


	def evaluate_landing_position(self):
		biome = self.map.at_position(self.player_loc)
		if biome == Tiles.CAVE:
			print('Random Fight!')
			level_fight = random.randint(1, self.player.level)
			enemy = player_character.PlayerCharacter(None, 1, level_fight)
			fight_module = basicfight.BasicCombatModule(self.player, enemy)
			fight_module.fight()

		if biome == Tiles.VILLAGE:
			offer = 3
			self.offer_loot(3)

		if biome == Tiles.LAKE:
			self.lake_module()
		self.evaluate_quest_completion()

	def lake_module(self):
		print('A very dangerous enemy approaches!')
		random_gen_monster = randomgenerator.RandomAssetGenerator('boss_name', 3)
		random_boss_name = random_gen_monster.generate_boss_name()
		level_fight = random.randint(self.player.level, self.player.level * 2)
		boss = player_character.PlayerCharacter(random_boss_name, 1, level_fight)
		fight_module = basicfight.BasicCombatModule(self.player, boss)
		outcome = fight_module.fight()
		if outcome:
			loot = boss.weapon
			self.offer_loot(1, loot)




	def walk_map(self):
		while True:
			self.take_player_movement()
			self.evaluate_landing_position()
			print(self.map.at_position(self.player_loc))
			# print(self.map.get_tile(self.map.at_position(self.player_loc)))
	def print_map(self):
		self.map.print_map_player(self.player_loc)
		if self.quest:
			self.quest.print_quest()

