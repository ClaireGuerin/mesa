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

### A wanna-be comprehensive manual of the Mesa framework
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

The scheduler has an internal list `agents` of all the agents it is scheduled to activate.

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

#### Space
Mesa currently supports two overall kinds of spaces: grid, and continuous. Both grids and continuous spaces are frequently toroidal, meaning that the edges wrap around, with cells on the right edge connected to those on the left edge, and the top to the bottom. This prevents some cells having fewer neighbors than others, or agents being able to go off the edge of the environment. Import the space type of your choice from `mesa.space`.

##### Grid
Base class for a square grid.

Attributes:
- `width`, `height` The grid's width and height.
- `torus` Boolean which determines whether to treat the grid as a torus.
- `grid` Internal list-of-lists which holds the grid cells themselves.

Methods:
- `get_neighbors()` Returns the objects surrounding a given cell.
- `get_neighborhood()` Returns the cells surrounding a given cell.
- `get_cell_list_contents()` Returns the contents of a list of cells ((x,y) tuples). Returns a list of the contents of the cells identified in `cell_list`.
- `neighbor_iter()` Iterates over position neighbours.
- `coord_iter()` Returns coordinates as well as cell contents.
- `place_agent()` Positions an agent on the grid, and set its pos variable.
- `move_agent()` Moves an agent from its current position to a new position.
- `iter_neighborhood()` Returns an iterator over cell coordinates that are in the neighborhood of a certain point.
- `torus_adj()` Converts coordinate, handles torus looping.
- `out_of_bounds()` Determines whether position is off the grid, returns the out of bounds coordinate.
- `iter_cell_list_contents()` Returns an iterator of the contents of the cells identified in `cell_list`.
- `remove_agent()` Removes an agent from the grid.
- `is_cell_empty()` Returns a bool of the contents of a cell.

##### SingleGrid
Grid where each cell contains exactly at most one object. Inherits `Grid` attributes and methods.

- `position_agent()` Position an agent on the grid. This is used when first placing agents! If x or y arguments are positive, they are used, but if "random", sets a random position. Ensure this random position is not occupied (`is_cell_empty()` in Grid).
- `move_to_empty()` Use when you want agents to jump to an empty cell.
- `swap_pos()` Use to swap agents positions.

##### MultiGrid
Grid where each cell can contain more than one object. Inherits `Grid` attributes and methods. Grid cells are indexed by `[x][y]`, where `[0][0]` is assumed to be at bottom-left and `[width-1][height-1]` is the top-right. If a grid is toroidal, the top and bottom, and left and right, edges wrap to each other. Each grid cell holds a set object.

##### HexGrid
Extends Grid to handle hexagonal neighbors. Functions according to odd-q rules. See [here](http://www.redblobgames.com/grids/hexagons/#coordinates) for more.

##### ContinuousSpace
Continuous space where each agent can have an arbitrary position. Assumes that all agents are point objects, and have a pos property storing their position as an (x, y) tuple. This class uses a numpy array internally to store agent objects, to speed up neighborhood lookups.

Attributes:
- `x_max`, `y_max` Maximum x and y coordinates for the space.
- `torus` Boolean for whether the edges loop around.
- `x_min`, `y_min` (default `0`) If provided, set the minimum x and y coordinates for the space. Below them, values loop to the other edge (if torus=True) or raise an exception.
- `width`, `height`, `center`
- `size`

Methods:
- `place_agent()` Place a new agent in the space.
- `move_agent()` Move an agent from its current position to a new position.
- `remove_agent()` Remove an agent from the simulation.
- `get_neighbors()` Get all objects within a certain radius.
- `get_heading()` Get the heading angle between two points, accounting for toroidal space.
- `get_distance()` Get the distance between two point, accounting for toroidal space.
- `torus_adj()` Adjust coordinates to handle torus looping. If the coordinate is out-of-bounds and the space is toroidal, return the corresponding point within the space. If the space is not toroidal, raise an exception.
- `out_of_bounds()` Check if a point is out of bounds.

##### NetworkGrid
Network Grid where each node contains zero or more agents.

- `place_agent()` Place an agent in a node.
- `get_neighbors()` Get all adjacent nodes
- `move_agent()` Move an agent from its current node to a new node.
- `remove_agent()` Remove the agent from the network and set its pos variable to `None`.
- `is_cell_empty()` Returns a bool of the contents of a cell.
- `get_cell_list_contents()`
- `get_all_cell_contents()`
- `iter_cell_list_contents()`


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