from __future__ import annotations

from collections.abc import Callable
from typing import Any

import gymnasium as gym
import numpy as np

from connect4 import Connect4Game


OpponentPolicy = Callable[[Connect4Game, np.random.Generator], int]


class Connect4Env(gym.Env[dict[str, Any], int]):
    metadata = {"render_modes": ["ansi"], "render_fps": 1}

    def __init__(self, opponent_policy: OpponentPolicy | None = None) -> None:
        super().__init__()
        self.game = Connect4Game()
        self.action_space = gym.spaces.Discrete(Connect4Game.COLUMNS)
        self.observation_space = gym.spaces.Dict(
            {
                "board": gym.spaces.Box(
                    low=Connect4Game.EMPTY,
                    high=Connect4Game.PLAYER_TWO,
                    shape=(Connect4Game.ROWS, Connect4Game.COLUMNS),
                    dtype=np.int8,
                ),
                "current_player": gym.spaces.Discrete(Connect4Game.PLAYER_TWO + 1),
            }
        )
        self.opponent_policy = opponent_policy or self._random_opponent_policy

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        del options
        super().reset(seed=seed)
        self.game.reset()
        return self._get_observation(), self._get_info(
            invalid_action=False,
            opponent_action=None,
        )

    def step(
        self,
        action: int,
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        if self.game.is_terminal():
            raise RuntimeError("Cannot call step() on a finished episode. Call reset().")

        try:
            self.game.apply_move(action)
        except ValueError:
            return self._handle_invalid_action()

        if self.game.is_terminal():
            return self._finalize_transition(
                reward=self._get_terminal_reward(),
                terminated=True,
                truncated=False,
                invalid_action=False,
                opponent_action=None,
            )

        opponent_action = self.opponent_policy(self.game, self.np_random)
        self.game.apply_move(opponent_action)

        return self._finalize_transition(
            reward=self._get_terminal_reward(),
            terminated=self.game.is_terminal(),
            truncated=False,
            invalid_action=False,
            opponent_action=opponent_action,
        )

    def render(self) -> str:
        return self.game.render()

    def _get_observation(self) -> dict[str, Any]:
        return {
            "board": np.array(self.game.get_board(), dtype=np.int8),
            "current_player": self.game.get_current_player(),
        }

    def _get_info(
        self,
        *,
        invalid_action: bool,
        opponent_action: int | None,
    ) -> dict[str, Any]:
        return {
            "legal_actions": self.game.get_legal_actions(),
            "winner": self.game.check_winner(),
            "is_draw": self.game.is_draw(),
            "last_move": self.game.last_move,
            "invalid_action": invalid_action,
            "opponent_action": opponent_action,
        }

    def _handle_invalid_action(
        self,
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        return self._finalize_transition(
            reward=-1.0,
            terminated=True,
            truncated=False,
            invalid_action=True,
            opponent_action=None,
        )

    def _finalize_transition(
        self,
        *,
        reward: float,
        terminated: bool,
        truncated: bool,
        invalid_action: bool,
        opponent_action: int | None,
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        return (
            self._get_observation(),
            reward,
            terminated,
            truncated,
            self._get_info(
                invalid_action=invalid_action,
                opponent_action=opponent_action,
            ),
        )

    def _get_terminal_reward(self) -> float:
        if not self.game.is_terminal():
            return 0.0
        if self.game.is_draw():
            return 0.0
        if self.game.check_winner() == Connect4Game.PLAYER_ONE:
            return 1.0
        return -1.0

    @staticmethod
    def _random_opponent_policy(
        game: Connect4Game,
        rng: np.random.Generator,
    ) -> int:
        legal_actions = game.get_legal_actions()
        return int(rng.choice(legal_actions))