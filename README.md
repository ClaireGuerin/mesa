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

### A mostly comprehensive description of the classes in the Mesa framework
Mesa has two core objects, Agent and Model. These are the basics to build a Mesa ABM. `Agent` and `Model` each require a `step()` function which contains a single step for the / all individual(s). The `step()` function is used by the Scheduler of your choice. Schedulers are in the `mesa.time` module. *Some Schedulers also require an `advance()` function, which will apply the changes prepared in the `step()` function.*

#### Agent class

Attributes:
- `unique_id` agent's unique id
- `pos` agent position on the grid

Methods:
- `step()` single step of the agent.
- `advance()` apply agent's step. To use if scheduler = `SimultaneousActivation`.

#### Model class

Attributes:
- `random` random-number generator. Works just like Python's random module, but with a fixed seed set when the model is instantiated, that can be used to replicate a specific model run later.
- `running`  bool indicating if the model should continue running
- `schedule` none if none specified. Can be set like in example code below.
- `current_id` individual ID where the model is currently at. See `next_id()` method.

Methods:
- `run_model()` run the model until the end condition is reached. Overload as needed. 
- `step()` a single step Overload as needed. 
- `next_id()` return the next unique ID for agents, increment `current_id`.
- `rest_randomizer()` reset the model random number generator.

#### Example

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

##### SimultaneousActivation
**Requires `advance()` method in Agent class.** Executes the step of the agents simultaneously. `step()` activates the agents and stages any necessary changes, but does not apply them yet. `advance()` applies the changes.

##### StagedActivation
Allows agent activation to be divided into several stages instead of a single `step` method. All agents execute one stage before moving on to the next. Agents must have all the stage methods implemented. Stage methods take a model object as their only argument. This schedule tracks steps and time separately. Time advances in fractional increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.

Optional arguments:
- `stage_list` List of strings of names of stages to run, in the order to run them in.
- `shuffle` If True, shuffle the order of agents each step.
- `shuffle_between_stages` If True, shuffle the agents after eachstage; otherwise, only shuffle at the start of each step.

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