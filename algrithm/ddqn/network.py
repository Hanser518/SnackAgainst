import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn


class Network(nn.Module):
    def __init__(self, input_shape, num_actions):
        """
        Args:
            input_shape: tuple (channels, height, width)
            num_actions: int, 动作空间大小
        """
        super().__init__()
        # 卷积层
        self.conv = nn.Sequential(
            nn.Conv2d(input_shape[0], 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )
        self.adaptive = nn.AdaptiveAvgPool2d((16, 16))

        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(64 * 16 * 16, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_actions)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.adaptive(x)
        x = x.reshape(x.size(0), -1)  # 保持batch维度
        return self.fc(x)

class ReplayBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        return states, actions, rewards, next_states, dones

    def clear(self):
        self.buffer.clear()

    def __len__(self):
        return len(self.buffer)
