from mesa.space import *

class Area(ContinuousSpace):
	""" Child class of Mesa Subclass ContinuousSpace from Mesa Space
	    Overwrites get_neighbors method to include blind spot(s) """
	def get_neighbors(
		self, pos: FloatCoordinate, radius: float, include_center: bool = True
	) -> List[GridContent]:
		"""Get all objects within a certain radius.
		Args:
			pos: (x,y) coordinate tuple to center the search at.
			radius: Get all the objects within this distance of the center.
			blind_angle: Angle of the blind spot
			front: If True, include blind spot in front. Else, blind spot will only be in the back
			include_center: If True, include an object at the *exact* provided
							coordinates. i.e. if you are searching for the
							neighbors of a given agent, True will include that
							agent in the results.
		"""
		deltas = np.abs(self._agent_points - np.array(pos))

		if self.torus:
			deltas = np.minimum(deltas, self.size - deltas)
		dists = deltas[:, 0] ** 2 + deltas[:, 1] ** 2

		(idxs,) = np.where(dists <= radius ** 2)
		neighbors = [
			self._index_to_agent[x] for x in idxs if include_center or dists[x] > 0
		]

		return neighbors