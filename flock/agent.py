from mesa import Agent
import logging
import numpy as np
import math as m
from flock.logging import *

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.heading = (0, 0) # heading vector of agent, zero before the agent is placed in space

    def head(self):
        newX = self.pos[0] + self.model.parameters.cruiseSpeed * m.cos(self.direction)
        newY = self.pos[1] + self.model.parameters.cruiseSpeed * m.sin(self.direction)
        self.newPos = (newX, newY)

    def group(self. radius):
         # pos: FloatCoordinate, radius: float, include_center: bool = True
        self.model.space.get_neighbors(self.pos, radius, False)
        
    def step(self):
        """ The agent's step will go here.
        The agent has three areas:
        - cohesion (radius 2)
        - alignment (radius 5)
        - separation (radius 15) """

        # ALIGNMENT
        alignmentGroup = self.group(self.model.parameters.alignmentRadius)
        xSum, ySum = 0

        for neighbor in alignmentGroup:
            xSum += neighbor.pos[0]
            ySum += neighbor.pos[1]

        alignmentDirection = -1 / len(alignmentGroup) * np.array([xSum, ySum])
        alignmentMagnitude = m.sqrt( np.sum( np.square(alignmentDirection - self.heading) ) )

        self.alignmentForce = self.model.parameters.alignmentWeight * alignmentDirection / alignmentMagnitude

        self.head()
               
    def advance(self):
        """Apply changes incurred in step()"""  
        logging.info("Agent {0} moves from {1}".format(self.unique_id, self.pos))      
        self.model.space.move_agent(self, self.newPos)
        logging.info(" to {0}\n".format(self.pos))