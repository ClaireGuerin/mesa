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
	""" Returns the angle in radians of a vector vec with the positive x-axis +x
		theta in [-pi, pi]
	    theta = arctan2(y, x) 
	    !!! y before x !!!"""
	return np.arctan2(vec[1], vec[0])
	
def normalize(ang):
	# sometimes an angle in radians is between -pi and pi
	# this function transforms an angle in radians between 0 and 2pi:
	return ang if ang >= 0 else 2 * np.pi + ang
