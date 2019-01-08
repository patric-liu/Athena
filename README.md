# Athena

Athena is a neural network that determines race strategy for week-long, 3000 km solar vehicle races. It's trained in simulation using evolutionary methods and validated in real physical testing. Once trained, Athena can run during the race and respond to changing weather conditions and unexpected deviations from the proposed strategy.

Athena is composed of two components, the long-term optimizer and the short-term optimizer. The long term optimizer does a low resolution search (brute force and guided) over future travel speeds and finds optima. It takes into account sun exposure, weather forecast, and even road gradient, and has an interal model of the vehicle dynamics. The short term optmizer is a neural network which looks at local conditions - such as the locally measured wind, irradiance and gradient of road - and makes adjustments to velocity proposed by the long term optimizer. Since it is not possible to backpropogate through the simulation of the car dynamics, the short term optmizer is optimized evolutionarily. Unlike the long term optimizer, this can be done and validated prior to the race. 

The evolutionary method used works by creating multiple slightly pertubed versions of the short term optimizer, and allows them to determine strategy for a simulated race. At the end of the simulations, optimizer parameters are updated based on the performance of each version. This is then repeated, along with real unsimulated testing, until Athena suprasses our team member's abilities to make strategic decisions. This evolutionary approach relies on accurate yet efficient simulations of relevant physical systems, dynamics randomization, generated race maps, and reading of real weather data.

** The 'Athena Flow Chart' image shows the flow chart for how strategy planning is carried out by the program in more visual detail. 

Since our optimizers also provide a predicted state, we can compare the real state of the vehicle to the predicted/simulated state of the vehicle. An ambitious goal is to update the car dynamics based on the error in our prediction, which could(?) be done with an Extended Kalman Filter. 

## Docs


* ```trainer.py``` - Training interface that allows you to specify training hyperparameters

* ```evolve.py``` - Implements the evolution algorithm

* ```race.py``` - Runs athena through a simulation

* ```car.py``` - Contains functions which model the physical behavior of the car

* ```network_self.py``` - Contains neural network functionality

### future functionality

* ```generate_environment.py``` - Generates a random race map 

* ```read_weather_data.py``` - Reads live NOAA data

* ```interpret_weather.py``` - Applies 1-d convolution and pooling to high-dimensional weather and map data to extract lower dimensional features to input to the neural network

* ```run_Athena``` -  runs Athena, pulling data from live telemetry feed, weather forecasts and if needed, human input

* ```Athenas/``` - Holds all saved versions of Athena


## Aside




Solar vehicle racing is at its core, a challenge of vehicle energy efficiency and energy management. When building a solar vehicle, vast amounts of time are rightfully spent on design, manufacturing, and testing for reliability - the building of the car. However once at the race, much of this effort can be quickly negated if race strategy is conducted poorly. Hopefully, Athena can support my team during the race and allow the vehicle that everyone spent so long desinging and building to perform to the best of its ability. 
