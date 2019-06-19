
class Weapon(object):
	def __init__(self, name, damage_formula, d_f_readable, level_req, stat_buff):
		self.name = name
		self.damage_formula = damage_formula
		self.damage_formula_readable = d_f_readable
		self.level_req = level_req
		self.stat_buff = stat_buff
		self.equipped = False

	def get_damage_formula(self):
		return self.damage_formula

	def print_weapon_stats(self):
		print('Weapon Name: %s Level: %d' %(self.name, self.level_req))
		print('Damage Formula: %s' % self.damage_formula_readable)
		print('+%d str +%d dex +%d int' % (self.stat_buff[0], self.stat_buff[1], self.stat_buff[2]))

	def equip(self):
		if self.equipped:
			print('This weapon is already equipped!')
			return (0, 0, 0)
		self.equipped = True
		return self.stat_buff

	def unequip(self):
		if not self.equipped:
			print('This weapon is not equipped to anyone!')
			return (0, 0, 0)
		self.equipped = False
		return (-1 * self.stat_buff[0], -1 * self.stat_buff[1], -1 * self.stat_buff[2])
