#!/usr/bin/env python3

import sys
import time
import random
import numpy as np

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src.RL import learning
from src import config

# Beginning
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Parameters Setting
    parameters = parser.parse(sys.argv[1])

    # print(parameters)

    t0 = time.time()

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    firstPop = population
    gen = 0

    Q_values = np.zeros((len(config.states), len(config.possible_pm_values)))
    
    makespans = [genetic.timeTaken(individual, parameters) 
                     for individual in population]
    
    action_t = random.randrange(10)

    firstMakespans = [genetic.timeTaken(individual, parameters) 
                       for individual in firstPop]
    state_t = learning.calculate_state(makespans, firstMakespans)

    # SARSA parameters
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor

    # Evaluate the population
    while not termination.shouldTerminate(gen):
        prevMakespans = makespans

        # Getting new parameter values
        parameters = learning.get_pc_pm_values(action_t, parameters)

        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        # Evaluate the fitness
        makespans = [genetic.timeTaken(individual, parameters) 
                     for individual in population]
        
        # Calculate rewards based on makespans
        reward_t_1 = learning.calculateRewards(makespans, prevMakespans)

        # Calculate new State
        state_t_1 = learning.calculate_state(makespans, firstMakespans)

        Q_values, action_t_1 = learning.sarsa(state_t, action_t, Q_values, state_t_1, reward_t_1)

        # Updating current state
        state_t = state_t_1

        # Executing new action
        action_t = action_t_1

        gen = gen + 1.

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    # Termination Criteria Satisfied ?
    gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))

    gantt.draw_chart(gantt_data)

    for i in range(20):
        for j in range(10):
            print(f"Q[{i}][{j}] = {Q_values[i][j]}")
                