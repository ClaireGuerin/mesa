import numpy as np

def magnitude(vec):
	""" Returns the magnitude of vector vec """
	return np.sqrt( vec.dot(vec) )

def unit(vec):
	""" Returns the unit vector of vec"""
	mag = magnitude(vec)
	if mag == 0.0:
		return 0.0
	else:
		return vec / magnitude(vec)

def direction(vec, n):
	""" Returns the direction vector """
	return - 1 / n * vec

def force(weight, sumVec, n):
	""" Returns the force vector """
	return weight * unit( direction(sumVec, n) )

def angle(vec):
	""" Returns the angle in radians of a vector vec with the x-axis +x
	    θ = cos^−1(a_x/|a⃗ |) """
	return np.arccos(vec[0] / magnitude(vec))
