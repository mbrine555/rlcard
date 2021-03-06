import unittest
import torch
import numpy as np

from rlcard.agents.dqn_agent_pytorch import DQNAgent

class TestDQN(unittest.TestCase):

    def test_init(self):

        agent = DQNAgent(scope='dqn',
                         replay_memory_size=0,
                         replay_memory_init_size=0,
                         update_target_estimator_every=0,
                         discount_factor=0,
                         epsilon_start=0,
                         epsilon_end=0,
                         epsilon_decay_steps=0,
                         batch_size=0,
                         action_num=2,
                         state_shape=[1],
                         mlp_layers=[10,10],
                         device=torch.device('cpu'))

        self.assertEqual(agent.replay_memory_init_size, 0)
        self.assertEqual(agent.update_target_estimator_every, 0)
        self.assertEqual(agent.discount_factor, 0)
        self.assertEqual(agent.epsilon_decay_steps, 0)
        self.assertEqual(agent.batch_size, 0)
        self.assertEqual(agent.action_num, 2)

    def test_train(self):

        memory_init_size = 100
        step_num = 1500

        agent = DQNAgent(scope='dqn',
                         replay_memory_size = 500,
                         replay_memory_init_size=memory_init_size,
                         update_target_estimator_every=100,
                         state_shape=[2],
                         mlp_layers=[10,10],
                         device=torch.device('cpu'))

        predicted_action, _ = agent.eval_step({'obs': np.random.random_sample((2,)), 'legal_actions': [0, 1]})
        self.assertGreaterEqual(predicted_action, 0)
        self.assertLessEqual(predicted_action, 1)

        for _ in range(step_num):
            ts = [{'obs': np.random.random_sample((2,)), 'legal_actions': [0, 1]}, np.random.randint(2), 0, {'obs': np.random.random_sample((2,)), 'legal_actions': [0, 1]}, True]
            agent.feed(ts)
        state_dict = agent.get_state_dict()
        self.assertIsInstance(state_dict, dict)

        predicted_action = agent.step({'obs': np.random.random_sample((2,)), 'legal_actions': [0, 1]})
        self.assertGreaterEqual(predicted_action, 0)
        self.assertLessEqual(predicted_action, 1)
