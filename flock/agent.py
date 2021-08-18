from mesa import Agent
import numpy as np

class Fish(Agent):
    """ An agent with body length, position, scalar speed, direction."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.bodyLength = 3 # body length in arbitrary unit
        #self.position = np.array([2,3]) # position vector from arbitrary origin O(0,0).
        #self.x = None
        #self.y = None
        #self.speed = None # speed in body length / s
        #self.direction = np.array([None, None]) # direction vector in 2D space
        
        #get_neighbours
        
        def step(self):
            """ The agent's step will go here.
            For demonstration purposes, we increase body length by 1"""
            self.bodyLength += 1
            
            
        def advance():
            """Apply changes incurred in step()
            For demonstration purposes we will print the agent's unique_id"""
            print ("Fish #" + str(self.unique_id) + ", BL= " + str(self.bodyLength) + ".")
            
            