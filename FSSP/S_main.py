import sys
import time
import random
import numpy as np

from Utils import parser, config
from Genetic import encoding, genetic
from src.RL import learning


# Beginning
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Parameters Setting
    parameters = parser.parse(sys.argv[1])

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    gen = 1

    # print(population)

    # parameters['pc'] = config.pc
    # parameters['pm'] = config.pm

    action_t = random.randrange(10)
    Q_values = np.zeros((len(config.states), len(config.possible_pm_values)))

    t0 = time.time()

    for eval in range(config.maxGen):
        #selection
        parents = genetic.select_parent(population, parameters)
        children = []

        parameters = learning.get_pc_pm_values(action_t, parameters)

        #crossover
        for parent in parents:
            r = np.random.rand()
            if r < parameters['pc']:
                children.append(genetic.crossover(parent))
            else:
                if r < 0.5:
                    children.append(parent[0])
                else:
                    children.append(parent[1])
        # print(children)
        
        mutatedChildren = []
        for child in children:
            r = np.random.rand()
            if r < parameters['pm']:
                mutatedChild = genetic.mutation(child)
                mutatedChildren.append(mutatedChild)
        
        children.extend(mutatedChildren)
        if(len(children)) > 0:
            genetic.update_population(population, children, parameters)
    
    t1 = time.time()

    costedPop = []
    for individual in population:
        indMakespan = (genetic.calc_makespan(individual, parameters['jobs'], len(parameters['jobs']), parameters['machinesNb']), individual)
        costedPop.append(indMakespan)
    costedPop.sort(key=lambda x: x[0])

    avgObjective = sum(cost[0] for cost in costedPop) / len(costedPop)
    bestObjective = costedPop[0][0]

    print("best chromosome value: ", bestObjective)
    print("Solution: ", costedPop[0][1])
    # print("CostedPop: ", costedPop)
    


