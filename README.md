# This is a Simulation of how COVID-19 virus can spread in some different case scenarios.

# Contents

 * [Introduction](#introduction)
 * [Requirements](#requirements)
 * [Installation](#installation)
 * [Configuration](#configuration)
 * [How to Run](#how-to-run)
 * [Maintainers](#maintainers)

# Introduction

This "project" started by my curiosity about the covid-19 spread around the world. In my own country, and after everyone knows all health authorities' rules the virus is now attacking harder than never before. Why the virus continues to spread is one of my big questions. So I did this simulation-like project to study the influences of people behavior in the overall number of infected people. As an example, evaluating the influence of 10% of the people within an area do not wear a mask, or do not respect the social distance as we should.

The simulation programming's paradigm is Object-oriented where we have two main classes.
* Simulation
    * Class that stores the list of agents in the simulation and "performs tasks" such as updating the health status on each day of simulation.
* Agent 
    * Class representing the agent where we defined each Agent characteristics such as age, position in the environment, health status, and so on.

Some of the probabilities used are based on real data from my county. The data was retrieved from the response of one service from this [site](https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/). After that, I store the data to have it in a file (I chose not to call the service and avoid that implementation since it takes time). Then I handle the data so I can have, for instance, the percentage of people that die grouped by age range. You can find that logic at the end of `constants.py` file.

In other cases, I simply defined probability values that I think they are valid. Almost all values can be changed in the configuration file if you want to test the Simulation.

# Requirements

To run this project you should have `python>=3.8.3`, as it was developed using that version. 

# Installation

To install the necessary libraries run the command `pip install -r requirements.txt` at the project root folder.

# Configuration

To configure the simulation you can use the `config.yaml` file at the root folder.
There you can change the parameters like the number of agents in the simulation and the probability of being infected by another sick agent
  

# How to Run

Run the command `python ./main.py -h` or `python ./main.py --help` to see how to run the simulation at `/src` folder.

To see the chart in real time go to the `/src` folder and run `python ./live_chart.py`.
  

# Maintainers

 * Joel Carneiro
    * [GitHub](https://github.com/jolasman)
    * [Blog](https://smartinsightblog.blogspot.com/)
    * [LinkedIn](https://www.linkedin.com/in/joelcarneiromieic/)

