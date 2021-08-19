from flock.model import Swarm

model = Swarm(10, 5, 5) # number of individuals, x max, y max in continuous space (defaulted to x min = y min = 0)
for i in range(20):
	model.step()