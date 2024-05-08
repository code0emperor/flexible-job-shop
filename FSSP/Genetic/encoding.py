#!/usr/bin/env python

import numpy as np
from Utils import config

def initializePopulation(parameters):
    population = []
    jobsNb = len(parameters['jobs'])
    # print(jobsNb)
    i = 0
    while i < config.popSize:
        individual = list(np.random.permutation(jobsNb))
        if individual not in population:
            population.append(individual)
            i += 1

    return population
