# Python implementation of a genetic algorithm for FJSP along with Reinforcement Learning on GA.

Based on a paper written by Xinyu Li and Liang Gao [1] and on another paper written by .


## Code structure

The code has been designed to be read along the section 4 of the paper [1].

- Workflow of the proposed HA (4.1)
    - main.py
- Encoding and decoding (4.2)
    - encoding.py, decoding.py
- Genetic operators (4.3)
    - genetic.py
- Terminate criteria (4.5)
    - termination.py

From the paper [2].

- Defining Updation rules (3.2)
- Switching update rule condition (4.2)
    - SQ_main.py
- State, action, and reward Calculation (section 4)
    - learning.py

## Usage

To run the algorithm on the Mk02 problem from the Brandimarte data:

```
$ python3 main.py test_data/Brandimarte_Data/Text/Mk02.fjs  ## for basic GA on FJSP
$ python3 Q_main.py test_data/Brandimarte_Data/Text/Mk02.fjs ## for Q-learning on GA on FJSP
$ python3 S_main.py test_data/Brandimarte_Data/Text/Mk02.fjs ## for SARSA on GA on FJSP
$ python3 SQ_main.py test_data/Brandimarte_Data/Text/Mk02.fjs ## for SARSA and Q-learning on GA on FJSP
```

Test data can be found on [this site](http://people.idsia.ch/~monaldo/fjsp.html).

## References 

[1] Xinyu Li and Liang Gao. An effective hybrid genetic algorithm and tabu searchfor  flexible  job  shop  scheduling  problem.International  Journal  of  ProductionEconomics, 174 :93 – 110, 2016
[2] Ronghua Chen, Bo Yang, Shi Li and Shilong Wang. A self-learning genetic algorithm based on reinforcement learning for flexible job-shop scheduling problem. Computers & Industrial Engineering, 149 : 2020, 106778