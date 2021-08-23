from mesa import Agent
import logging
import numpy as np
import math as m
from flock.logging import *
#import pytest

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.heading = (0, 0) # heading vector of agent, zero before the agent is placed in space

    def head(self):
        self.newPos = np.asarray(self.pos) + self.model.parameters.cruiseSpeed * self.newHeading

    def group(self, radius):
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

        if alignmentGroup:

            alignmentVector = np.array([0, 0])

            for neighbor in alignmentGroup:
                alignmentVector += np.asarray(neighbor.pos)

            alignmentDirection = -1 / len(alignmentGroup) * alignmentVector
            alignmentMagnitude = m.sqrt( np.sum( np.square(alignmentDirection - self.heading) ) )

            alignmentForce = self.model.parameters.alignmentWeight * alignmentDirection / alignmentMagnitude

        else:
            alignmentForce = np.asarray(self.heading)

        # HEADING
        self.newHeading = alignmentForce
        self.head()
               
    def advance(self):
        """Apply changes incurred in step()"""  
        logging.info("Agent {0} moves from {1}".format(self.unique_id, self.pos))      
        self.model.space.move_agent(self, self.newPos)
        self.heading = self.newHeading
        logging.info(" to {0}\n".format(self.pos))