import network_self
import numpy as np
import evolve
import time
import all_parameters
para = all_parameters.Parameters()

start_time = time.time()

# specify data input size, should be automated later using evolve method
input_size = 4

# specify desired network shape
net_shape = [input_size, 10, 1]

# initialize new random network/ option to import existing should be added
Athena = network_self.Network(net_shape)

# exports network to evolution class
Train = evolve.Evolution(parameters = Athena.parameters)

# executes evolutionary model algorithm
Train.evolve(population_size = 20, 
			mutation_rate = 0.1, 
			selection_bias = 1, 
			inheritance_rate = 1,
			generations = 1000)

print('time taken:', round(time.time() - start_time, 2))