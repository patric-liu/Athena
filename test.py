import evolve
import numpy as np
import network_self

#np.random.seed(40)


input_size = 4

net_shape = [input_size, 6, 1]
strategy = network_self.Network(net_shape)

x = np.zeros( (input_size,1) )

#y = strategy.feedforward_minus_last(x)

evolve = evolve.Evolution(strategy.sizes, strategy.biases, strategy.weights)

evolve.evolve(10, 0.01, 1, 1)
