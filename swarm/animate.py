import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class AnimationScatter(object):
	"Animate scatter plot data from a Pandas DataFrame"

	def __init__(self, numtime, numpoints, width, height, data):
		self.numtime = numtime
		self.numpoints = numpoints
		self.width = width
		self.height = height
		self.data = data

		self.colors = np.random.rand(self.numpoints)
		self.sizes = [200 for n in range(self.numpoints)]


		# Initial drawing of the scatter plot.
		## Setup figure and axes
		self.fig, self.ax = plt.subplots()
		x = [None] * self.numpoints
		y = [None] * self.numpoints

		self.scat = self.ax.scatter(x, y, c=self.colors, s=self.sizes, vmin=0, vmax=1,
								cmap="jet", edgecolor="k")
		self.ax.axis([0, self.width, 0, self.height])

		# Setup FuncAnimation.
		# update the plot with update function, fed with subsequent frames from the data_stream generator function
		self.anim = animation.FuncAnimation(self.fig, self.update, frames=self.data_stream, 
											interval=500, blit=True)

	def data_stream(self):
		"""Creates a Generator for data"""
		for i in range(self.numtime):
			yield np.c_[self.data.xs(i, level="Step")["XPosition"].values.tolist(), 
						self.data.xs(i, level="Step")["YPosition"].values.tolist()]

	def update(self, frame):
		currentData = frame
		# Set x and y data
		self.scat.set_offsets(currentData)
		# Set sizes
		self.scat.set_sizes(self.sizes)
		# Set colors
		self.scat.set_array(self.colors)

		# We need to return the updated artist for FuncAnimation to draw..
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,

	def save(self):
		self.anim.save('img/agents_in_space.gif', writer='imagemagick', fps=2)

if __name__ == '__main__':
    print("This script cannot be run by itself")