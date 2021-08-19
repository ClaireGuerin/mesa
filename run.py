from flock.model import Swarm

model = Swarm(10, 5, 5)
for i in range(20):
	model.step()