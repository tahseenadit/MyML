import sys
import numpy as np
import math
import random
import gym


def choose_next_action(q_table, state, epsilon):
    # agent_curr_state_x should be the current row index
    # agent_curr_state_y should be the current column index

    # In the beginning we want to select action's randomly and then later we want to select the best actions.
    # Sometimes epsilon is used differently and in those case epsilon indicates the percentage of time we want
    # to select the best actions. But in those cases, there are always some percentage of chance to select
    # random actions if we do not increase epsilon. Here we will implement epsilon differently. We would like to slowly decay
    # the epsilon so that later our epsilon becomes very small and enables us to select the best action instead of a random action.
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()  # select an action randomly from possible actions
    else:
        return np.argmax(q_table[state])


def get_next_state_location(next_action_to_take):

    next_state = env.step(next_action_to_take)
    return next_state


def simulate():

    global epsilon
    for episode in range(MAX_EPISODES):

        # during each episode we need to reset the environment.
        environment = env.reset()
        # The environment stores the current observation returned from the reset function. The current observation is the current state.
        state = environment
        # We also need to reset the reward
        total_reward = 0

        for step in range(MAX_TRY):

            # User can take three actions: forward, right, left. Which action to take
            # will be selected based on the radar's observation or radar's state.
            # Select the action to take from the current state
            next_action_to_take = choose_next_action(q_table, state, epsilon)

            curr_state = state

            # the next state is radar's state after taking the action indicated by 'next_action_to_take'
            next_state = get_next_state_location(next_action_to_take)

            # Get the reward to go to that next state
            reward, done, _ = env.get_reward()
            total_reward += reward

            # Now calculate the current q-value of the current state for that 'next_action_to_take' from the current state
            current_q_value = q_table[curr_state][next_action_to_take]

            # Now in the next state, there are 3 actions. So there are 3 q-values in the next state and we know those q-values.
            # We can not say now which action will be choosen from that next state in future, but based on the current q-values
            # of the next state, we can guess what can be the maximum q-value that we can achieve in that next state in future
            # time step. Let's get that maximum q-value in the next state.

            max_achievable_q_values_in_next_state = np.max(q_table[next_state])

            # We do not want to get the full effect of that knowledge to our current state. Let's minimize the effect.

            max_achievable_q_values_in_next_state = discount_factor * max_achievable_q_values_in_next_state

            # Now, let us calculate the overall profit the agent can get by going to that next state

            profit = reward + max_achievable_q_values_in_next_state

            # Let us calculate how the profit is compared to the profit in our curent state
            temporal_difference = profit - current_q_value

            # Let us update the current state profit or in other words, q-value. We do not want to be greedy.
            # So, we will not learn 100%.
            new_q_value_of_the_current_state_for_the_next_action = current_q_value + (
                        learning_rate * temporal_difference)

            q_table[state][next_action_to_take] = new_q_value_of_the_current_state_for_the_next_action

            # Set up for the next iteration
            state = next_state

            # Draw games
            env.render()

            # When episode is done, print reward
            if done or step >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f." % (episode, step, total_reward))
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay


if __name__ == '__main__':
    env = gym.make('mycustomenv-v0')
    MAX_EPISODES = 9999
    MAX_TRY = 1000
    # Hyperparameters start
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    # discount factor for future state's q_values
    discount_factor = 0.4
    gamma = 0.6
    # Hyperparameters end
    num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
    q_table = np.zeros(num_box + (env.action_space.n,))
    simulate()

