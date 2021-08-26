# A wanna-be comprehensive manual of the Mesa framework
Compiled from the Mesa source code function definitions and from Claire Guerin's own use of the framework. This si work in progress, use with a grain of salt.

Mesa has two core objects, Agent and Model. These are the basics to build a Mesa ABM. `Agent` and `Model` each require a `step()` function which contains a single step for the / all individual(s). The `step()` function is used by the Scheduler of your choice. Schedulers are in the `mesa.time` module. *Some Schedulers also require an `advance()` function, which will apply the changes prepared in the `step()` function.*

## Agent class

Attributes:
- `unique_id` agent's unique id
- `pos` agent position on the grid / in space

Methods:
- `step()` single step of the agent.
- `advance()` apply agent's step. To use if scheduler = `SimultaneousActivation`.

## Model class

Attributes:
- `random` random-number generator. Works just like Python's random module, but with a fixed seed set when the model is instantiated, that can be used to replicate a specific model run later.
- `running`  bool indicating if the model should continue running
- `schedule` none if none specified. Can be set like in example code below.
- `current_id` individual ID where the model is currently at. See `next_id()` method.

Methods:
- `run_model()` run the model until the end condition is reached. Overload as needed. 
- `step()` a single step Overload as needed. 
- `next_id()` return the next unique ID for agents, increment `current_id`.
- `reset_randomizer()` reset the model random number generator.

### Example

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

## Schedulers

### BaseScheduler

This is the base scheduler, which activates agents in the order they've been added. It is the parent of all the other schedulers.
- `add(Agent)` adds Agent instance to the scheduler
- `remove(Agent)` removes all instances of Agent from the scheduler
- `get_agent_count()` current number of agents in the queue
- `agent_buffer()` yields the agents while letting the user remove and/or add agents during stepping
- `step()` executes the step of all the agents

The scheduler has an internal list `agents` of all the agents it is scheduled to activate.

### RandomActivation

Executes the step of all agents, one at a time, in random order.

### SimultaneousActivation
**Requires `advance()` method in Agent class.** Executes the step of the agents simultaneously. `step()` activates the agents and stages any necessary changes, but does not apply them yet. `advance()` applies the changes.

### StagedActivation
Allows agent activation to be divided into several stages instead of a single `step` method. All agents execute one stage before moving on to the next. Agents must have all the stage methods implemented. Stage methods take a model object as their only argument. This schedule tracks steps and time separately. Time advances in fractional increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.

Optional arguments:
- `stage_list` List of strings of names of stages to run, in the order to run them in.
- `shuffle` If True, shuffle the order of agents each step.
- `shuffle_between_stages` If True, shuffle the agents after eachstage; otherwise, only shuffle at the start of each step.

## Space
Mesa currently supports two overall kinds of spaces: grid, and continuous. Both grids and continuous spaces are frequently toroidal, meaning that the edges wrap around, with cells on the right edge connected to those on the left edge, and the top to the bottom. This prevents some cells having fewer neighbors than others, or agents being able to go off the edge of the environment. Import the space type of your choice from `mesa.space`.

### Grid
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

### SingleGrid
Grid where each cell contains exactly at most one object. Inherits `Grid` attributes and methods.

- `position_agent()` Position an agent on the grid. This is used when first placing agents! If x or y arguments are positive, they are used, but if "random", sets a random position. Ensure this random position is not occupied (`is_cell_empty()` in Grid).
- `move_to_empty()` Use when you want agents to jump to an empty cell.
- `swap_pos()` Use to swap agents positions.

### MultiGrid
Grid where each cell can contain more than one object. Inherits `Grid` attributes and methods. Grid cells are indexed by `[x][y]`, where `[0][0]` is assumed to be at bottom-left and `[width-1][height-1]` is the top-right. If a grid is toroidal, the top and bottom, and left and right, edges wrap to each other. Each grid cell holds a set object.

