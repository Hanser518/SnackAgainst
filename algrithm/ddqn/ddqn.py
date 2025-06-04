import random

import torch
from torch import optim, nn

from algrithm.ddqn.network import Network, ReplayBuffer
from environment import Environment
from model.params import Params


class DDQN:
    def __init__(self, env: Environment):
        """
        DDQN算法初始化
        :param env:
        """
        self.env = env
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # 初始化网路
        shape = env.get_state_shape()
        self.policy_net = Network(shape, 4).to(self.device)
        self.target_net = Network(shape, 4).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        # 配置模型超参数
        self.eta = 0.001
        self.gamma = 0.9
        self.batch_size = 64
        self.epsilon = 1.0
        self.epsilon_delay = 0.995
        self.target_update_freq = 10
        # 初始化经验池
        self.replay_buffer = ReplayBuffer(capacity=10000)
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.eta)

    def train(self):
        print("Start training, device=", self.device)
        for epoch in range(500):
            self.env = Environment()

            total_reward = 0

            step_score_prev = self.env.agent_link.score_record
            step_score_prev2 = self.env.against_link.score_record

            state = self.env.get_agent_state(self.env.agent_link)
            state2 = self.env.get_agent_state(self.env.against_link)

            for step in range(500):
                action = self.select_action(state)
                action2 = self.env.get_agent_action(self.env.against_link)

                self.env.set_action(self.env.agent_link, action)

                while not self.env.update_frame:
                    self.env.run()
                self.env.update_frame = False

                next_state = self.env.get_agent_state(self.env.agent_link)
                next_state2 = self.env.get_agent_state(self.env.against_link)

                step_score = self.env.get_agent_score(self.env.agent_link)
                if step_score > step_score_prev:
                    reward = 2
                elif step_score == step_score_prev:
                    reward = -1
                else:
                    reward = step_score_prev - step_score
                step_score_prev = step_score
                reward += 0.1 * self.env.get_agent_length(self.env.agent_link)
                total_reward += reward

                step_score2 = self.env.get_agent_score(self.env.against_link)
                if step_score2 > step_score_prev2:
                    reward2 = 2
                elif step_score2 == step_score_prev2:
                    reward2 = -1
                else:
                    reward2 = step_score_prev2 - step_score2
                step_score_prev2 = step_score2
                reward2 += 0.1 * self.env.get_agent_length(self.env.against_link)

                self.replay_buffer.push(state, action, reward, next_state, step_score == 100)
                self.replay_buffer.push(state2, action2, reward2, next_state2, step_score2 == 100)

                state = next_state
                state2 = next_state2

                self.update_policy_net()
                self.update_epsilon()

                if step_score == 100:
                    break

                print("", end="\r")
                print(f"Epoch: {epoch}, Step: {step}, Action: {action}, Total Reward: {total_reward :.2f}, Epsilon: {self.epsilon :.2f}", end="")

            if epoch % self.target_update_freq == 0:
                self.update_target_net()
            print()

        torch.save(self.policy_net, 'model1.pth')

    def update_policy_net(self):
        if len(self.replay_buffer) < self.batch_size:
            return None

        states, actions, rewards, next_states, dones = self.get_tensor_replaybuffer(self.batch_size)

        # 计算当前状态下选择的动作的 Q 值
        q_values = self.policy_net(states)
        predict_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        # 使用目标网络计算下一状态的最大 Q 值
        with torch.no_grad():
            next_q_values = self.target_net(next_states)
            current_q_values_next = self.policy_net(next_states)  # 使用下一状态的策略网络
            best_actions = torch.argmax(current_q_values_next, dim=1)
            next_q_values = next_q_values.gather(1, best_actions.unsqueeze(1)).squeeze(1)
        target_values = rewards + self.gamma * next_q_values * (1 - dones)

        # 计算 MSE 损失并反向传播更新策略网络
        loss = nn.MSELoss()(predict_value, target_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def update_epsilon(self):
        self.epsilon = max(0.01, self.epsilon * self.epsilon_delay)

    def select_action(self, state):
        if self.epsilon > torch.rand(1):
            action = random.randint(0, 3)
        else:
            with torch.no_grad():
                q_values = self.policy_net(self.get_trans_state(state))
            action = q_values.squeeze(0).argmax().item()
        return action

    def get_trans_state(self, state):
        state_tensor = torch.tensor(state).unsqueeze(0).to(self.device)
        return state_tensor

    def get_tensor_replaybuffer(self, batch_size):
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(batch_size)
        states = torch.tensor(states).to(self.device)
        actions = torch.tensor(actions, dtype=torch.long).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float).to(self.device)
        next_states = torch.tensor(next_states).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float).to(self.device)
        return states, actions, rewards, next_states, dones
