import network_self
import numpy as np

print("**************************************************")

network = network_self.Network([5,6,1])

_input = np.zeros([5,1])

_input[0] = ((3000000./1e6)**-1)/10
_input[1] = 0
_input[2] = 0
_input[3] = 5
_input[4] = 1

output = network.feedforward(_input)

print(output, '1')

'''
distance_from_finish = 2998000.

_input[0] = ((distance_from_finish/1e6)**-1)/10
_input[1] = 0.0001
_input[2] = 1./3600.
_input[3] = distance_from_finish
_input[4] = 1

output2 = network.feedforward(_input)

print(output2, '2')

distance_from_finish = 1000

_input[0] = ((distance_from_finish/1e6)**-1)/10
_input[1] = 0.9
_input[2] = 14
_input[3] = distance_from_finish
_input[4] = 1

output3 = network.feedforward(_input)

print(output3, '3')
'''
