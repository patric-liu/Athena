'''import network_self
import numpy as np


network = network_self.Network([5,100,1])

_input = np.zeros([5,1])

_input[0] = ((3000000./1e6)**-1)/10
_input[1] = 0
_input[2] = 0
_input[3] = 3000000
_input[4] = 1

output = network.feedforward_minus_last(_input)

print(output)

distance_from_finish = 2998000.

_input[0] = ((distance_from_finish/1e6)**-1)/10
_input[1] = 0.0001
_input[2] = 1./3600.
_input[3] = distance_from_finish
_input[4] = 1

output2 = network.feedforward_minus_last(_input)

print(output2)

distance_from_finish = 1000

_input[0] = ((distance_from_finish/1e6)**-1)/10
_input[1] = 0.9
_input[2] = 14
_input[3] = distance_from_finish
_input[4] = 1

output3 = network.feedforward_minus_last(_input)

print(output3)
'''

import numpy as np
import math
from math import cos
from math import pi

print(123%5)