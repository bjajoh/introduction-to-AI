# -*- coding: utf-8 -*-
import sys
import numpy as np
from vpython import *
import time


class environment:
    '''
    Cliffworld environment

    states:
        +--+--+--+--+--+--+--+--+--+--+--+--+
        | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|
        +--+--+--+--+--+--+--+--+--+--+--+--+
        |12|13|14|15|16|17|18|19|20|21|22|23|
        +--+--+--+--+--+--+--+--+--+--+--+--+
        |24|25|26|27|28|29|30|31|32|33|34|35|
        +--+--+--+--+--+--+--+--+--+--+--+--+
        |36|37|38|39|40|41|42|43|44|45|46|47|
        +--+--+--+--+--+--+--+--+--+--+--+--+
    
    actions:
        a = 0 -> top
        a = 1 -> down
        a = 2 -> left
        a = 3 -> right
    '''

    def __init__(self):
        self.height = 4
        self.width = 12 
        self.cliff = np.arange(37, 47)
        self.start = 36
        self.goal = 47
        #self.move_symbols = ['↑', '↓', '←', '→']
        self.move_symbols = ['u', 'd', 'l', 'r']
        self.r_step = -1
        self.r_cliff = -100

        scene.width = 1600
        scene.height = 900

        self.episode_text = label( pos=vec(0,5,0), text=f"Episode: {-1}", color=color.white, height=50)
        self.field       = box(pos=vec(0,0,0), length=self.width, height=2, width=self.height, color=color.green)
        self.goal_field  = box(pos=vec((self.width/2)-0.5,0,((self.height/2)+0.5)), length=1, height=2, width=1, color=color.green)
        self.goal_text   = text(text='Goal', pos=vec((self.width/2)-1,1,((self.height/2)+1.5)), align='center', height=0.5, color=color.yellow, billboard=True, emissive=True)
        self.start_field = box(pos=vec(-((self.width/2)-0.5),0,((self.height/2)+0.5)), length=1, height=2, width=1, color=color.green)
        self.start_text  = text(text='Start', pos=vec(-((self.width/2)-1),1,(self.height/2)+1.5), align='center', height=0.5, color=color.yellow, billboard=True, emissive=True)
        self.ground      = box(pos=vec(0,-.9,((self.height/2)+0.5)), length=self.width-2, height=.2, width=1, color=color.red)
        self.wall_back   = box(pos=vec(0,1,-((self.height/2)+0.5)), length=self.width, height=4, width=1, color=color.white)
        self.wall_start  = box(pos=vec(-((self.width/2)+0.5),1,0), length=1, height=4, width=self.height+2, color=color.white)
        self.wall_goal   = box(pos=vec(((self.width/2)+0.5),1,0), length=1, height=4, width=self.height+2, color=color.white)
        self.agent       = cylinder(pos=vec(-5.5,1,-1+4), radius=0.3, axis=vec(0,1.5,0), color=color.blue)

        time.sleep(15)



    def apply_action(self, s, a):
        '''
        Assumes current state s and applies action a.
        Returns resulting state and reward.
        '''

        x = s % self.width 
        y = int(s / self.width)
       
        # move
        if a == 0:
            y -= 1 
        elif a == 1:
            y += 1 
        elif a == 2:
            x -= 1
        elif a == 3:
            x += 1

        s_ = s
        r = self.r_step 

        # check if move is legal
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            s_ = y * self.width + x 

            state = s_
            state_y = int(state/self.width)
            state_x = state-self.width*state_y

            self.agent.pos = vec(state_x-5.5,1,-.5+state_y)

            if s_ == self.goal:
                #self.agent.pos = vec(11-5.5,1,-.5+3)
                self.agent.color = color.yellow
                time.sleep(0.5)
                self.agent.color = color.blue
            if s_ in self.cliff:
                self.agent.pos = vec(state_x-5.5,-1,-.5+state_y)
                self.agent.color = color.red
                time.sleep(0.5)
                self.agent.color = color.blue
                s_ = self.start
                r = self.r_cliff

            time.sleep(0.02)

        return s_, r


    def draw_statistics(self, episodes, reward):
        self.episode_text.text = f"Episode: {episodes} \n Reward: {reward}"







    
    def print_greedy_policy(self, Q):
        '''
        Evaluates policy greedily on Q and prints it.
        
        :param Q: Q-function
        :type Q: numpy.ndarray
        '''
        
        a_seq = np.argmax(Q, axis=1)

        for s in range(a_seq.shape[0]):
            if s in self.cliff:
                sys.stdout.write('#')
            else:
                sys.stdout.write(self.move_symbols[a_seq[s]])

            if (s + 1) % self.width == 0:
                print
        print
