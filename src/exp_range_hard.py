import gym
import numpy as np
import random
from typing import List


class Optimum:
    def __init__(self, mag, std, x):
        self.mag = mag
        self.std = std
        self.x = x

    def __repr__(self):
        return f'Optimum at {self.x} with m={self.mag}, std={self.std}'





class ExponentialEnv(gym.core.Env):

    action_space = gym.spaces.Box(np.zeros([1]), 10 * np.ones([1]))
    observation_space = gym.spaces.Box(np.zeros([1]), np.ones([1]))

    def __init__(self, max_turns: int = 10, steepness = 6, noise_factor = 1):
        self.done = False
        self.ctr = 0
        self.optima = []
        self.optima.append(Optimum(3*random.random(), random.random(), 10*random.random()))
        self.optima.append(Optimum(2*random.random(), random.random(), 10*random.random()))
        self.optima.append(Optimum(random.random(), random.random(), 10*random.random()))
        self.steepness = steepness

        self.noise_factor = noise_factor
        self.max_turns = max_turns

    def rwrd(self, action):
        tr = 0
        for o in self.optima:
            log_miss = self.steepness * abs(o.x - action)
            reward = o.mag * 10 ** (-log_miss / 10) * (1 + self.noise_factor * o.std * (0.5 - random.random()))
            tr += reward

        return tr

    def reset(self):
        self.done = False
        self.ctr = 0
        return self.useless_obs

    def step(self, action):
        if self.done:
            raise Exception("reset the env!")

        self.ctr += 1
        if self.ctr >= self.max_turns:
            self.done = True

        action_float =  np.squeeze(action)

        return self.useless_obs, self.rwrd(action_float), self.done, {}

    @property
    def useless_obs(self):
        return np.random.rand(1, 1)

    def render(self, mode='human'):
        pass


    def __str__(self):
        return (f"Exp range environment, steep={self.steepness}, noise={self.noise_factor} with maxima:\n" +
                '\n'.join([repr(o) for o in self.optima]) )



if __name__ == "__main__":
    import time

    env = ExponentialEnv(max_turns=20)
    done = False
    total_reward = 0
    time.sleep(0.1)
    print('Earn points by taking action as any real number between 0 and 10.')
    while not done:
        a = -float( input(f"\nStep {env.ctr + 1}/{env.max_turns}\n") )
        _, r, done, _ = env.step(a)
        total_reward += r
        print(f'you have earned {r:.3f} by taking action {-a}')

    print('Your score is:', total_reward)