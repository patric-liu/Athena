import network_self
import car
import numpy as np

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
		self.initialize_car()
		self.set_car_constants()

		self.abort = False
		max_race_time = self.environment[0] / 20 # time in seconds taken to finish race at n m/s

		while True:
			self.get_nn_inputs()
			velocity = self.mutated_network.feedforward_minus_last(self.inputs)
			self.argo.update_state(velocity)

			if self.inputs[3] < 0:		
				break 

			if self.argo.race_time > max_race_time:
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

		input_size = 4 #number of input neurons

		# input must be an np.array of shape (input_size, 1)
		self.inputs = np.zeros( (input_size,1) )
		self.inputs[0] = float(inverse_distance_to_finish)
		self.inputs[1] = battery_charge
		self.inputs[2] = time_hour
		self.inputs[3] = float(distance_from_finish)

	def initialize_car(self):
		# Starting racing conditions of the car
		self.argo = car.Argo(
			starting_position =0, 
			starting_time = 0, 
			starting_charge = 1.6e7, 
			panel_temperature = 25,
			time_step = 600, 
			clock_time = 0, 
			cell_voltage = 3.5
			)

	def set_car_constants(self):
		# Properties of the car
		self.argo.set_constants(
			mass = 240,
			E_regen = 0.8, 
			max_charge = 1.6e7, 
			Cd = 0.12, 
			Crr = 0.03,
			Frontal_Area = 1, 
			solar_hour = -4, 
			panel_area = 6 , 
			basecell_efficiency = 0.16,
			battery_inefficiency = 0.00005
			)
