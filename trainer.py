''' Trainer

Randomly Initializes and then trains Athena from scratch using evolutionary
strategies

Future Functionality:
Pretrain Athena using gradient descent and hand-curated input-output pairs
before running through evolution. Saving pretrained networks and then importing
them should save on initial training time. This runs the risk of not fully 
exploring the parameter space and getting stuck at the same local minimums
'''

import network_self
import numpy as np
import evolve
import time
import all_parameters
para = all_parameters.Parameters()

# keep track of computation time
start_time = time.time()

# initialize new random network/ option to import existing should be added
Athena = network_self.Network(para.sizes)

# exports network to evolution class
Train = evolve.Evolution(parameters = Athena.parameters)

# executes evolutionary model algorithm
Train.evolve()

print( 'time taken:', round(time.time() - start_time, 2))
