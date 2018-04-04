## motivations - the function

Solar vehicle racing fundamentally a challenge of energy efficiency and management. When building a solar vehicle, vast amounts of time are rightfully spent on design, manufacturing, and testing - the critical steps for building a reliable, legal, and efficient car. Once at the race, however, the benefits of these efforts are at the peril of a team’s race strategy. Poorly conducted race strategy has the potential to be just as detrimental a flat tire. If successful, Athena will provide this much needed support and allow the vehicle that everyone spends so long designing and building to perform to the best of its ability. 

Race strategy consists of making decisions that depend on information you have, most of which are physical variables of the environment (e.g. battery state, time of day, predicted weather). While decisions can include deciding camp locations, when to have breaks, and whether freely roll down a hill or use regen to gain back some energy, the majority of strategic decision can be boiled down to deciding what velocity to maintain at the present moment. For any given set of environmental variables, there is a single velocity that maximizes expected final race performance. In this sense, a good strategy policy can be expressed as a function:
<p align="center"> <img src="https://latex.codecogs.com/svg.latex?\Large&space;velocity=f(environment)" />

The ultimate goal of Athena is to find such a function, so that its velocity output is a better choice than the one decided by a person. Such a function could be called at any moment during the race, and so long as there is fresh input data could adapt to any changes in the environment, expected or unexpected. 

So how do we define such a function? Attempting to curate such a function by hand would be enormously tedious and difficult, and would in principle perform no better than the best strategist working on that project.

Luckily, neural networks are a type of function that can model our ideal function. In fact neural networks can approximate any continuous function to an arbitrary degree of accuracy given enough hidden neurons. Furthermore, since a good race strategy function is somewhat continuous (meaning a small change in environmental variables should correspond to a small change in optimal velocity) a neural network should be able to work quite well.  

To get a sense how neural networks work, take a look at Michael Neilson’s online book: https://neuralnetworksanddeeplearning.com
Chapter 1 introduces the idea of neural networks
Chapter 4 explains its universality property

## neural networks

Naturally, the next question is: How do we construct a neural network that models our desired function? Even ignoring advanced architectures, we still have an abundance of variables and options. 

* number and size of hidden layers (shape)
* weights and biases (parameters)
* type of nonlinearity (activation function)

To simplify the problem, we can say that a network's shape and activation function determine the resolution at which to approximate the function, while the parameters determine what function to approximate. Therefore, roughly speaking, we can first create a method which finds the most suitable parameters given a certain shape, and then worry about optimizing its shape. The proccess of finding the best parameters is often called 'training' or 'learning'

A typical procedure for training a neural network to find good parameters may look like the following:

1) Start with a neural network with randomly initialized parameters
2) Feed it input data and record output
3) Compare actual output to correct output
4) Use backpropagation (calculus) to adjust parameters such that output error decreases for the given example
5) Repeat over tens of thousands to millions of input/output pairs (training examples)

This strategy is often used to learn functions that have definite outputs, and therefore training examples are readily available. We know that a picture of a cat is of cat, whether the stock went up or down last friday, and even if making a particular left turn resulted in a crash. With Athena, however, we don't know how to correctly quantify the quality of a given output. The consequences of a particular strategic decision may not become apparent until a day later, or even until the end of the race, by the time which it's difficult to trace back causality. A person likely does not know *the* ideal strategy for a set of given conditions; therefore, not only will it be tedious to create such vast amounts of training data, Athena would be cursed to never perform better than a person. 

## reinforcement learning

A more appropriate machine learning strategy would be reinforcement learning. The method is at the heart of some recent breakthroughs in AI, creating programs which outperform humans in both discrete and continuous games such as Go, Dota2, Atari and MuJoCo movement. 

A massively simplified explanation of this method would be as follows:
1) Allow the agent to have episodes of interaction with the environment 
2) Keep track of the rewards and future rewards recieved after every action made in every sequence of states
3) Adjust the quality of a given action-state pair to better reflect the expected future rewards
4) Tweak the network using backpropogation so that it would have been more likely to make more rewarding actions 

I believe that a well executed reinforcement learning approach to the problem of solar racing strategy would be the best approach in theory. But, I’m not sure if we have the time and talent at our disposal to complete the project before ASC, though this is definitely a long term goal. 

## evolutionary strategies

An alternative I’ve found is an approach called “Evolutionary Strategies” (ES) researched by OpenAI. They found that performance was comparable to reinforcement learning techniques for benchmarks such as Atari and MuJoCo. 

