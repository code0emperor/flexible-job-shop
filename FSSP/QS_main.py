import sys
import time
import random
import numpy as np

from Utils import parser, config
from Genetic import encoding, genetic
from Rl import learning

# Beginning
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Parameters Setting
    parameters = parser.parse(sys.argv[1])
    t0 = time.time()

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    gen = 1

    # print(population)
    # parameters['pc'] = config.pc
    # parameters['pm'] = config.pm

    Q_values = np.zeros((len(config.states), len(config.possible_pm_values)))

    makespans = [genetic.calc_makespan(individual, parameters['jobs'], len(parameters['jobs']), parameters['machinesNb'])
                 for individual in population]
    
    # print(makespans)
    a_t = random.randrange(10)

    first_makespans = [genetic.calc_makespan(individual, parameters['jobs'], len(parameters['jobs']), parameters['machinesNb'])
                 for individual in population]

    s_t = learning.calculate_state(makespans, first_makespans)

    for eval in range(config.maxGen):
        prev_makespans = makespans

        parameters = learning.get_pc_pm_values(a_t, parameters)

        #selection
        parents = genetic.select_parent(population, parameters)
        children = []

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

        makespans = [genetic.calc_makespan(individual, parameters['jobs'], len(parameters['jobs']), parameters['machinesNb'])
                 for individual in population]
        
        r_t_1 =learning.calculateRewards(makespans, prev_makespans)
        s_t_1 = learning.calculate_state(makespans, first_makespans)

        a_t_1 = 0

        ## SARSA
        if(gen < (len(config.states) * len(config.possible_pc_values) / 2)):
            Q_values, a_t_1 = learning.sarsa(s_t, a_t, Q_values, s_t_1, r_t_1)
        ## Q-LEARNING
        else:
            Q_values, a_t_1 = learning.qLearning(s_t, a_t, Q_values, s_t_1, r_t_1)

        s_t = s_t_1
        a_t = a_t_1
        if(a_t > 9):
            a_t = 9

        gen = gen+1
    
    t1 = time.time()

    costedPop = []
    for individual in population:
        indMakespan = (genetic.calc_makespan(individual, parameters['jobs'], len(parameters['jobs']), parameters['machinesNb']), individual)
        costedPop.append(indMakespan)
        print(indMakespan)
    costedPop.sort(key=lambda x: x[0])

    avgObjective = sum(cost[0] for cost in costedPop) / len(costedPop)
    bestObjective = costedPop[0][0]

    print("best chromosome value: ", bestObjective)
    print("Solution: ", costedPop[0][1])
    # print("CostedPop: ", costedPop)
    


