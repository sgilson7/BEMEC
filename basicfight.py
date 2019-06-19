import random
from enum import Enum
class Turn(Enum):
	PLAYER = 0
	ENEMY = 1

class AttackType(Enum):
	BASIC = 1
	COMBATART = 2
	DEFEND = 3
class BasicCombatModule(object):
	def __init__(self, player1, player2):
		self.player = player1
		self.enemy = player2
		self.turns = {Turn.PLAYER : Turn.ENEMY, Turn.ENEMY : Turn.PLAYER}

	def next_turn(self, cur_turn):
		return self.turns[cur_turn]

	def player_print_options(self):
		while True:
			print('%s HP: %.3f MP: %.3f' % (self.player.name, self.player.health, self.player.mana))
			print('1: Basic Attack')
			print('2: Combat Art')
			print('3: Defend')
			try:
				option = int(input('Choose your action!\n'))
				return option
			except Exception:
				print('Invalid input!')
	def calculate_first_attack(self):
		if self.player.dexterity > self.enemy.dexterity:
			return Turn.PLAYER
		else:
			return Turn.ENEMY

	def player_perform_action(self, choice):
		if choice == AttackType.BASIC.value:
			damage = self.player.calculate_base_damage()
			print('%s did %.3f damage to %s!' %(self.player.name, damage, self.enemy.name))
			self.enemy.lose_health(damage)
		elif choice == AttackType.COMBATART.value:
			while True:
				self.player.print_combat_arts()
				try:
					chosen_ca = input('Type the name of the Combat Art you wish to use, leave to skip.\n')
					if chosen_ca == 'skip':
						return
					damage = self.player.calculate_combat_art_damage(chosen_ca)
					print('%s did %.3f damage!' %(self.player.name, damage))
					self.enemy.lose_health(damage)
					return 
				except Exception:
					print('Invalid Input!')
					continue


	def fight(self):
		print('%s is fighting %s!\n' %(self.player.name, self.enemy.name))
		self.enemy.print_stats()
		turn = self.calculate_first_attack()
		while not self.player.is_dead() and not self.enemy.is_dead():
			if turn == Turn.PLAYER:
				choice = self.player_print_options()
				self.player_perform_action(choice)

			if turn == Turn.ENEMY:
				print('%s HP: %.3f' % (self.enemy.name, self.enemy.health))
				# print('Str: %d, Dex: %d, Int: %d' %(self.enemy.strength, self.enemy.dexterity, self.enemy.intelligence))
				damage_inflicted = self.enemy.calculate_base_damage()
				print('%s dealt %.3f damage' %(self.enemy.name, damage_inflicted))
				self.player.lose_health(damage_inflicted)
			turn = self.next_turn(turn)
		if self.player.is_dead():
			print("You have died!")
			self.player.full_heal()
		elif self.enemy.is_dead():
			exp_gain = self.enemy.reward
			print("You have gained %.3f exp!" % exp_gain)
			self.player.add_exp(exp_gain)



		