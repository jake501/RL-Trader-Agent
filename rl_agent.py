import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class ActorCritic(nn.Module):
    def __init__(self, input_size, output_size):
        super(ActorCritic, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc_actor = nn.Linear(64, output_size)
        self.fc_critic = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        actor_output = torch.softmax(self.fc_actor(x), dim=-1)
        critic_output = self.fc_critic(x)
        return actor_output, critic_output


class RLAgent:
    def __init__(self, state_size, action_space, learning_rate=0.001, gamma=0.99, epsilon=0.2, clip_value=0.2):
        self.actor_critic = ActorCritic(state_size, len(action_space))
        self.optimizer = optim.Adam(self.actor_critic.parameters(), lr=learning_rate)
        self.loss_fn = nn.SmoothL1Loss()  # Huber loss
        self.state_size = state_size
        self.action_space = action_space
        self.gamma = gamma
        self.epsilon = epsilon
        self.clip_value = clip_value
        self.states = []
        self.actions = []
        self.rewards = []
        self.old_probs = []
        self.dones = []

    def select_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float32)
        actor_output, _ = self.actor_critic(state_tensor)
        action_probs = actor_output.detach().numpy()
        action = np.random.choice(len(action_probs), p=action_probs)
        return action, action_probs[action]

    def train(self):
        states = torch.tensor(self.states, dtype=torch.float32)
        actions = torch.tensor(self.actions, dtype=torch.int64)
        old_probs = torch.tensor(self.old_probs, dtype=torch.float32)
        rewards = torch.tensor(self.rewards, dtype=torch.float32)
        dones = torch.tensor(self.dones, dtype=torch.float32)

        _, critic_values = self.actor_critic(states)

        td_targets = rewards + self.gamma * critic_values.squeeze() * (1 - dones)
        advantages = td_targets - critic_values.detach().squeeze()

        _, actor_output = self.actor_critic(states)
        probs = torch.gather(actor_output, 1, actions.unsqueeze(1))
        ratio = probs / old_probs

        actor_loss = -torch.min(ratio * advantages, torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages)
        critic_loss = self.loss_fn(critic_values.squeeze(), td_targets)
        total_loss = actor_loss.mean() + critic_loss.mean()

        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

        self.states = []
        self.actions = []
        self.rewards = []
        self.old_probs = []
        self.dones = []

    def remember(self, state, action, reward, old_prob, done):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.old_probs.append(old_prob)
        self.dones.append(done)
