from swarm.model import Swarm
from swarm.animate import AnimationScatter as Animation

nAgents = 300
nSteps = 1000
spaceWidth = 10000
spaceHeight = 10000

model = Swarm(nAgents, spaceWidth, spaceHeight) # number of individuals, x max, y max in continuous space (defaulted to x min = y min = 0)
for i in range(nSteps):
	model.step()

# Make an object with agent data
agent_data = model.dataCollector.get_agent_vars_dataframe()

# Make and save animation
anim = Animation(nSteps, nAgents, spaceWidth, spaceHeight, agent_data[["XPosition", "YPosition"]])
anim.save('img/agents_in_space.gif', 15)