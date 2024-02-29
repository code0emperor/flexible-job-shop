import random
import numpy as np

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
        if S_star < config.states[i]:
            return i-1
    return 19

def calculateRewards(makespans, prevMakespans):
    r_c = (np.max(makespans) - np.max(prevMakespans))/np.max(prevMakespans)
    r_m = (np.sum(makespans) - np.sum(prevMakespans))/np.sum(prevMakespans)

    return (config.wc*r_c) + (config.wm*r_m)

def qLearning(state_t, action_t, Q_values, state_t_1, reward_t_1):
    # Choosing action with epsilon-greedy
    random_num = random.uniform(0.00, 1.00)
    random_action = random.randrange(10)

    # Greedy Approach
    action_t_1 = np.argmax(Q_values[state_t_1])

    print(f"action_t_1 = {action_t_1} random_num = {random_num}, random_action = {random_action}")
    # Update Q-values using Q-Learning
    Q_values[state_t, action_t] = (1 - config.alpha) * Q_values[state_t, action_t] \
                        + config.alpha * (reward_t_1 + config.gamma * np.max(Q_values[state_t_1, :]))

    # Updating a_t+1 with epsilon greedy approach
    action_t_1 = np.argmax(Q_values[state_t_1]) if (config.epsilon >= random_num) else random_action

    return Q_values, action_t_1

def sarsa(state_t, action_t, Q_values, state_t_1, reward_t_1):
    # Choosing action with epsilon-greedy
    random_num = random.uniform(0.00, 1.00)
    random_action = random.randrange(10)

    # Epsilon-greedy Approach
    action_t_1 = np.argmax(Q_values[state_t_1]) if (config.epsilon >= random_num) else random_action

    print(f"action_t_1 = {action_t_1} random_num = {random_num}, random_action = {random_action}")
    # Update Q-values using SARSA
    Q_values[state_t, action_t] = (1 - config.alpha) * Q_values[state_t, action_t] \
                        + config.alpha * (reward_t_1 + config.gamma * Q_values[state_t_1, action_t_1])
    
    return Q_values, action_t_1

def deepQLearning():
    return None