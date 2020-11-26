import gym
from gym import spaces
import numpy as np
from myrl_gym_game.envs.myrlgame_2d import MyGame2D

class CustomEnv(gym.Env):
    def __init__(self):
        self.pygame = MyGame2D()
        self.action_space = spaces.Discrete(3)

        # Box space: let us see an example below ::

        # self.action_space = spaces.Box( np.array([-1,0,0]), np.array([+1,+1,+1]))  # steer, gas, brake.
        #
        # Box means that you are dealing with real valued quantities. The first array np.array([-1, 0, 0]
        # are the lowest accepted values, and the second np.array([+1, +1, +1]) are the highest accepted
        # values.In this case we see that we have 3 available actions:
        #
        # Steering: Real valued in [-1, 1]
        # Gas: Real valued in [0, 1]
        # Brake: Real valued in [0, 1]

        # Box space is a 2D array, we will have 5 radar and each radar has minimum distance 0 and maximum distance 10.
        # It means each radar can detect objects if it is inside 0 to 10 distance range.
        self.observation_space = spaces.Box(np.array([0,0,0,0,0]), np.array([10,10,10,10,10]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = MyGame2D()
        obs = self.pygame.observe()
        print("tuple obs :", obs)
        return obs

    def step(self, action):
        self.pygame.action_to_take(action)
        obs = self.pygame.observe()
        return obs

    def get_reward(self):
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return reward, done, {}

    def render(self, mode='human', close=False):
        self.pygame.view()
