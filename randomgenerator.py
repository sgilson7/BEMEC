import random
import os 
import weapon

class RandomAssetGenerator(object):
	def __init__(self, type_a, num_descriptors):
		self.type = type_a
		self.num_descriptors = num_descriptors
		self.adjectives = self.adjective_pool()
		self.names = self.name_pool()
		self.weapons = self.weapon_pool()
		self.verbs = self.verb_pool()
		self.nouns = self.noun_pool()
		# print(self.weapons)
		self.namingschemes = \
		{'basic_name': lambda n, a: '%s the %s' %(n, a)
		,'weapon' : lambda w, a: '%s %s' %(a, w)
		,'boss_name': lambda n, a, no: '%s, %s %s' % (n, a, no)}



		self.weapon_l_dict = \
		{'BasicWand' : (lambda s, d, i, h, m, r: i, 'i')
		,'BasicAxe': (lambda s, d, i, h, m, r: s, 's')
		,'BasicDagger': (lambda s, d, i, h, m, r: d, 'd')
		,'BasicMace': (lambda s, d, i, h, m, r: 2*s - i, '2s - i')
		,'BasicBow': (lambda s, d, i, h, m, r: 2*d - i, '2d - i')
		,'BasicStaff': (lambda s, d, i, h, m, r: 2*i - s, '2i - s')}

	def adjective_pool(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		# print(dir_path)
		infh = open('adjectives/28K_adjectives.txt', 'r')
		data = infh.read().splitlines()
		return data

	def name_pool(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		# print(dir_path)
		infh = open('adjectives/fantasy_name.txt', 'r')
		data = infh.read().splitlines()
		return data

	def weapon_pool(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		infh = open('adjectives/weapon_types.txt', 'r')
		data = infh.read().splitlines()
		return data

	def verb_pool(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		infh = open('verbs/4syllableverbs.txt', 'r')
		data = infh.read().splitlines()
		return data

	def noun_pool(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		infh = open('nouns/4syllablenouns.txt', 'r')
		data = infh.read().splitlines()
		return data



	def get_random_attr(self, particle_list):
		# print(len(particle_list))
		r_spot = random.randint(0, len(particle_list) - 1)
		# print(r_spot)
		if particle_list[r_spot] == '':
			return self.get_random_attr(particle_list)
		return particle_list[r_spot]


	def generate_random_title(self):
		return self.namingschemes[self.type](self.get_random_attr(self.names), self.get_random_attr(self.adjectives))

	def generate_weapon_name(self):
		return self.namingschemes[self.type](self.get_random_attr(self.weapons), self.get_random_attr(self.adjectives))

	def generate_boss_name(self):
		return self.namingschemes[self.type](self.get_random_attr(self.names), self.get_random_attr(self.adjectives), self.get_random_attr(self.nouns))

	def generate_random_weapon(self, level):
		d_f, d_f_readable = self.weapon_l_dict[random.choice(list(self.weapon_l_dict.keys()))]
		#print(d_f_readable)
		if level == 0:
			level = 1
		level_req = random.randint(level - 1, level + 1)
		pool = level
		s_buff = random.randint(0, pool)
		pool = level - s_buff
		d_buff = random.randint(0, pool)
		pool = pool - d_buff
		i_buff = random.randint(0, pool)
		stat_buff = (s_buff, d_buff, i_buff)
		random_weapon = weapon.Weapon(self.generate_weapon_name(),  d_f, d_f_readable,  level_req, stat_buff)
		return random_weapon


if __name__ == '__main__':
	name_creator = RandomAssetGenerator('basic_name', 3)

	random_name = name_creator.generate_random_title()

	print(random_name)