### HexGrid
Extends Grid to handle hexagonal neighbors. Functions according to odd-q rules. See [here](http://www.redblobgames.com/grids/hexagons/#coordinates) for more.

### ContinuousSpace
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
- `get_distance()` Get the distance between two points, accounting for toroidal space.
- `torus_adj()` Adjust coordinates to handle torus looping. If the coordinate is out-of-bounds and the space is toroidal, return the corresponding point within the space. If the space is not toroidal, raise an exception.
- `out_of_bounds()` Check if a point is out of bounds.

### NetworkGrid
Network Grid where each node contains zero or more agents.

- `place_agent()` Place an agent in a node.
- `get_neighbors()` Get all adjacent nodes
- `move_agent()` Move an agent from its current node to a new node.
- `remove_agent()` Remove the agent from the network and set its pos variable to `None`.
- `is_cell_empty()` Returns a bool of the contents of a cell.
- `get_cell_list_contents()`
- `get_all_cell_contents()`
- `iter_cell_list_contents()`

## Data Collector
Handles data collection and storage for us and make it easier to analyze.
The data collector stores three categories of data: model-level variables, agent-level variables, and tables (which are a catch-all for everything else). Model- and agent-level variables are added to the data collector along with a function for collecting them.
A `DataCollector` is instantiated with dictionaries of names of model- and agent-level variables to collect, associated with attribute names or functions which actually collect them. When the `collect(...)` method is called, it collects these attributes and executes these functions one by one and stores the results.

```python
from mesa.datacollection import DataCollector

def compute_mean(model):
	# A function to compute summary statistic, will be used by the Data Collector
	agent_x, agent_y = 0
	n = 0
	for agent in model.schedule.agents:
		agent_x += agent.pos[0]
		agent_y += agent.pos[1]
		++n
	return [agent_x / n, agent_y / n]

class myModel(Model):
	def __init__(self, N, width, height):
		#...

		self.dataCollector = DataCollector(
			model_reporters={"Mean position": compute_mean},
			agent_reporters={"ID": "unique_id"}) # <- define Data Collector here

	def step(self):
		self.datacollector.collect(self) # <- collect data here
        self.schedule.step()
```

Arguments:
- `model_reporters` Dictionary of reporter names and attributes/funcs
- `agent_reporters` Dictionary of reporter names and attributes/funcs.
- `tables` Dictionary of table names to lists of column names.

Both `model_reporters` and `agent_reporters` accept a dictionary mapping a variable name to either an attribute name, or a method. For example, if there was only one model-level reporter for number of agents, it might look like: `{"agent_count": lambda m: m.schedule.get_agent_count() }`. If there was only one agent-level reporter (e.g. the agent's energy), it might look like this: `{"energy": "energy"}` or like this: `{"energy": lambda a: a.energy}`. Model reporters can take four types of arguments:
- **lambda**: `{ "agent_count": lambda m: m.schedule.get_agent_count() }`
- method with **@property decorators**: `{ "agent_count": schedule.get_agent_count() }`
- class **attributes** of model: `{"model_attribute": "model_attribute"}`
- **functions** with parameters that are placed in a list: `{"Model_Function":[function, [par1, par2]]}`

The `tables` argument accepts a dictionary mapping names of tables to lists of columns. For example, if we want to allow agents to write their age when they are destroyed (to keep track of lifespans), it might look like: `{"Lifespan": ["unique_id", "age"]}`

If you want to [pickle](https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/) your model, do not use lambda functions. If your model includes a large number of agents, you should *only* use attribute names for the agent reporter, it will be much faster.

Attributes:
- `model_reporters`
- `agent_reporters`
- `model_vars`
- `tables`

Methods:
- `collect(model)` Collect all the data for the given model object.
- `add_table_row(table_name, row)` Add a row dictionary to a specific table.
- `get_model_vars_dataframe()` Create a pandas DataFrame from the *model* variables. Has one column for each model variable, with index = model tick.
- `get_agent_vars_dataframe()` Create a pandas DataFrame from the *agent* variables. Has one column for each variable, with two additional columns for tick and `agent_id`.
- `get_table_dataframe(table_name)` Create a pandas DataFrame from a particular table. 

### Plotting

The `DataCollector` can export the data it has collected as a pandas DataFrame, for easy interactive analysis.

```python
model = myModel(50, 10, 10)
for i in range(100):
    model.step()

mean_pos = model.datacollector.get_model_vars_dataframe()
mean_pos.plot()

agent_pos = model.datacollector.get_agent_vars_dataframe()
agent_pos.head() # DataFrame
```
