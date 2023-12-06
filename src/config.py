popSize = 100 #400
maxGen = 50  #200
pr = 0.005
pc = 0.8
pm = 0.1
latex_export = True

# Learning variables
possible_pc_values = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
pc_interval = 0.05
possible_pm_values = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19]
pm_interval = 0.02
states = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
states_interval = 0.05
# epsilon value for epsilon-greedy approach
epsilon = 0.85
# Weights for reward calc
wc = 0.5
wm = 0.5
# Weights for State calculation
w1 = 0.35
w2 = 0.35
w3 = 0.3
# Learning parameters
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
