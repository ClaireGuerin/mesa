from swarm.model import Swarm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
# from IPython.display import HTML, Image

nAgents = 3
nSteps = 5
spaceWidth = 100
spaceHeight = 100

model = Swarm(nAgents, spaceWidth, spaceHeight) # number of individuals, x max, y max in continuous space (defaulted to x min = y min = 0)
for i in range(nSteps):
	model.step()

agent_data = model.dataCollector.get_agent_vars_dataframe()

def data_stream():
		"""Creates a Generator for data"""
		for i in range(nSteps):
			yield np.c_[agent_data.xs(i, level="Step")["XPosition"].values.tolist(), 
						agent_data.xs(i, level="Step")["YPosition"].values.tolist()]

# stream = data_stream()

colors = np.random.rand(nAgents)
sizes = [200 for n in range(nAgents)]

# Setup figure and axes
fig, ax = plt.subplots()


"""Initial drawing of the scatter plot."""
#xy = next(stream)
x = []
y = []

scat = ax.scatter(x, y, c=colors, s=200, vmin=0, vmax=1,
					cmap="jet", edgecolor="k")
ax.axis([0, spaceWidth, 0, spaceHeight])

def update(frame):
	currentData = frame
	# Set x and y data
	scat.set_offsets(currentData)
	# Set sizes
	scat.set_sizes(sizes)
	# Set colors
	scat.set_array(colors)

	# We need to return the updated artist for FuncAnimation to draw..
	# Note that it expects a sequence of artists, thus the trailing comma.
	return scat,


# Setup FuncAnimation.
anim = animation.FuncAnimation(fig, update, frames=data_stream, interval=5, blit=True)
plt.show()

# ###################################################################

# # Setup the figure and axes...
# fig, ax = plt.subplots()
# colors = np.random.rand(nAgents)
# scat = ax.scatter([], [], color=colors, s=200)

# def setup_plot():
# 	"""Initial drawing of the scatter plot."""
# 	ax.axis([0, spaceWidth, 0, spaceHeight])
# 	# For FuncAnimation's sake, we need to return the artist we'll be using
# 	# Note that it expects a sequence of artists, thus the trailing comma.
# 	return scat,

# def update(i):
# 	"""Update the scatter plot."""
# 	x = agent_data.xs(i, level="Step")["XPosition"]
# 	y = agent_data.xs(i, level="Step")["YPosition"]

# 	# Set x and y data...
# 	scat.set_offsets([x, y])
# 	# Set sizes...
# 	#scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
# 	# Set colors..
# 	#scat.set_array(data[:, 3])

# 	# We need to return the updated artist for FuncAnimation to draw..
# 	# Note that it expects a sequence of artists, thus the trailing comma.
# 	return scat,

# # Then setup FuncAnimation.
# anim = animation.FuncAnimation(fig, update, interval=5, init_func=setup_plot, blit=True)
# #anim.save('img/agents_in_space.gif', writer='imagemagick', fps=60)

# from swarm.animate import AnimationScatter as Animation

# anim = Animation(nSteps, nAgents, spaceWidth, spaceHeight, d)
# plt.show()