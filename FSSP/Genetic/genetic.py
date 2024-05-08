#!/usr/bin/env python

import random
import time
import numpy as np

def calc_makespan(solution, proccessing_time, number_of_jobs, number_of_machines):
    cost = [0] * number_of_jobs
  
    for machine_no in range(0, number_of_machines):
        # print("machine_no: ",machine_no)
        for slot in range(number_of_jobs):
            cost_so_far = cost[slot]
            # print("slot: ", slot)
            # print("solution: ", solution)
            # print("solution[slot]: ",solution[slot])
            # print("ProcTime: ",proccessing_time[solution[slot]][machine_no])
            if slot > 0:
                cost_so_far = max(cost[slot - 1], cost[slot])
            cost[slot] = cost_so_far + proccessing_time[solution[slot]][machine_no]
    return cost[number_of_jobs - 1]

def crossover(parents):
    # print("parents: ", parents)
    parent1 = parents[0]
    parent2 = parents[1]
    length_of_parent = len(parent1)
    first_point = int(length_of_parent / 2 - length_of_parent / 4)
    second_point = int(length_of_parent - first_point)
    intersect = parent1[first_point:second_point]

    child = []
    index = 0
    for pos2 in range(len(parent2)):
        if first_point <= index < second_point:
            child.extend(intersect)
            index = second_point
        if parent2[pos2] not in intersect:
                child.append(parent2[pos2])
                index += 1

    return child

def mutation(solution):
    mutated_solution = list(solution)
    solution_length = len(solution)
    
    swap_positions = list(np.random.permutation(np.arange(solution_length))[:2])
    first_job = solution[swap_positions[0]]
    second_job = solution[swap_positions[1]]
    mutated_solution[swap_positions[0]] = second_job
    mutated_solution[swap_positions[1]] = first_job
    return mutated_solution

# Selects parent by binary tournament method
def select_parent(population, parameters):
    number_of_jobs = len(parameters['jobs'])
    number_of_machines = parameters['machinesNb']
    parent_pairs = []
    # randomly choose how many parent pairs will be selected
    parent_pair_count = random.randint(2, int(len(population)/2))
    for k in range(parent_pair_count):
        parent1 = binary_tournament(number_of_jobs, number_of_machines, population, parameters['jobs'])
        parent2 = binary_tournament(number_of_jobs, number_of_machines, population, parameters['jobs'])
        if parent1 != parent2 and (parent1, parent2) not in parent_pairs:
            parent_pairs.append((parent1, parent2))
    return parent_pairs

def binary_tournament(number_of_jobs, number_of_machines, population, processing_time):
    parent = []
    candidates = random.sample(population, 2)
    # print("Candidate Binary Tourney:", candidates)
    makespan1 = calc_makespan(candidates[0], processing_time, number_of_jobs, number_of_machines)
    makespan2 = calc_makespan(candidates[1], processing_time, number_of_jobs, number_of_machines)
    if makespan1 < makespan2:
        parent = candidates[0]
    else:
        parent = candidates[1]
    return parent

def update_population(population, children, parameters):
    no_of_jobs = len(parameters['jobs'])
    no_of_machines = parameters['machinesNb']
    processing_time = parameters['jobs']
    costed_population = []
    i = 0
    # print("Population: ", population)
    # print("Length of population", len(population))
    # time.sleep(3)
    for individual in population:
        # print("iteration: ", i)
        # print("individual in updatePop: ",individual)
        # time.sleep(1)
        i=i+1
        ind_makespan = (calc_makespan(individual, processing_time, no_of_jobs, no_of_machines), individual)
        costed_population.append(ind_makespan)
    costed_population.sort(key=lambda x: x[0], reverse=True)

    costed_children = []
    # print("Children: ", children)
    for individual in children:
        # print("Individual: ", individual)
        ind_makespan = (calc_makespan(individual, processing_time, no_of_jobs, no_of_machines), individual)
        costed_children.append(ind_makespan)
    costed_children.sort(key=lambda x: x[0])
    for child in costed_children:
        if child not in population:
            population.append(individual)
            population.remove(costed_population[0][1])
            break

