

class StockMarketEnvironment:
    def __init__(self, market_data):
        self.market_data = market_data
        self.current_index = 0
        self.position = "Hold"
        self.initial_balance = 10000  # Initial balance
        self.balance = self.initial_balance
        self.shares_held = 0
        self.done = False

    def reset(self):
        self.current_index = 0
        self.position = "Hold"
        self.balance = self.initial_balance
        self.shares_held = 0
        self.done = False
        return self.get_state()

    def get_state(self):
        # Return the current candle data along with position and balance
        return self.market_data[self.current_index], self.position, self.balance

    def step(self, action):
        reward = 0

        if action == "Buy":
            if self.position == "Hold":
                self.shares_held = self.balance / self.market_data[self.current_index]
                self.balance = 0
                self.position = "Buy"
        elif action == "Sell":
            if self.position == "Buy":
                self.balance = self.shares_held * self.market_data[self.current_index]
                self.shares_held = 0
                self.position = "Sell"

        self.current_index += 1
        if self.current_index >= len(self.market_data):
            self.done = True

        if self.done:
            # Calculate final reward based on final balance
            reward = self.balance - self.initial_balance

        return self.get_state(), reward, self.done
