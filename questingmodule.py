import randomgenerator
class Quest(object):
	def __init__(self, child, destination, reward, name=None):
		self.child = child
		self.name = name
		if not name:
			random_quest_gen = randomgenerator.RandomAssetGenerator('quest_name', 3)
			self.name = random_quest_gen.generate_quest_name()
		self.destination = destination
		self.reward = reward

	def check_destination(self, dest):
		return destination == dest

	def set_child(self, child):
		self.child = child

	def get_child(self):
		return self.child

	def check_quest_completion(self, destination):
		if self.check_destination(destination):
			print('You have completed %s!' % self.name)
			return (self.reward, self.child)



