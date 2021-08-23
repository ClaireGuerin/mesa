from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import SimultaneousActivation
from flock.agent import Fish
from flock.logging import *


class Swarm(Model):
    """A model with some number of Fish agents."""
    def __init__(self, N, x_max, y_max):
        self.n_agents = N
        self.space = ContinuousSpace(x_max, y_max, True)
        self.schedule = SimultaneousActivation(self) # scheduler, very useful to control the individual order to perform actions
        # Here, it simulates the simultaneous activation of all the agents.
        # This scheduler requires that each agent have two methods: step and advance.
        # step() activates the agent and stages any necessary changes, but does not
        # apply them yet. advance() then applies the changes.

        logging.info('Creating model...\n')
        
        # Create agents
        for i in range(self.n_agents):
            logging.info( 'Generating agent {0}\n'.format(i) )
            fishAgent = Fish(i, self)

            self.schedule.add(fishAgent)

            # Add the agent to a random position in space
            # Using the model's random generator
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            fishAgent.position = (x, y)
            self.space.place_agent( fishAgent, (x, y) )
            
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()