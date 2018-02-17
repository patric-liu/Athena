import numpy as np
import race
import matplotlib.pyplot as plt
import all_parameters
para = all_parameters.Parameters()


''' Uses Evolutionary Models to improve network

Creates multiple versions ('clones') of original network with slight 
pertubations ('mutations') to the parameters, runs them through a race 
simulation, and creates a new network ('child') using a weighted 
average of each clone based on its performance ('fitness')

Child then becomes the original network and this is looped over 'generations'

'''

class Evolution(object):

	def __init__(self, parameters):
		# import network from trainer
		self.parameters = parameters
		self.sizes = self.parameters[2]
		self.biases = self.parameters[0]
		self.weights = self.parameters[1]

	def evolve(self, population_size = para.population_size, 
					mutation_rate = para.mutation_rate, 
					selection_bias = para.selection_bias , 
					inheritance_rate = para.inheritance_rate, 
                	generations = para.generations):
		''' Evolve
		Main training method, taking original network (self.parameters) and 
		replaces it with an evolved one
		
		population_size: number of clones to make/evaluate each generation
		mutation_rate: amount by which the clones vary from the parent
		selection_bias: how strongly the weights favor better performance
		inheritance_rate: amount by which the child varies from the parent
		generations: number of generations to evolve over

		'''
		for generation in range(generations):
			print()
			print("generation", generation + 1)

			# creates clones of original network
			self.clone_parent(population_size, mutation_rate)
			# runs clones through the simulatin to determine fitness
			self.determine_fitness(population_size)
			if self.abort_evolution:
				print("reinitialize network")
				break
			# creates child network using clones based on fitness
			self.reproduce(selection_bias, inheritance_rate, population_size, generation)

	def clone_parent(self, population_size, mutation_rate):
		''' Clone Parent
		Creates clones of parent network each with slight mutations
		Mutations are slight adjustments, positive or negative, made 
		to the weights and biases of the parent network

		population_size: number of clones to create
		mutation_rate: standard deviation of mutations

		'''
		self.mutations = [] 
		self.clones = []
		for n in range(population_size):
			# randomly generate mutations
			bias_mutation  = [np.random.randn(y, 1) for y in self.sizes[1:]]
			weight_mutation = [np.random.randn(y, x)/np.sqrt(x) 
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]
			mutation = [bias_mutation, weight_mutation]
			self.mutations.append(mutation)

			# apply mutations to parent network to create clones
			clone_biases = [x * mutation_rate + y for x,y 
						in zip(bias_mutation, self.biases)]
			clone_weights = [x * mutation_rate + y for x,y 
						in zip(weight_mutation, self.weights)]
			clone_parameters = [clone_biases, clone_weights, self.sizes]
			self.clones.append(clone_parameters)

	def determine_fitness(self, population_size):
		''' Determine Fitness
		Returns a fitness value for each clone by determining performance in 
		simulation. Fitness is evaluated primarily based on race performance 
		(time, distance), but undesireable behaviors such as letting the battery 
		voltage stay too low will be punished with a decrease in fitness value.
		'''

		self.environment = para.environment # **temporary replacement for environment**
		self.performances = []
		self.distances = []

		# runs each clone through simulation to determine its fitness
		for n in range(population_size): 
			# export clone's network parameters and environment to set up a race
			competition = race.Race(self.clones[n], self.environment)
			# runs through a race allowing clone network to determine strategy
			competition.race()
			# aborts evolution proccess if a fatal error occurs
			self.abort_evolution = competition.abort
			# evaluate performance
			performance = competition.argo.position ** 2 / competition.argo.race_time / para.environment[0]

			self.performances.append(performance)

		print('average performance: ', np.sum(self.performances)/population_size)

	def reproduce(self, selection_bias, inheritance_rate, population_size, generation):
			''' Reproduce - creates a child network based on clone performance
			A new mutation equal to the weighted average of ckone mutations 
			is applied to the original network. Weights are proportional 
			to (clone performance[i] - average clone performance)^selection_bias
			Inheritance rate scales how big the new mutation is. 
			'''

			# Create list of weights
			mean_performance = np.sum(self.performances)/population_size
			weights = [(((performance-mean_performance))/mean_performance)**selection_bias * inheritance_rate
					 for performance in self.performances]

			# Initialize child network
			child_net = self.parameters[:]
			# Loop through the numpy arrays that make up the parameters
			for parameter_type in [0,1]: # No 2 index to preserve self.sizes
				for index in range(len(self.sizes)-1):

					# Initialize np array from 1st clone **required to sum**
					parameter_deltas = (self.mutations[0][parameter_type][index]
									 	* weights[0] * inheritance_rate)

					# Add weighted np arrays from rest of clones,		
					for clone in range(1, population_size):
						parameter_deltas = (parameter_deltas + 
								self.mutations[clone][parameter_type][index] * 
								weights[clone] * 
								inheritance_rate)
					
					# Normalize by population size and update child_net
					parameter_deltas = parameter_deltas / float(population_size)
					child_net[parameter_type][index] = (child_net[parameter_type]\
													[index] + parameter_deltas)



			# Determine and display performance of child network
			competition = race.Race(child_net, self.environment)
			if generation % 10 == True:
				competition.race(True)
				print("show graph")
				plt.figure(1)
				np_battery_tracker = np.array(competition.battery_tracker)/para.battery_max_charge
				plt.plot(np_battery_tracker) #np.divide(np.array(competition.battery_tracker, dtype=int), para.battery_max_charge)
				plt.subplot(311)
				plt.plot(competition.distance_tracker)
				plt.subplot(312)
				plt.plot(competition.velocity_tracker)
				plt.subplot(313)
				plt.savefig("graphs.png")
			else:
				competition.race()
			print('new gen: ', competition.argo.position **
			      2 / competition.argo.race_time / para.environment[0])

			#plt.plot(competition.battery_tracker)