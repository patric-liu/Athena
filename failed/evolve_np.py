import numpy as np
import race


class Evolution(object):

	def __init__(self, net_sizes, net_biases, net_weights):
		# import network
		self.sizes = net_sizes #list of sizes
		self.biases = net_biases
		self.weights = net_weights
		self.parameters = [self.biases, self.weights, self.sizes]

	def evolve(self, population_size, mutation_rate, selection_bias, inheritance_rate, generations):
		# Returns slightly improved network
		
		for generation in range(generations):
			'''Create multiple random versions of network'''
			self.clone_parent(population_size, mutation_rate)
			'''	Keep track of their differences from original
	
			run each through the same training map
				input network, return total time'''
			#self.determine_fitness(population_size)
			'''Find the difference between time and mean_time for all networks
				raise the difference to the power of 1+selection_bias'''
			#self.reproduce(selection_bias, inheritance_rate, population_size)
			'''Multiply deltas by time_difference^(1+selection_bias) to create new network'''
			#self.reproduce(selection_bias, inheritance_rate, population_size)

	def clone_parent(self, population_size, mutation_rate):
		# prepare list of deltas and population parameters
		self.mutations = []
		self.clones = []
		for n in range(population_size):
			# randomly generate mutations

			bias_mutation = np.array([])
			for y in self.sizes[1:]:
				np.append(bias_mutation, np.random.randn(y, 1) * mutation_rate)
			weight_mutation = np.array([])
			for x, y in zip(self.sizes[:-1],self.sizes[1:]):
				np.append(weight_mutation, np.random.randn(y, x) * mutation_rate)
			print(weight_mutation)
			

	def determine_fitness(self, population_size):
		self.times = []
		self.distances = []

		self.environment = [100000]
		for n in range(population_size):
			parameters = self.clones[n]
			competition = race.Race(parameters, self.environment)
			competition.race()
			self.distances.append(competition.car.position/1000)
			self.times = self.distances
		print()
		print(self.distances)
		print('generation average distance: ', np.sum(self.distances)/population_size)

	def reproduce(self, selection_bias, inheritance_rate, population_size):
			# return relative performance

			mean_speed = np.sum(self.times)/population_size
			weights = [(time-mean_speed)**selection_bias * inheritance_rate
					 for time in self.times]

			print(type(self.clones[0]))
			self.new_parameters = self.clones[0]
			print(type(self.new_parameters))
			for n in range(population_size-1):
				self.new_parameters += self.clones[n]
				print(type(self.new_parameters), "asdfasldkjf;lasfksadf;laslkadflj")

			print(self.new_parameters)
			#self.new_parameters = np.divide(self.new_parameters, float(population_size))

			#a = self.new_parameters/2
						#print(self.new_parameters[clone_index][parameter_type][layer_index])
			#	new_biases_deltas.append([weight * x for x in clone[0]])
			#	new_weights_deltas.append([weight * x for x in clone[1]])
			# new parameters formed by adding the weighted 
			# sum of mutations to parent network

			#competition = race.Race(self.new_parameters, self.environment)
			#competition.race()
			#print('new gen: ', competition.car.position/1000)

