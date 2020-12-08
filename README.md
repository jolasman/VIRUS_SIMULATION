# This is a Simulation of how COVID-19 virus can spread in some different case scenarios.
<div style="text-align: justify "> 

# Disclaimer 
**This project aims to simulate the human being and COVID-19 behaviours, however, the real behaviours can be very different from the conceptual model I defined. The simulation's results are based on simple math calculations and probabilities, where we have a big margin for errors.**
# Contents

 * [Introduction](#introduction)
 * [Requirements](#requirements)
 * [Installation](#installation)
 * [Configuration](#configuration)
 * [How to Run](#how-to-run)
 * [Maintainers](#maintainers)

# Introduction

This "project" started with my curiosity about the covid-19 spread around the world. In my own country, and after everyone knows all health authorities' rules the virus is now attacking harder than never before. Why the virus still continues to spread: This is one of my big questions. So I did this simulation-like project to study the influences of people behaviours in the overall number of infected people. As an example, evaluating the influence of 10% of the people within an area do not wear a mask, or do not respect the social distance as we should.

To build the simulation I used the python programming language and the Object-oriented programming paradigm. I did not use any python library to build the simulation environment itself. It is just two classes to represent the Agents and the Simulation.

## Classes

* Simulation
    * The class that stores the list of agents in the simulation and "performs tasks" such as updating the health status, the quarantine zone, and move the agents on each day of simulation.
* Agent
    * The class representing the agent where we defined each Agent characteristics such as age, position in the environment, health status, name, number of days with the virus, and so on.


The simulation is based on random Agent behaviours to simulate the free will of real persons. So, the functions to move the agents use a randomly generated number in the x-axis and y-axis. I also added a parameter to limit the agent's movement ray to test cases where the agents' moves are limited, and a social distancing value that forces the agents to choose a position, when they need to move, with a distance to another agent greater than the social distance value. As you must already found out, the simulation has two dimensions to represent the agent's position (x-axis and y-axis. The environment's size is also configurable to evaluate the free space impact in the virus spread.


With regard to the Agents, we have two different ways of creating them: 
* We can create n agents based on probabilities of being Healthy, Sick, Asymptomatic, or the agent's immune system response to the virus being moderately infected, etc. 

* The other possible way is by specifying the number of agents of each type of health status and immune system response. 

Please note that only in the first case the age of each agent is used as the factor to indicate the immune system response. The second approach, defined as static begging in the simulation, do not take into account the age of the agent. The immune system response type is randomly distributed by the agents, according to the specified numbers for each type.
# The age influence
In the random beginning approach, I used probabilities based on real data from my country when it comes to age range death data. The data was retrieved from the response of one service from this site. After that, I stored the data to have it in a file (I chose not to call the service and avoid that implementation since it takes time). Then I handle the data so I can have, for instance, the percentage of people that die grouped by age range. You can find that logic at the end of constants.py file. In other cases, I simply defined probability values that I think are valid. Almost all values can be changed in the configuration file (config.yaml) if you want to test the Simulation. The file also includes the variables' meaning in the simulation context through code comments. 

Using the Simulation
After having your own configurations, you can run the simulation in a trivial graphic mode. This mode shows an image in a black background and the agents represented by pixels with different colours, also configurable in the config.yaml file. In each simulation day, the image is updated. I chose this approach as it is quite simple and quick to develop, and my focus was not in the graphical part. You can also run a parallel small script to show you, in real-time, the current simulation's cumulative values. 
# Requirements

To run this project you should have `python>=3.8.3`, as it was developed using that version. 

# Installation

To install the necessary libraries run the command `pip install -r requirements.txt` at the project root folder.

# Configuration

To configure the simulation you can use the `config.yaml` file at the root folder.
There you can change the parameters like the number of agents in the simulation and the probability of being infected by another sick agent.

# How to Run

Run the command `python ./main.py -h` or `python ./main.py --help` to see how to run the simulation at `/src` folder.

To see the chart in real time go to the `/src` folder and run `python ./live_chart.py`.

Suggested commands:
* `python ./main.py -s -d -g` --> for a single run of the simulation. Runs in graphical mode and saves the data.
* `python ./main.py -s -d -g -multi=10` --> for multiple runs of the same config file. Runs in graphical mode and saves the data.
* `python ./main.py -s -l -max=10` --> for getting the average charts for old simulations with the same config file.

  

# Maintainers

 * Joel Carneiro
    * [GitHub](https://github.com/jolasman)
    * [Blog](https://smartinsightblog.blogspot.com/)
    * [LinkedIn](https://www.linkedin.com/in/joelcarneiromieic/)

</div>
