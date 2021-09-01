from mesa.space import *
from swarm.vectors import *
from math import radians, atan2

class Area(ContinuousSpace):
	""" Child class of Mesa Subclass ContinuousSpace from Mesa Space
	    Overwrites get_neighbors method to include blind spot(s) """
	def get_neighbors(
		self, 
		pos: FloatCoordinate, 
		radius: float, 
		include_center: bool = True,
		focal_heading: list,
		blind_angle: float,
		front: bool = False
	) -> List[GridContent]:
		"""Get all objects within a certain radius.
		Args:
			pos: (x,y) coordinate tuple to center the search at.
			radius: Get all the objects within this distance of the center.
			include_center: If True, include an object at the *exact* provided
							coordinates. i.e. if you are searching for the
							neighbors of a given agent, True will include that
							agent in the results.
			focal_heading: focal.heading vector
			blind_angle: Angle of the blind spot, in degrees (will be translated to radians)
			front: If True, include blind spot in front. Else, blind spot will only be in the back
		"""
		# Neighbors are agents: 
		# 1) within radius, i.e. distance between pos and agent.pos <= radius
		deltas = np.abs( self._agent_points - np.array(pos) )

		if self.torus:
			deltas = np.minimum(deltas, self.size - deltas)
		dists = deltas[:, 0] ** 2 + deltas[:, 1] ** 2

		(idxs,) = np.where(dists <= radius ** 2)


		# 2) outside of blind spot (in the back, and in the front if True), i.e. 
		# IN THE BACK:
		# !(beta + Pi - alpha / 2 < gamma < beta + Pi + alpha / 2), where
		# alpha = blind_angle in radians
		# beta = heading angle of focal agent
		# gamma = angle of agent.pos from x-axis in radians

		alpha = radians(blind_angle)
		beta = angle(focal_heading) 
		gamma = np.atan2( self._agent_points - np.array(pos) ) # WARNING: 
		# returns value between -Pi and Pi, 
		# should check whether this is automatically translated


		# Get neighbors

		neighbors_no_blind_spot = [
			self._index_to_agent[x] for x in idxs if include_center or dists[x] > 0
		]
		

		return neighbors