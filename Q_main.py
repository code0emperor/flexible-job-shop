#!/usr/bin/env python

import sys
import time
import random
import numpy as np

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config


# Beginning
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Parameters Setting
    parameters = parser.parse(sys.argv[1])

    # print(parameters)

    t0 = time.time()
    print(t0)

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    gen = 1

    Q_values = np.zeros((len(config.possible_pr_values), len(config.possible_pc_values), len(config.possible_pm_values)))

    # Q-learning parameters
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor

    # Evaluate the population
    while not termination.shouldTerminate(population, gen):
        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        # Evaluate the population
        makespans = [genetic.timeTaken(individual, parameters) for individual in population]

        # Calculate rewards based on makespans
        rewards = [1 / makespan for makespan in makespans]

        # Update Q-values using Q-learning
        for i, pr_value in enumerate(config.possible_pr_values):
            for j, pc_value in enumerate(config.possible_pc_values):
                for k, pm_value in enumerate(config.possible_pm_values):
                    Q_values[i, j, k] = (1 - alpha) * Q_values[i, j, k] + alpha * (np.mean(rewards) + gamma * np.argmax(Q_values))
        
        # Adjust probability parameters based on Q-values
        pr_index, pc_index, pm_index = np.unravel_index(np.argmax(Q_values), Q_values.shape)
        parameters['pr'] = config.possible_pr_values[pr_index]
        parameters['pc'] = config.possible_pc_values[pc_index]
        parameters['pm'] = config.possible_pm_values[pm_index]

        gen = gen + 10.

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    # Termination Criteria Satisfied ?
    gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))

    # if config.latex_export:
    #     # print("#################################")
    #     gantt.export_latex(gantt_data)
    # else:
    #     gantt.draw_chart(gantt_data)
    gantt.draw_chart(gantt_data)

    for i in range(5):
        for j in range(5):
            for k in range(5):
                print(f"pc_value = {config.possible_pc_values[j]}, 
                      pm_value = {config.possible_pm_values[k]}, 
                      Q[{i}][{j}][{k}] = {Q_values[i][j][k]}")