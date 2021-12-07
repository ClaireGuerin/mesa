class Parameters(object):

	def __init__(self):
		self.cohesionRadius = 2 # in body length (BL)
		self.alignmentRadius = 5 # in BL
		self.separationRadius = 15 # in BL
		self.cohesionWeight = 9 # in BM/s^2
		self.alignmentWeight = 5 # in BM/s^2
		self.separationWeight = 10 # in BM/s^2
		self.cohesionAngle = 60 # in degrees
		self.alignmentAngle = 60 # in degrees
		self.separationAngle = 90 # in degrees

		self.randomNoise = 0.5

		self.cruiseSpeed = 2.0  # cruise speed in BL/s.
		self.relaxationTime = 0.2 # characteristic time scale for the return to cruise speed, in s.
  
		self.border_distance = 10
		self.border_strength = 0.5