from swarm.model import Swarm
import matplotlib.pyplot as plt
import numpy as np

nAgents = 10
nSteps = 20
spaceWidth = 5
spaceHeight = 5

model = Swarm(nAgents, spaceWidth, spaceHeight) # number of individuals, x max, y max in continuous space (defaulted to x min = y min = 0)
for i in range(nSteps):
	model.step()

agent_data = model.dataCollector.get_agent_vars_dataframe()
#agent_data.head()

plt.ion() # turn on interactive plotting
colors = np.random.rand(nAgents)

for step in range(nSteps):
	x = agent_data.xs(step, level="Step")["XPosition"]
	y = agent_data.xs(step, level="Step")["YPosition"]
	# area = (30 * np.random.rand(nAgents))**2  # 0 to 15 point radii
	plt.scatter(x, y, s=200, c=colors, alpha=0.5) # to change dot area: s=area
	plt.xlim([0, spaceWidth])
	plt.ylim([0, spaceHeight])
	plt.title("Step {0}".format(step))
	plt.draw()
	plt.pause(0.1)
	plt.clf() # clear current figure