from mesa import Model
#from mesa.space import MultiGrid
from mesa.time import RandomActivation
from flock.agent import Fish
import logging


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]::%(levelname)s  %(message)s',
                    datefmt='%Y.%m.%d - %H:%M:%S')


class Swarm(Model):
    """A model with some number of Fish agents."""
    def __init__(self, N, width, height):
        self.n_agents = N
        #self.grid = MultiGrid(width, height, True)

        logging.info('Creating model...\n')
        
        self.schedule = RandomActivation(self) # scheduler, very useful to control the individual order to perform actions
        # Here, it simulates the simultaneous activation of all the agents.
        # This scheduler requires that each agent have two methods: step and advance.
        # step() activates the agent and stages any necessary changes, but does not
        # apply them yet. advance() then applies the changes.

        # Create agents
        for i in range(self.n_agents):
            logging.info( 'Generating agent {0}\n'.format(i) )
            fishAgent = Fish(i, self)

            self.schedule.add(fishAgent)

            # Add the agent to a random grid cell
            #x = self.random.randrange(self.grid.width)
            #y = self.random.randrange(self.grid.height)
            #self.grid.place_agent(fishAgent, (x, y))
            #fishAgent.x = x
            #fishAgent.y = y
            
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()