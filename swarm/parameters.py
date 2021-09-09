class Parameters(object):

	def __init__(self):
		self.cohesionRadius = 2
		self.alignmentRadius = 5
		self.separationRadius = 15
		self.cohesionWeight = float(1/3)
		self.alignmentWeight = float(1/3)
		self.separationWeight = float(1/3)
		self.cohesionAngle = 60
		self.alignmentAngle = 60
		self.separationAngle = 90

		self.cruiseSpeed = 2.0  # speed in body length / s