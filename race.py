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

	def race(self, track_performance = False):
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

		self.distance_tracker = []

		while True:
			self.get_nn_inputs()

			if track_performance:
				self.distance_tracker.append(self.argo.position)

			velocity = self.mutated_network.feedforward_minus_last(self.inputs)
			# velocity = 30/3.6 # m/s TEMPORARY TESTING
			
			# decreases speed if battery power is low
			decrease_factor = (1 + np.exp( -120 * (self.inputs[1] - 0.03) ))
			noise_factor = np.random.normal(1, para.velocity_noise)
			self.argo.update_state(velocity * noise_factor)

			#print()
			#print('********************************************')
			#print(velocity, 'm/s')
			#print(self.argo.position, 'meters progress')
			#print(self.argo.race_time, 'seconds into race')
			#print(self.argo.solar_hour + 12., 'military hour')
			#print(self.argo.battery_charge, 'joules charge')
			#print()
			#print(self.argo.sensor_solar_p, 'watts from array')
			#print(self.argo.sensor_battery_dCharge, 'change in battery charge')
			#print(self.argo.sensor_motion_p_loss, 'kinetic energy loss')
			#print(self.argo.sensor_batteryheatlosspower, 'energy value for heat loss')
			#print(self.argo.sensor_battery_heat_loss, 'heat loss in batteries')
			#print()
			#print(self.argo.sensor_avg_battery_current, 'current draw')

			if self.inputs[1] < 0: #battery
				break

			if self.inputs[3] < 0: #distance
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
		time_hour = self.argo.solar_hour/6

		input_size = 5 #para.input_size #number of input neurons

		# input must be an np.array of shape (input_size, 1)
		self.inputs = np.zeros( (input_size,1) )
		self.inputs[0] = float(inverse_distance_to_finish)
		self.inputs[1] = battery_charge
		self.inputs[2] = time_hour
		self.inputs[3] = float(distance_from_finish)
		self.inputs[4] = float(random.uniform(-2,2))
