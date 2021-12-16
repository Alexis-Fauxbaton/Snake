import numpy as np
import random
import time


class Q_learning:
    """
    Using eps-greedy method
    """
    def __init__(self, states, actions, max_episodes=10000, max_steps=1000, learning_rate=0.001, epsilon_decay=0.01, e_greedy=1, discount_factor=0.9):
        self.actions = actions
        self.actions_list = [i for i in range(actions)]
        self.states = states
        self.q_table = np.zeros((states, actions))
        self.max_episodes = max_episodes
        self.max_steps = max_steps
        self.learning_rate = learning_rate
        self.epsilon_decay = epsilon_decay
        self.e_greedy = e_greedy
        self.discount_factor = discount_factor
        self.rew_list = []

    def choose_action(self, state):
        if random.uniform(0, 1) < self.e_greedy:
            return random.choice(self.actions_list)
        else:
            return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state):
        self.q_table[state, action] = (1 - self.learning_rate) * self.q_table[state, action] + self.learning_rate * (reward + self.discount_factor * np.max(self.q_table[next_state, :]) - self.q_table[state,action])

    def update_epsilon(self):
        self.e_greedy = (1 - self.epsilon_decay) * self.e_greedy

