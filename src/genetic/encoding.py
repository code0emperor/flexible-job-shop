#!/usr/bin/env python

# This module creates a population of random OS and MS chromosomes

import random
from src import config


def generateOS(parameters):
    jobs = parameters['jobs']
    # print(jobs)
    OS = []
    i = 0
    for job in jobs:
        print("job:",job)
        for op in job:
            OS.append(i)
        i = i+1
    print(OS)
    random.shuffle(OS)

    return OS


def generateMS(parameters):
    jobs = parameters['jobs']

    MS = []
    for job in jobs:
        for op in job:
            randomMachine = random.randint(0, len(op)-1)
            MS.append(randomMachine)

    return MS


def initializePopulation(parameters):
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))
    # print(gen1)
    return gen1
