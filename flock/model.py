from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from flock.agent import Fish
from flock.logging import *
from flock.parameters import Parameters as Par


class Swarm(Model):
    """A model with some number of Fish agents."""
    def __init__(self, N, x_max, y_max):
        self.nAgents = N
        self.space = ContinuousSpace(x_max, y_max, True)
        self.schedule = SimultaneousActivation(self) # scheduler, with simultaneous activation of all the agents.
        # This scheduler requires that each agent have two methods: step and advance.
        # - step() activates the agent and stages any necessary changes, but does not apply them yet. 
        # - advance() then applies the changes.
        self.dataCollector = DataCollector(
            agent_reporters={"Position": "pos",
                             "Heading": "heading"})
        self.parameters = Par()

        logging.info('Creating model...\n')
        
        # Create agents
        for i in range(self.nAgents):
            logging.info( 'Generating agent {0}\n'.format(i) )

            # Give the agent a random position in space
            # Using the model's random generator
            x = self.random.randrange(1, self.space.width)
            y = self.random.randrange(1, self.space.height)

            fishAgent = Fish(i, self, x, y)

            # Add the agent to the scheduler and to space
            self.schedule.add(fishAgent)            
            self.space.place_agent( fishAgent, (x, y) )
            
    def step(self):
        '''Advance the model by one step.'''
        self.dataCollector.collect(self)
        self.schedule.step()