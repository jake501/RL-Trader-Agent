import numpy as np

import rl_agent, market_environment
from market_data import market_data, enums as ed


if __name__ == '__main__':

    # Get market data
    ticker = "TSLA"
    _, market_data = market_data.request_market_data_for_ticker(ticker, ed.Interval.ONE_DAY, ed.Period.FIVE_YR)

    # Main training loop
    env = market_environment.StockMarketEnvironment(market_data)
    state_size = 1  # Size of each state (candle)
    action_space = ["Buy", "Hold", "Sell"]
    agent = rl_agent.RLAgent(state_size, len(action_space))

    num_episodes = 1000
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        while not done:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.train(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
        print(f"Episode {episode + 1}, Total Reward: {total_reward}")

