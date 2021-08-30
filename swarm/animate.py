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
		self.stream = self.data_stream()

		# Setup figure and axes
		self.fig, self.ax = plt.subplots()
		# Setup FuncAnimation.
		self.anim = animation.FuncAnimation(self.fig, self.update, interval=5,
											init_func=self.setup_plot, blit=True)

	def setup_plot(self):
		"""Initial drawing of the scatter plot."""
		x, y = next(self.stream).T
		self.scat = self.ax.scatter(x, y, c=self.colors, s=20, vmin=0, vmax=1,
									cmap="jet", edgecolor="k")
		self.ax.axis([0, self.width, 0, self.height])
		# For FuncAnimation's sake, we need to return the artist we'll be using
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,

	def data_stream(self):
		"""Creates a Generator for data"""
		x = self.data["XPosition"]
		y = self.data["YPosition"]
		for i in range(self.numtime):
			yield np.c_[x.xs(i, level="Step"), y.xs(i, level="Step")]

	def update(self, i):
		currentData = next(self.stream)
		# Set x and y data
		self.scat.set_offsets(currentData[:, :2])
		# Set sizes
		self.scat.set_sizes(300 * abs(currentData[:, 2])**1.5 + 100)
		# Set colors
		self.scat.set_array(self.colors)

		# We need to return the updated artist for FuncAnimation to draw..
		# Note that it expects a sequence of artists, thus the trailing comma.
		return self.scat,