from mesa import Agent
import numpy as np
import math as m
from swarm.log import *
#import pytest
from swarm.vectors import *

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model, init_x, init_y):
        super().__init__(unique_id, model)
        self.heading = unit(np.array([init_x, init_y])) # heading vector of agent
        self.speed = self.model.parameters.cruiseSpeed # current speed of the individual. Initially, the same as cruise speed. UPDATE???

    def group(self, radius, angle, include_front = False, include_center = False):
         # pos: FloatCoordinate, radius: float, include_center: bool = True
        self.model.space.get_neighbors( pos=self.pos, 
                                        radius=radius, 
                                        focal_heading=self.heading, 
                                        blind_angle=angle, 
                                        include_center=include_center,
                                        include_front=include_front)

    def align(self):
        """ ALIGNMENT """

        alignmentGroup = self.group(radius=self.model.parameters.alignmentRadius,
                                    angle=self.model.parameters.alignmentAngle,
                                    include_front=True)

        if alignmentGroup:
            # if there are other agents within the alignement area:

            alignmentVector = np.array([0, 0])

            for neighbor in alignmentGroup:
                alignmentVector += neighbor.heading[0]

            alignmentDirection = direction( alignmentVector, len(alignmentGroup) )

            return self.model.parameters.alignmentWeight * unit(alignmentDirection - self.heading[0])

        else:
            # if there are no neighbors in the vicinity, the agent changes its heading at random
            jitterX = self.model.random.gauss(0.0, 1.0)
            jitterY = self.model.random.gauss(0.0, 1.0)
            return self.heading + np.array([jitterX, jitterY])

    def cohese(self):
        """ COHESION
        attraction to the center of gravity of the group within the cohesion area """

        cohesionGroup = self.group( radius=self.model.parameters.cohesionRadius,
                                    angle=self.model.parameters.cohesionAngle)

        if cohesionGroup:
            # if there are other agents within the cohesion area:

            cohesionVector = np.array([0, 0])

            for neighbor in cohesionGroup:
                distance = np.asarray(neighbor.pos) - np.asarray(self.pos)
                cohesionVector += unit(distance)

            return force(self.model.parameters.cohesionWeight, cohesionVector, len(cohesionGroup))
        else:
            return np.array([0, 0])

    def separate(self):
        """ SEPARATION """

        separationGroup = self.group(   radius=self.model.parameters.separationRadius,
                                        angle=self.model.parameters.separationAngle)

        if separationGroup:
            # if there are other agents within the separation area:

            separationVector = np.array([0, 0])

            for neighbor in separationGroup:
                distance = np.asarray(neighbor.pos) - np.asarray(self.pos)
                separationVector += distance / ( magnitude(distance) * magnitude(distance) )

            return force(self.model.parameters.separationWeight, separationVector, len(separationGroup))
        else:
            return np.array([0, 0])

    def err(self):
        """ STOCHASTICITY
            Random error in movement alignement based on others"""
        errorX = self.model.random.gauss(0.0, self.model.parameters.randomNoise)
        errorY = self.model.random.gauss(0.0, self.model.parameters.randomNoise)
        return np.array([errorX, errorY])

    def adjust_speed(self):
        """ ADJUST OWN SPEED BASED ON OTHERS TO AVOID COLLISION OR REJOIN THE GROUP
            From Hemelrijk & Hildenbrandt 2008:
            (1 / tau) * (v0 - v) * x, where:
            - tau = relaxation time, fixed parameter
            - v0 = cruise speed
            - v = current scalar speed, agent characteristic
            - x = x-coordinate of the agent's current heading """
        return (1 / self.model.parameters.relaxationTime) * (self.model.parameters.cruiseSpeed - self.speed) * self.heading[0]
        
    def step(self):
        """ The agent takes into account three areas:
        - cohesion (radius defaulted to 2)
        - alignment (radius defaulted to 5)
        - separation (radius defaulted to 15) """

        # Calculate new HEADING and POS according to others
        self.newHeading = self.align() + self.cohese() + self.separate() + self.err() + self.adjust_speed()
        self.newSpeed = magnitude(self.newHeading)
        assert not self.newSpeed != self.newSpeed, self.newSpeed # Checking isnan
        # self.newPos = np.asarray(self.pos) + self.model.parameters.cruiseSpeed * self.newHeading
        self.newPos = np.asarray(self.pos) + self.newHeading
               
    def advance(self):
        """Apply changes incurred in step(), i.e. update agent's position and heading"""  
        logging.info("Agent {0} moves from {1}".format(self.unique_id, self.pos))  
        assert np.isnan(self.newPos).any, "{1},{0}".format(np.isnan(self.newPos), self.newPos)
        self.model.space.move_agent(self, tuple(self.newPos))
        assert type(self.pos) is tuple, type(self.pos)
        assert self.pos == tuple(self.newPos), "Self position is {0} when it should be {1}".format(self.pos, tuple(self.newPos))
        self.heading = self.newHeading
        self.speed = self.newSpeed # this line creates a bug
        logging.info(" to {0}, speed = {1}, heading = {2}\n".format(self.pos, self.speed, self.heading))