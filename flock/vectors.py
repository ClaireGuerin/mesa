import numpy as np

def magnitude(vec):
	return np.sqrt( vec.dot(vec) )

def unit(vec):
	return vec / magnitude(vec)

def direction(vec, n):
	return - 1 / n * vec

def force(vec, weight, sumVec, n):
	return weight * unit( direction(sumVec, n) )
