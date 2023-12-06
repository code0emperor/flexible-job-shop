#!/usr/bin/env python3

import sys
import time
import random
import numpy as np

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

def get_pc_pm_values(idx, parameters):
    random_float = random.random()
    random_scaled = random_float * config.pc_interval
    parameters['pc'] = config.possible_pc_values[idx] + random_scaled

    random_float = random.random()
    random_scaled = random_float * config.pm_interval
    parameters['pm'] = config.possible_pm_values[idx] + random_scaled

    return parameters

def calculate_state(makespans, prevMakespans):
    f_star = np.sum(makespans)/np.sum(prevMakespans)
    d_star = np.sum(makespans - np.mean(makespans))/np.sum(prevMakespans - np.mean(prevMakespans))
    m_star = np.max(makespans)/np.max(prevMakespans)

    S_star = (config.w1 * f_star) + (config.w2 * d_star) + (config.w3 * m_star)

    for i in range(1,20):
        if S_star < config.set_states[i]:
            return i-1
    return 19

def calculateRewards(makespans, prevMakespans):
    r_c = (np.max(makespans) - np.max(prevMakespans))/np.max(prevMakespans)
    r_m = (np.sum(makespans) - np.sum(prevMakespans))/np.sum(prevMakespans)

    return (config.wc*r_c) + (config.wm*r_m)

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

    Q_values = np.zeros((len(config.set_states), len(config.possible_pm_values)))
    
    makespans = [genetic.timeTaken(individual, parameters) 
                     for individual in population]
    
    action_t = random.randrange(10)

    firstMakespans = [genetic.timeTaken(individual, parameters) 
                       for individual in firstPop]
    state_t = calculate_state(makespans, firstMakespans)

    # SARSA parameters
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor

    # Evaluate the population
    while not termination.shouldTerminate(gen):
        prevMakespans = makespans

        # Getting new parameter values
        parameters = get_pc_pm_values(action_t, parameters)

        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        # Evaluate the fitness
        makespans = [genetic.timeTaken(individual, parameters) 
                     for individual in population]
        
        # Calculate rewards based on makespans
        reward_t_1 = calculateRewards(makespans, prevMakespans)

        # Calculate new State
        state_t_1 = calculate_state(makespans, firstMakespans)

        # Choosing action with epsilon-greedy
        random_num = random.uniform(0.00, 1.00)
        random_action = random.randrange(10)

        # Epsilon-greedy Approach
        action_t_1 = np.argmax(Q_values[state_t_1]) if (config.epsilon >= random_num) else random_action

        print(f"action_t_1 = {action_t_1} random_num = {random_num}, random_action = {random_action}")
        # Update Q-values using SARSA
        Q_values[state_t][action_t] = (1 - alpha) * Q_values[state_t, action_t] \
                            + alpha * (reward_t_1 + gamma * Q_values[state_t_1, action_t_1])

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
                