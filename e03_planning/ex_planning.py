import numpy as np
import mdp as util

def print_v_func(k, v):
    if PRINTING:
        print "k={} V={}".format(k, v)


def print_simulation_step(state_old, action, state_new, reward):
    if PRINTING:
        print "s={} a={} s'={} r={}".format(state_old, action, state_new, reward)


def value_iteration(mdp, num_iterations=10):
    """
    Does value iteration on the given Markov Decision Process for given number of iterations

    :param mdp: the Markov Decision Process
    :param num_iterations: the number of iteration to compute the V-function
    :return: (v, q) = the V-function and Q-function after 'num_iterations' steps

    :type mdp: util.MarkovDecisionProcess
    :type num_iterations: int
    """
    """
     Useful functions:
      - arr = np.ones(shape)
      - arr = np.zeros(shape)
      - arr = np.empty(shape)
      - arr = np.array(list)
      - mdp.gamma
      - P(s'|s,a) = mdp.psas[s',a,s]
      - reward = mdp.ras[a,s]
      - max(arr), util.argmax(arr)
    """
    # init the q and v function as numpy array
    q = np.zeros((mdp.num_states, mdp.num_actions))
    v = np.zeros(mdp.num_states)  
    q_old = np.vstack(q)
    for k in range(num_iterations):
       print_v_func(k, v) 
       for s in range(mdp.num_states):
           for a in range(mdp.num_actions):
               ProbSum = 0
               for sp in range(mdp.num_states):
                   ProbSum += mdp.psas[sp,a,s]*max(q_old[sp,:])               
               q[s,a] = mdp.ras[a,s] + mdp.gamma*(ProbSum)
           v[s] = max(q[s,:])
       q_old = np.vstack(q)
    return v, q

def simulate(mdp, state_old, action):
    """
    Simulates a single step in the given Markov Decision Process

    :param mdp: the Markov Decision Process
    :param action: the Action to be taken
    :param state_old: the old state
    :return: (reward, state_new) = the reward for taking the action in old state and the new state you are in

    :type mdp: util.MarkovDecisionProcess
    :type action: int
    :type state_old: int
    :rtype: tuple
    """
    # this method work as is, no change required
    reward = mdp.ras[action, state_old]  # gets reward
    state_new = util.sample_multinomial(mdp.psas[:, action, state_old])  # get new state as sample s' from P(s'|a,s)
    print_simulation_step(state_old, action, state_new, reward)  # print transition and reward
    return reward, state_new


PRINTING = False  # do not print by default, please do not change this
if __name__ == '__main__':
    PRINTING = True  # enable printing
    util.random_seed()  # seed random number generator
    value_iteration(util.data.create_mdp_circle_world_one())