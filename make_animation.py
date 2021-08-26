from swarm.model import Swarm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, rc
from IPython.display import HTML, Image

nAgents = 3
nSteps = 5
spaceWidth = 100
spaceHeight = 100

model = Swarm(nAgents, spaceWidth, spaceHeight) # number of individuals, x max, y max in continuous space (defaulted to x min = y min = 0)
for i in range(nSteps):
	model.step()

agent_data = model.dataCollector.get_agent_vars_dataframe()

###################################################################

# Setup the figure and axes...
fig, ax = plt.subplots()
colors = np.random.rand(nAgents)
scat = ax.scatter([], [], color=colors, s=200)

def setup_plot():
	"""Initial drawing of the scatter plot."""
	ax.axis([0, spaceWidth, 0, spaceHeight])
	# For FuncAnimation's sake, we need to return the artist we'll be using
	# Note that it expects a sequence of artists, thus the trailing comma.
	return scat,

def update(i):
	"""Update the scatter plot."""
	x = agent_data.xs(i, level="Step")["XPosition"]
	y = agent_data.xs(i, level="Step")["YPosition"]

	# Set x and y data...
	scat.set_offsets([x, y])
	# Set sizes...
	#scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
	# Set colors..
	#scat.set_array(data[:, 3])

	# We need to return the updated artist for FuncAnimation to draw..
	# Note that it expects a sequence of artists, thus the trailing comma.
	return scat,

# Then setup FuncAnimation.
anim = animation.FuncAnimation(fig, update, interval=5, init_func=setup_plot, blit=True)
#anim.save('img/agents_in_space.gif', writer='imagemagick', fps=60)