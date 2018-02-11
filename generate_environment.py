''' Generate Environment creates an environment through which the car navigates.
An environment consists of weather and road geometry. Road geometry is mostly 
described with road inclination, though a more detailed description will include
road bearing and traffic congestion. Weather consists of cloud cover, 
temperature and wind. 

Generated maps should be of variable length, with lengths distributed between 
0 and (real) race length (~3000km), in order to recreate scenarios that our team
will encounter. Maps need to be generated such that when given any time/distance 
traveled, the environment can be returned for the next time step. 

'''