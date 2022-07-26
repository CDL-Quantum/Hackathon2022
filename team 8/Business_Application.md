# Space Debris Removal Optimization

### What is Space Debris?
Space debris (also known as space junk, space pollution, space waste, space trash, or space garbage)  refers to objects that were created by humans but are no longer functional in space.
The debris includes rocket thrusters, abandoned satellites, and most importantly, fragments from collisions and explosions. It is estimated that 95% of all manmade satellites in low Earth orbit (LEO) are space junk.

![Space Debris](./images/space_debris.jpg)

### Problems Created by Space Debris
There were approximately 128 million pieces of debris under 1 cm (0.4 in), about 900,000 pieces between 1 and 10 cm, and approximately 34,000 pieces larger than 10 cm (3.9 in) in orbit around the Earth as of January 2019.

Space debris orbits around the earth at tremendous speeds - about 15,700 miles per hour (25,265 kph) in low Earth orbit which is 10 times the speed of a bullet. So there is a possibility that active satellites and spacecraft could be damaged by space debris. Space travel is also at risk due to all this debris. 

A large amount of space debris in orbit could hinder satellite activities for many generations to come.

Kessler syndrome (also called Kessler effect) was proposed by NASA scientist Donald J. Kessler in 1978 as a scenario where collisions between objects in low Earth orbit (LEO) may result in a cascade creating space debris and increasing collision likelihood. According to Kessler, modeling results concluded in 2009 that the debris environment was already unstable, "such that attempts to eliminate past debris sources will likely fail since fragments from future collisions will be generated faster than atmospheric drag can remove them." 

### Recent Events
* Space junk slams into International Space Station, leaving hole in robotic arm: Space junk hurtling towards the station smashed into one of its robotic arms, leaving a hole. 
NASA and the Canadian Space Agency first noticed the damage on Canadarm2 on May 12, according to a recent statement. The debris left a gaping hole in a section of the arm boom and thermal blanket. 
* International Space Station swerves to dodge space junk: 
The ISS had been forced to move due to space junk from a U.S. launch vehicle sent into orbit in 1994.
 A close encounter was avoided by dropping by 310 metres (339 yards) as part of an unscheduled maneuver carried out by mission control.


### Space Debris Removal Optimization
In space debris removal optimization, the goal is to create an optimal path for satellite vessels to collect as much debris as possible in one pass, while saving fuel. As a result, space debris collection will take fewer days overall.

A space debris removal optimization could also be described as combinatorial optimization, which is searching for maxima (or minima) of an objective function F whose domain is a discrete but large configuration space (in contrast to an N-dimensional continuous space).

![Space Debris](./images/knapsack.png)

This can be also considered as a Knapsack problem where the goal is to determine the number of items each with a weight and value to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible. According to its name, it refers to the problem of filling a fixed-size knapsack with valuable items when constrained by a fixed size. A similar problem occurs when decision-makers have to select from a set of non-divisible projects or tasks within a fixed budget or timeframe.

### Potential Customers
* Space agencies such as NASA, ESA, etc.
* Governments across the world.
* Space companies such as SpaceX, OneWeb, etc.
* Space debris removal startups such as CleanSpace, Astroscale, etc.

### Architecture

We gather open source space debris data and encode it for Pennylane from Xanadu. As a pre-processing step, we also use AI to clean and rank debris according to size, collection cost, etc. 

### Business Model
Yearly Subscription: Our solution is scalable and can be used by several space companies or agencies with no or minimal changes. Our model returns the optimal path for satellite vessels to collect as much debris as possible in one pass.

We offer both on-premises and cloud deployment options for our model on yearly subscription basis.

### References:
* https://en.wikipedia.org/wiki/Space_debris
* https://www.youtube.com/watch?v=Ctvzf_p0qUA
* https://www.cbsnews.com/news/space-junk-damage-international-space-station
* https://www.reuters.com/lifestyle/science/international-space-station-swerves-dodge-space-junk-2021-12-03
* https://en.wikipedia.org/wiki/Knapsack_problem