Its advantages lie in its ability to work in sparse reward environments such as a solar car race, where the only true reward is given at the very end. When comparing to reinforcement learning, it’s important to consider this point - the consequences of strategic decisions made at any point during the race do not decay significantly over the duration of the race. This means that it is difficult (though not impossible) to determine rewards to give in the middle of the race. For example, if we offer a reward for getting to Alice Springs quickly, the policy will maximize the sum of these two rewards, which may not maximize the only metric that matters, which is the final average speed. 

I’ll summarize the method here, but to read in detail about how it works, check out their blog post: 
https://blog.openai.com/evolution-strategies/

1. Start with a randomly initialized network with parameter vector
<br/>	 <img src="https://latex.codecogs.com/svg.latex?\Large&space;p" />

2. Create clones of this network by adding random mutation vectors to the oiginal parameters
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;clone_{i}=p+mutation_{i}" />

3. Allow each copy to interact with the environment
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;outcome_{i}=f(clone_{i})" />

4. Determine each of their rewards based on perfomance
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;r=[outcomes]" />

5. Find difference between performances and mean performance to create a list of weights
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;\mu=\sum(r)/len(r)" />
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;weights=(r-\mu)" />

6. Sum the element-wise products of weights and corresponding mutation vectors and 
add it to the original network to create a new network
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;p_{new}=p+weights*mutations" />

7. Repeat process with new network as the network to be copied
<br/>	<img src="https://latex.codecogs.com/svg.latex?\Large&space;p=p_{new}" />

If we consider the performance of a neural network to be function with network parameters for inputs, then this algorithm is equivalent to randomly sampling nearby points in high dimensional parameter space, evaluating performance at each point, and then moving in the direction that most improves performance. In this way, ES somewhat resembles gradient descent in backpropagation, but without the need of handmade data. Instead, it requires an environment with which to interact and perform.

Where would we find such an environment? In theory we could have this environment be the real world and let networks decide strategy . However, not only would variables not be controlled, but we would never collect enough episodes of interaction. 

The only solution for now is to simulate a race environment, but historically, the success of this method have been limited. The problem arises when a well trained policy (function) in simulation is expected to perform well in the real world. This failure of transferability stems from the discrepancy between the characteristics of a simulated environment and the characteristics of the real environment. For instance, energy loss during charging may be higher than expected or aerodynamic drag doesn’t vary perfectly with the square of relative velocity because of a small relative side wind. Efforts have been made to increase the accuracy and precision of simulations, but this proves to either be extremely difficult and costly or ineffective, if posed as the only solution. 

Fortunately, OpenAI has also researched a method of greatly improving transferability between simulation and reality without hyper-realistic simulations. By randomizing aspects of the simulated environment, one effectively expands the domain of the simulation such that the domain of the physical world is within the simulation domain. This allows policies to be trained well in simulation. 

This way, the policy trained in simulation must gain an ability to adapt to unexpected changes in its environment, rather than relying on the immutability of environmental characteristics found only in simulation. 

Read more: blog.openai.com/generalizing-from-simulation/

This ends the summary of my motivations for starting project athena. 



## challenges
Some potential challenges come to mind 


1. Environment Generation: 
	How do we create a simulated race environment?

2. Simulation Accuracy:
	How can we create a more accurate physical model?

3. Accommodating Unique Circumstances during Training
	How do we account for things like mid-race target rest stops or traffic?

4. Computational Speed
	How do we speed up computation needed during training?

5. Neural Network Optimization
	How do we choose the network architecture, shape, and curate inputs and output(s)

6. Training Hyper-parameter Optimization
	What's the best set of hyper-parameters for training

7. Implementation
	How do we transfer the network from simulation to reality?
	
8. Testing
	How do we validate the performance of a network so we know it will be better than a person?


Environment Generation:

Problem:
The simulation domain must be wide enough to encapsulate the different possible states the car might find itself in while driving - two such conditions are it’s position, weather. Of course, we don’t just want the current location and weather, but also future location and weather (since we can get the data). The problem comes with the high dimensionality of this data. We need at least latitude, road bearing, and incline at multiple points along the road to describe relevant position states. And, we need at least wind magnitude, wind bearing, cloud cover, and temperature at multiple positions and times to describe relevant weather states. This could result in thousands, if not tens of thousands of units of input data - both computationally costly and difficult to learn and regularize. 

graph with car going through time and distance, with points at each sample location for weather and lines for each sample location for road. 

Possible Solutions:
Three options which can be used in conjunction are preprocessing, lower sample rates and filtering.

Preprocessing aims to decrease the amount of data at each state by analytically calculating relevant inputs. For instance, road bearing, wind bearing and wind magnitude are only necessary to compute the component of wind tangent to the road, and therefore can be reduced from three inputs to one. Same could be done for weather data and expected power in from the solar array. 

