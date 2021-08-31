import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class AnimationScatter(object):
	"Animate scatter plot data from a Pandas DataFrame"

	def __init__(self, numtime, numpoints, width, height, data_generator):
		self.numtime = numtime
		self.numpoints = numpoints
		self.width = width
		self.height = height
		self.stream = data_generator

		self.colors = np.random.rand(self.numpoints)

		# Setup figure and axes
		self.fig, self.ax = plt.subplots()
		# Setup FuncAnimation.
		self.anim = animation.FuncAnimation(self.fig, self.update, interval=5,
											init_func=self.setup_plot, blit=True)

	def setup_plot(self):
		"""Initial drawing of the scatter plot."""
		xy = next(self.stream)
		x = xy[1, :]
		y = xy[2, :]

		self.scat = self.ax.scatter(x, y, c=self.colors, s=200, vmin=0, vmax=1,
									cmap="jet", edgecolor="k")
		self.ax.axis([0, self.width, 0, self.height])
		# For FuncAnimation's sake, we need to return the artist we'll be using
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,

	def update(self, i):
		currentData = next(self.stream)
		# Set x and y data
		self.scat.set_offsets(currentData)
		# Set sizes
		self.scat.set_sizes([200 for n in range(self.numpoints)])
		# Set colors
		self.scat.set_array(self.colors)

		# We need to return the updated artist for FuncAnimation to draw..
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,