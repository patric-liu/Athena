import network_self
import numpy as np


network = network_self.Network([4,5,1])

_input = np.zeros([4,1])

_input[0] = 100
_input[1] = 100
_input[2] = 100
_input[3] = 100

output = network.feedforward_minus_last(_input)

print(output)

_input[0] = -100
_input[1] = -100
_input[2] = -100
_input[3] = -100

output = network.feedforward_minus_last(_input)

print(output)
