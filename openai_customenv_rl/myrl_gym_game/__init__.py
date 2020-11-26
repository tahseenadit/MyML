from gym.envs.registration import register

register(
    id = 'mycustomenv-v0',
    entry_point = 'myrl_gym_game.envs: CustomEnv',
    max_episode_steps = 2000,
)