import matplotlib.pyplot as plt
import numpy as np
from environment import environment
#import mpmath 

def eps_greedy_action(Q, s, eps):
    '''
    Implement epsilon greedy action selection:
        With Probability 1-eps select greedy action,
        otherwise select random action

    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s: state 
    :type s: int 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    
    :returns: selected action
    :rtype: int
    '''
    if np.random.rand() > eps:
        return np.argmax(Q[s, :]) 
    else:
        return np.random.randint(0, Q.shape[1]) 


def smooth(y, box_pts):
    '''
    Simple box filter implementation for smoothing
    
    :param y: discrete signal to be smoothed
    :type gamma: npumpy.ndarray
    
    :returns: smoothed signal 
    :rtype: numpy.ndarray
    '''

    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def qlearning(Q, s0, env, alpha, gamma, eps, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type eps: int
    
    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    list_of_rewards= np.zeros(episodes)

    for episode in range(episodes):
        state = s0
        #print episode
        while state != env.goal:
            action = eps_greedy_action(Q, state, eps)
            s_prime, step_reward = env.apply_action(state,action)
            Qnext = Q.item((state,action))
            Qnext = Qnext + alpha*(step_reward + gamma*(Q.item((s_prime,np.argmax(Q[s_prime])))) - Qnext)
            Q[state][action] = Qnext
            state = s_prime
            list_of_rewards[episode] += step_reward
            env.draw_statistics(episode, list_of_rewards[episode])
            
    return Q, list_of_rewards



def sarsa(Q, s0, env, alpha, gamma, eps, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    list_of_rewards= np.zeros(episodes)

    for episode in range(episodes):
        state = s0
        while state != env.goal:
            action = eps_greedy_action(Q, state, eps)
            (s_prime, step_reward) = env.apply_action(state,action)
            Qnext = Q.item((state,action))
            Qnext = Qnext + alpha*(step_reward + gamma*(Q.item((s_prime,eps_greedy_action(Q,s_prime,eps)))) - Qnext)
            Q[state][action] = Qnext
            state = s_prime
            list_of_rewards[episode] += step_reward
            env.draw_statistics(episode, list_of_rewards[episode])
            
    return Q, list_of_rewards

def qlearning_sched(Q, s0, env, alpha, gamma, eps0, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type eps: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''      
    list_of_rewards= np.zeros(episodes)

    for episode in range(episodes):
        state = s0
        eps = 0.001 + (eps0-0.001)*np.exp(-0.1*episode)
        #print episode
        while state != env.goal and list_of_rewards[episode]>-9e03:
            action = eps_greedy_action(Q, state, eps)
            (s_prime, step_reward) = env.apply_action(state,action)
            Qnext = Q.item((state,action))
            Qnext = Qnext + alpha*(step_reward + gamma*(Q.item((s_prime,np.argmax(Q[s_prime])))) - Qnext)
            Q[state][action] = Qnext
            state = s_prime
            list_of_rewards[episode] += step_reward
            env.draw_statistics(episode, list_of_rewards[episode])
            
    return Q, list_of_rewards

def sarsa_sched(Q, s0, env, alpha, gamma, eps0, episodes):
    '''
    Implementation of the Q-Learning algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param eps: epsilon for eps-greedy action selection 
    :type eps: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    list_of_rewards= np.zeros(episodes)

    for episode in range(episodes):
        state = s0
        #print episode
        eps = 0.001 + (eps0-0.001)*np.exp(-0.1*episode)
        while state != env.goal and list_of_rewards[episode]>-9e03:
            action = eps_greedy_action(Q, state, eps)
            (s_prime, step_reward) = env.apply_action(state,action)
            Qnext = Q.item((state,action))
            Qnext = Qnext + alpha*(step_reward + gamma*(Q.item((s_prime,eps_greedy_action(Q,s_prime,eps)))) - Qnext)
            Q[state][action] = Qnext
            state = s_prime
            list_of_rewards[episode] += step_reward
            env.draw_statistics(episode, list_of_rewards[episode])
            
    return Q, list_of_rewards


def rmax(Q, s0, env, alpha, gamma, episodes):
    '''
    Implementation of the rmax-like algorithm as explained in the slides
    
    :param Q: Q-function
    :type Q: numpy.ndarray
    :param s0: initial state 
    :type s0: int 
    :param env: environt 
    :type env: function 
    :param alpha: learning rate 
    :type alpha: float 
    :param gamma: discount factor 
    :type gamma: float 
    :param episodes: number of episodes 
    :type episodes: int

    :returns: Q, list of the commulative reward per episode 
    :rtype: tuple
    '''
    list_of_rewards= np.zeros(episodes)
    number_of_visits = np.zeros(Q.shape)
    r_max=0
    
    for episode in range(episodes):
        number_of_steps = 0
        state = s0
        #print episode
        while state < env.goal:
            action = np.argmax(Q[state, :])
            (s_prime, step_reward) = env.apply_action(state,action)
            if s_prime not in env.cliff:
                if number_of_visits[s_prime, action] < 100:
                    step_reward = r_max
            Qnext = Q.item((state,action))
            Qnext = Qnext + alpha*(step_reward + gamma*(Q.item((s_prime,np.argmax(Q[s_prime])))) - Qnext)
            Q[state][action] = Qnext
            state = s_prime     
            number_of_visits[s_prime,action] += 1
            list_of_rewards[episode] += step_reward
            env.draw_statistics(episode, list_of_rewards[episode])

    return Q, list_of_rewards

if __name__ == "__main__":
    env = environment()
    
    #Params
    episodes = 500
    alpha = .1
    gamma = 1.
    eps = .1 
    eps0 = 1.
    s0 = 36
    
    #Q_ql, R_ql = qlearning(np.zeros((48, 4)), s0, env, alpha, gamma, eps, episodes)
    #print("q_learning")
    #Q_sa, R_sa = sarsa(np.zeros((48, 4)), s0, env , alpha, gamma, eps, episodes)
    #print("sarsa")
    #Q_ql_sched, R_ql_sched = qlearning_sched(np.zeros((48, 4)), s0, env, alpha, gamma, eps0, episodes)
    #print("q_learning_s")
    #Q_sa_sched, R_sa_sched = sarsa_sched(np.zeros((48, 4)), s0, env , alpha, gamma, eps0, episodes)
    #print("sarsa_s")
    Q_rm, R_rm = rmax(np.zeros((48, 4)), s0, env , alpha, gamma, episodes)
    #print("r_max")
    #
    #print("Q_Learning")
    #env.print_greedy_policy(Q_ql)
    #print("Sarsa")
    #env.print_greedy_policy(Q_sa)
    #print("Q_Learning with scheduled eps")
    #env.print_greedy_policy(Q_ql_sched)
    #print("Sarsa with scheduled")
    #env.print_greedy_policy(Q_sa_sched)
    #print("Rmax")
    #env.print_greedy_policy(Q_rm)
    #
    #np.savetxt("R_ql.csv", R_ql)
    #np.savetxt("R_sa.csv", R_sa)
    #np.savetxt("R_ql_sched.csv", R_ql_sched)
    #np.savetxt("R_sa_sched.csv", R_sa_sched)
    #np.savetxt("R_rm.csv", R_rm)
    #
    #plt.plot(smooth(R_ql, 50), label='Q-Learning')
    #plt.plot(smooth(R_sa, 50), label='Sarsa')
    #plt.plot(smooth(R_ql_sched, 50), label='Q-Learning with scheduled eps')
    #plt.plot(smooth(R_sa_sched, 50), label='Sarsa with scheduled eps')
    #plt.plot(smooth(R_rm, 50), label='Rmax')
    
    #plt.legend(loc=4)
    #plt.show()
