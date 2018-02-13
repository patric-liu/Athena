import network_self
import car
import numpy as np
import random
import all_parameters
para = all_parameters.Parameters()


class Race(object):

	def __init__(self, parameters, environment):
		# Imports network and environment from evolve
		self.biases = parameters[0]
		self.weights = parameters[1]
		self.sizes = parameters[2]
		self.environment = environment
		# Performance metrics
		self.performance = 0

	def race(self):
		''' Race simulates a race given a certain set of conditions: network(policy),
		car constants(metrics), and environment
		'''
		# Initializes a network self.mutated_network with the imported parameters
		self.mutated_network_initializer()
		
		# Initializes vehicle, including its position and time
		self.argo = car.Argo()
		self.argo.set_constants()

		self.abort = False
		max_race_time = self.environment[0] / 20 # time in seconds taken to finish race at n m/s

		while True:
			self.get_nn_inputs()
			velocity = self.mutated_network.feedforward_minus_last(self.inputs)
			self.argo.update_state(velocity)

			print()
			print('********************************************')
			print(velocity, 'm/s')
			print(self.argo.position, 'meters')
			print(self.argo.race_time, 'seconds')
			print(self.argo.clock_time + 12., 'military hour')
			print(self.argo.battery_charge, 'joules in battery')
			print(self.argo.irradiance, 'watts into array')

			if self.inputs[3] < 0:		
				break 

			if self.argo.race_time > para.max_race_time:
				break

	def mutated_network_initializer(self):
		# exports network parameters to network_self class
		self.mutated_network = network_self.Network( self.sizes )
		self.mutated_network.biases = self.biases
		self.mutated_network.weights = self.weights

	def get_nn_inputs(self):
		''' Produce a vector of inputs to neural network

		Data is changed to better fit between 0-1 for better nn input
		'''

		# distance from finish line information
		distance_from_finish = ((self.environment[0]-self.argo.position))
		inverse_distance_to_finish = ((self.environment[0]-self.argo.position/1e6)**-1)/10

		# battery state as a percentage
		battery_charge = self.argo.battery_charge/self.argo.max_charge
		
		# time of day - hours from solar hour (noon)
		time_hour = self.argo.clock_time/6

		input_size = 5 #para.input_size #number of input neurons

		# input must be an np.array of shape (input_size, 1)
		self.inputs = np.zeros( (input_size,1) )
		self.inputs[0] = float(inverse_distance_to_finish)
		self.inputs[1] = battery_charge
		self.inputs[2] = time_hour
		self.inputs[3] = float(distance_from_finish)
		self.inputs[4] = float(random.uniform(-2,2))