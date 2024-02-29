#!/usr/bin/env python

# This script contains a high level overview of the proposed hybrid algorithm
# The code is strictly mirroring the section 4.1 of the attached paper

import sys
import time
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

    parameters['pc'] = config.pc
    parameters['pm'] = config.pm

    # Evaluate the population
    while not termination.shouldTerminate(gen):
        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        gen = gen + 10.

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    makespans = [genetic.timeTaken(individual, parameters) 
                     for individual in population]

    print(makespans)
    print(np.min(makespans))
    print(np.average(makespans))

    # Termination Criteria Satisfied ?
    gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))

    # if config.latex_export:
    #     # print("#################################")
    #     gantt.export_latex(gantt_data)
    # else:
    #     gantt.draw_chart(gantt_data)
    # gantt.draw_chart(gantt_data)
