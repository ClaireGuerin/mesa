# Swarming with Mesa

Agent based modelling with Python's Mesa package. Reproduces fish schools swarming behaviour in a fully synchronous manner, as opposed to NetLogo's swarming and flocking models, which are inherently asynchronous (due to parallelization)

## Project Status

In progress, starting stage

## Visuals

Coming soon

## Installation

Fork or download this repository on your local machine. 

### Requirements

This code was developped under Ubuntu (20.04.2 LTS)

Install [Mesa](https://mesa.readthedocs.io/en/master/) with `pip install mesa`
Make sure you have Numpy installed in your Python environment.

## Usage

### Using Mesa
Mesa has two core objects, Agent and Model. These are the basics to build a Mesa ABM. `Agent` and `Model` each require a `step()` function which contains a single step for the / all individual(s). The `step()` function is used by the Scheduler of your choice. Schedulers are in the `mesa.time` module. *Some Schedulers also require an `advance()` function, which will apply the changes prepared in the `step()` function.*


```python
from mesa import Agent, Model
from mesa.time import RandomActivation

class myAgent(Agent):
	def __init__(self, unique_id, model):
		'''use super class Agent's init function in child class myAgent'''
		super().__init__(unique_id, model)
		# ...

	def step(self):
		# do something

	def advance(self):
		pass

class myModel(Model):
	def __init__(self, n):
		self.numberOfAgents = n
		self.schedule = RandomActivation(self) # create the Scheduler. In this case, agents are activated at random

		for i in range(self.numberOfAgents):
			agent = myAgent(i, self)
			self.schedule.add(agent) # add agent to the Scheduler

	def step(self):
		self.schedule.step() # activate agents' steps according to the schedule, here at random.
``` 

#### Schedulers

##### BaseScheduler

This is the base scheduler, which activates agents in the order they've been added. It is the parent of all the other schedulers.
- `add(Agent)` adds Agent instance to the scheduler
- `remove(Agent)` removes all instances of Agent from the scheduler
- `get_agent_count()` current number of agents in the queue
- `agent_buffer()` yields the agents while letting the user remove and/or add agents during stepping
- `step()` executes the step of all the agents

##### RandomActivation

Executes the step of all agents, one at a time, in random order.

##### SimulataneousActivation
**Requires `advance()` method in Agent class.** Executes the step of the agents simultaneously. `step()` activates the agents and stages any necessary changes, but does not apply them yet. `advance()` applies the changes.


## Support 

Raise an issue 

## Roadmap

- basic fish school placed on grid
- individual fish movement based on others (rules of cohesion, avoidance and alignment)
- visual output
- dynamic parameter control

## Contributing

Fork this repository and send pull requests

## Authors and acknowledgments

Code developped by [Claire Guerin](https://github.com/ClaireGuerin)

## License

[GNU General Public License v3.0](https://github.com/ClaireGuerin/mesa/blob/main/LICENSE)