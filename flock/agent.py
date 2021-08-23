from mesa import Agent
import logging
#import numpy as np
import math as m
from flock.logging import *

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.bodyLength = 3 # body length in arbitrary unit
        self.speed = 2 # speed in body length / s
        self.direction = 2 * m.pi / 3 # direction angle in radians

    def head(self):
        newX = self.pos[0] + self.speed * m.cos(self.direction)
        newY = self.pos[1] + self.speed * m.sin(self.direction)
        self.newPos = (newX, newY)

        
    def step(self):
        """ The agent's step will go here.
        For demonstration purposes, we increase body length"""
        self.bodyLength += self.unique_id
        #self.n_neighbors = len( self.model.space.get_neighbors(self.pos, 1, False) ) # pos: FloatCoordinate, radius: float, include_center: bool = True
        self.head()
               
    def advance(self):
        """Apply changes incurred in step()"""  
        logging.info("Agent {0} moves from {1}".format(self.unique_id, self.pos))      
        self.model.space.move_agent(self, self.newPos)
        logging.info(" to {0}\n".format(self.pos))