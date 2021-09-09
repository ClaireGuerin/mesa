# Swarming with Mesa

Agent based modelling with Python's Mesa package. Reproduces fish schools swarming behaviour in a fully synchronous manner, as opposed to NetLogo's swarming and flocking models, which are inherently asynchronous (due to parallelization)

## Project Status

In Progress

### Functionalities

Swarm Agents update their heading based on:
- alignement zone
- cohesion zone
- separation zone
- noise

Swarm agents lack these features:
- blind zone
- speed adjustment

## Visuals

![agents in space](https://github.com/ClaireGuerin/mesa/blob/develop/img/agents_in_space.gif)

## Installation

Fork or download this repository on your local machine. 

### Requirements

This code was developped under Ubuntu (20.04.2 LTS)

Install [Mesa](https://mesa.readthedocs.io/en/master/) with `pip install mesa`
Make sure you have Numpy installed in your Python environment.

## Usage

For help understanding the Mesa framework, checkout [MESAHELP](https://github.com/ClaireGuerin/mesa/blob/develop/doc/MESAHELP.md)

To run the default model, use command line `python run.py` in terminal.
To reproduce the animation in Visuals, use command line `python make_animation.py` in terminal.

### Classes

- `SwarmAgent` in `agent.py`. A child class of Mesa's `Agent` class
- `ModelAgent` in `model.py`. A child class of Mesa's `Model` class
- `Area` in `area.py`. A child class of Mesa's `ContinuousSpace` class
- `AnimationScatter` in `animate.py`. Creates animations of graphical output.

## Support 

Raise an issue 

## Roadmap

- basic fish school placed on grid
- individual fish movement based on others (rules of cohesion, avoidance and alignment)
- visual output
- dynamic parameter control

## Contributing

Fork this repository and send pull requests

## Authors and acknowledgments

Code developped by [Claire Guerin](https://github.com/ClaireGuerin)

## License

[GNU General Public License v3.0](https://github.com/ClaireGuerin/mesa/blob/main/LICENSE)