import unittest

import numpy as np

from connect4 import Connect4Game
from connect4_env import Connect4Env


def first_legal_opponent(game: Connect4Game, _rng: np.random.Generator) -> int:
    return game.get_legal_actions()[0]


class Connect4EnvTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = Connect4Env(opponent_policy=first_legal_opponent)

    def test_reset_returns_initial_observation_and_info(self) -> None:
        observation, info = self.env.reset(seed=7)

        self.assertEqual(observation["board"].shape, (Connect4Game.ROWS, Connect4Game.COLUMNS))
        self.assertEqual(observation["board"].dtype, np.int8)
        self.assertTrue(np.all(observation["board"] == Connect4Game.EMPTY))
        self.assertEqual(observation["current_player"], Connect4Game.PLAYER_ONE)
        self.assertEqual(info["legal_actions"], list(range(Connect4Game.COLUMNS)))
        self.assertIsNone(info["winner"])
        self.assertFalse(info["is_draw"])
        self.assertIsNone(info["last_move"])
        self.assertFalse(info["invalid_action"])
        self.assertIsNone(info["opponent_action"])

    def test_valid_action_updates_board_and_runs_opponent_turn(self) -> None:
        self.env.reset(seed=3)

        observation, reward, terminated, truncated, info = self.env.step(3)

        self.assertEqual(reward, 0.0)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertEqual(info["opponent_action"], 0)
        self.assertFalse(info["invalid_action"])
        self.assertEqual(observation["board"][5, 3], Connect4Game.PLAYER_ONE)
        self.assertEqual(observation["board"][5, 0], Connect4Game.PLAYER_TWO)
        self.assertEqual(observation["current_player"], Connect4Game.PLAYER_ONE)

    def test_invalid_action_returns_negative_terminal_transition(self) -> None:
        self.env.reset(seed=11)
        self.env.game.board = [
            [Connect4Game.PLAYER_ONE, 0, 0, 0, 0, 0, 0],
            [Connect4Game.PLAYER_TWO, 0, 0, 0, 0, 0, 0],
            [Connect4Game.PLAYER_ONE, 0, 0, 0, 0, 0, 0],
            [Connect4Game.PLAYER_TWO, 0, 0, 0, 0, 0, 0],
            [Connect4Game.PLAYER_ONE, 0, 0, 0, 0, 0, 0],
            [Connect4Game.PLAYER_TWO, 0, 0, 0, 0, 0, 0],
        ]
        self.env.game.current_player = Connect4Game.PLAYER_ONE
        self.env.game.terminal = False
        self.env.game.winner = None
        self.env.game.last_move = (0, 0)

        observation, reward, terminated, truncated, info = self.env.step(0)

        self.assertEqual(reward, -1.0)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertTrue(info["invalid_action"])
        self.assertIsNone(info["opponent_action"])
        self.assertEqual(observation["board"][0, 0], Connect4Game.PLAYER_ONE)

    def test_agent_win_returns_positive_terminal_reward(self) -> None:
        self.env.reset(seed=5)
        self.env.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 2, 2, 0],
        ]
        self.env.game.current_player = Connect4Game.PLAYER_ONE
        self.env.game.terminal = False
        self.env.game.winner = None
        self.env.game.last_move = None

        observation, reward, terminated, truncated, info = self.env.step(3)

        self.assertEqual(reward, 1.0)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertEqual(info["winner"], Connect4Game.PLAYER_ONE)
        self.assertIsNone(info["opponent_action"])
        self.assertEqual(observation["board"][5, 3], Connect4Game.PLAYER_ONE)

    def test_opponent_win_returns_negative_terminal_reward(self) -> None:
        self.env.reset(seed=13)
        self.env.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [2, 1, 1, 0, 0, 0, 0],
        ]
        self.env.game.current_player = Connect4Game.PLAYER_ONE
        self.env.game.terminal = False
        self.env.game.winner = None
        self.env.game.last_move = None

        observation, reward, terminated, truncated, info = self.env.step(6)

        self.assertEqual(reward, -1.0)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertEqual(info["winner"], Connect4Game.PLAYER_TWO)
        self.assertEqual(info["opponent_action"], 0)
        self.assertEqual(observation["board"][3, 0], Connect4Game.PLAYER_TWO)

    def test_draw_returns_zero_terminal_reward(self) -> None:
        self.env.reset(seed=17)
        self.env.game.board = [
            [2, 2, 1, 1, 2, 2, 0],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
        ]
        self.env.game.current_player = Connect4Game.PLAYER_ONE
        self.env.game.terminal = False
        self.env.game.winner = None
        self.env.game.last_move = None

        observation, reward, terminated, truncated, info = self.env.step(6)

        self.assertEqual(reward, 0.0)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertTrue(info["is_draw"])
        self.assertIsNone(info["winner"])
        self.assertEqual(observation["board"][0, 6], Connect4Game.PLAYER_ONE)

    def test_environment_can_run_multiple_episodes_without_leaking_state(self) -> None:
        first_observation, _ = self.env.reset(seed=19)
        self.env.step(2)
        second_observation, second_info = self.env.reset(seed=19)

        self.assertTrue(np.array_equal(first_observation["board"], second_observation["board"]))
        self.assertEqual(second_observation["current_player"], Connect4Game.PLAYER_ONE)
        self.assertEqual(second_info["legal_actions"], list(range(Connect4Game.COLUMNS)))
        self.assertIsNone(second_info["winner"])


if __name__ == "__main__":
    unittest.main()