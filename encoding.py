# This module creates a population of random OS and MS chromosomes

import config
import random

def generateOS(parameters):
    machinesNb = parameters['machinesNb']
    jobs = parameters['jobs']

    OS = []
    i = 0
    for job in jobs:
        for op in job:
            OS.append(i)
        i = i+1

    random.shuffle(OS)

    return OS

def generateMS(parameters):
    machinesNb = parameters['machinesNb']
    jobs = parameters['jobs']

    MS = []
    for job in jobs:
        for op in job:
            randomMachine = random.randint(0, len(op)-1)
            MS.append(op[randomMachine]['machine'])

    return MS

def initializePopulation(parameters):
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))

    return gen1