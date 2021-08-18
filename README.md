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
Mesa has two core objects, Agent and Model. These are the basics to build a Mesa ABM. `Agent` and `Model` each require a `step()` function which contains a single step for the / all individual(s). Load and use them in Python with: 

```python
from mesa import Agent, Model

class myAgent(Agent):
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model) # use super class Agent's init function in child class myAgent
		# ...

	def step(self):
		# do something

class myModel(Model):
	def __init__(self, n):
		self.numberOfAgents = n

		for i in range(self.numberOfAgents):
			agent = myAgent(i, self)

	def step():
		# do something
``` 

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