from mesa import Agent
import logging
#import numpy as np
from flock.logging import *

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.bodyLength = 3 # body length in arbitrary unit
        self.position = (0, 0)
        #self.x = None
        #self.y = None
        #self.speed = None # speed in body length / s
        #self.direction = np.array([None, None]) # direction vector in 2D space
        
    def step(self):
        """ The agent's step will go here.
        For demonstration purposes, we increase body length"""
        self.bodyLength += self.unique_id
        self.n_neighbors = len( model.space.get_neighbors(self.position, 3, False) ) # pos: FloatCoordinate, radius: float, include_center: bool = True
               
    def advance(self):
        """Apply changes incurred in step()
        For demonstration purposes we will print the agent's unique_id"""        
        logging.info( 'Agent {0} {1} has {2} neighbors'.format(self.unique_id, self.position, self.n_neighbors) )