Next, lower sample rates is an obvious option to reduce the number of inputs: it’s likely not very useful to know that the road incline 1400 miles away from the current position is 5% but at 1401 miles away it’s 2%. The further away data is in distance/time, the lower the sample rate. Also, not all data across all time is needed for sampling, and we could sample the data as such:

Filtering is an idea that could prove very powerful if well implemented, but I’m not yet sure how to go about it without RL. The idea is to apply layers of filters to the weather and position data to extract features from the data much like a convolutional neural network would from a picture. In fact it would be a CNN. The uncertainty is in how to train a network to recognize these features. I have my doubts on whether evolutionary methods are practical. 

Simulation Accuracy:

There are many nice mathematical models for how various aspects of the car should behave, such as:

drag equation:
cosine rule for incident radiation 

Unfortunately, reality does not match these quite so well. It may be worth spending some time doing physical tests to model some of these behaviors more accurately. Some tests include:

Change in drag due to change in effective attack angle
reflectivity of solar array at different angles
internal resistance of batteries as a function of temperature

Accommodating Unique Circumstances during Training

Problem:
A race has more subtlety than driving at different speeds down a road. There’s required stops, unexpected stops, charging at night and morning, traffic, and trailering. The policy must at the very least still work if stops are made - that is, if a random stop is made, the network could recalibrate and successfully continue after the stop ends. That is to say, the network cannot depend on the ability to continuously drive to work successfully. 

Solutions:
Add expected stops during training and some random stops depending on what is expected. More ideally, mid-race stops thats are known ahead of time can be placed at various distances/times along the race route as obstacles, and have the duration/time/location of these stops be inputs. 
Many other circumstances, such as morning and nightly charging can be easily modeled (in simple form)
If time allows, a feature could be added that allows rewards and punishments to be placed onto the map. For instance, an energy reward could be placed at a evening charging location by a reflective lake. 

Computational Speed:

Problem:
The whole training process requires a substantial amount of computation (~10000 generations) * (~40 population size) * (~1000 time steps) * (computation per time step) = 400 million * # of computations per time step
The slower the training process, the more delayed our improvements to the training process is. 

Solution:
Eliminate redundancies where possible and reduce the frequency of environmental updates. For example, rather than recalculating expected solar power for every weather prediction every time step, it’s possible to refer to tables of precalculated values to speed things up as Naman has suggested. 

If not being used for FEA or CFD, the resident ‘supercomputer’ could be used to run each generations’ simulations in parallel. 

5) Neural Network Optimization

Problem:
There’s an abundance of options: different architectures, different shapes and activation functions for each architecture and more. According to OpenAI, policies trained in simulation tend to generalize better when they keep track of previous states/positions

Solution:

6) Training Hyperparameter Optimization

Hyperparameters aer parametesr that determine how the training process proceeds, for instance number generations, population size, and size of mutations. 

Problem:
While better than RL, ES still has many hyper parameters to optimize for. It’s not practical to do a brute force search for the best hyper-parameters

Solution:
Tarin on smaller, simpler problems to get within an order of magnitude of the right parameters, and make small tweaks from therre. More generations means more steps, more population should mean bette steps, smaller mutation size means finer changes in policy, large mutation size means bette exploration of the parameter space. 

Training schedules, which change hyper-parameters as training progresses, will be critical for balancing parameter exploration, tuning and computational cost. An example of this would be to begin training with large mutation vectors and decreases these mutation vectors as the policy improves. 

7) Implementation

Problem:
	We have to create infrastructure which allows the policy to get existing data directly from the car using telemetry, among other inputs. It may also be worthwhile to install new hardware on the car/chase vehicle to increase the amount of available data, such as wind and irradiance. This goes the other way too - we shouldn’t allow information that is unaccessible in IRL to be accessible in simulation. 
	Another issue is what I call immediate strategy. Situations that occur on small timescales will come up, and the appropriate reaction to this situation will not align with what our policy says - on short timescales, physical behaviors such as acceleration and regenerative braking become significant. 

Solution:
	Adding more input data is straightforward, though potentially costly. It will be valuable to simulate the effects of adding different hardware and see which pieces of hardware would be most valuable. 
	Another network could be trained to deal with short-timescale scenarios. It would likely minimize energy spent before returning to the original state. 

8) Testing
Problem:
	How do we validate network and have confidence in its ability in a week long race if it can't be fully physically validated in without at least a full week of testing?
  
Solution:
  A person could compete with a neural network in simulated races through the same environment. The person will get access to the same data, if not more, as the neural network does. If the neural network is able to consistently beat a person by a human by a significant marigin, then we can be confident that the training algorithm works. 
  The issue of generalization from simulation still stands, but that can be verified with shorter tests. 
