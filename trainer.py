import network_self
import numpy as np
import evolve
import time
import all_parameters
para = all_parameters.Parameters()

start_time = time.time()

# specify desired network shape
net_sizes = para.sizes

# initialize new random network/ option to import existing should be added
Athena = network_self.Network(net_sizes)

# exports network to evolution class
Train = evolve.Evolution(parameters = Athena.parameters)

# executes evolutionary model algorithm
Train.evolve()

print( 'time taken:', round(time.time() - start_time, 2))
asdfadsfasf
asdfadsf

