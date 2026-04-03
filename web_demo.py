from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any, Callable
from uuid import uuid4

import numpy as np
from flask import Flask, jsonify, render_template, request
from stable_baselines3 import DQN

from connect4 import Connect4Game

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "connect4_dqn_phase9.zip"
HUMAN_PLAYER = Connect4Game.PLAYER_ONE
AGENT_PLAYER = Connect4Game.PLAYER_TWO
CENTER_COLUMN = Connect4Game.COLUMNS // 2

AgentPolicy = Callable[[Connect4Game], tuple[int, bool]]


@dataclass
class WebDemoSession:
    game: Connect4Game


def create_app(agent_policy: AgentPolicy | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SESSIONS"] = {}
    app.config["SESSION_LOCK"] = Lock()
    app.config["AGENT_POLICY"] = agent_policy or load_agent_policy(MODEL_PATH)

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.post("/api/new-game")
    def new_game() -> Any:
        session_id = str(uuid4())
        session = WebDemoSession(game=Connect4Game())

        with app.config["SESSION_LOCK"]:
            app.config["SESSIONS"][session_id] = session

        return jsonify(
            serialize_game_state(
                session_id=session_id,
                game=session.game,
                message="Your turn. You are X and the agent is O.",
                agent_action=None,
                agent_fallback_used=False,
            )
        )

    @app.post("/api/move")
    def apply_move() -> Any:
        payload = request.get_json(silent=True) or {}
        session_id = payload.get("session_id")
        column = payload.get("column")

        if not session_id:
            return jsonify({"error": "session_id is required."}), 400

        try:
            column = int(column)
        except (TypeError, ValueError):
            return jsonify({"error": "column must be an integer."}), 400

        with app.config["SESSION_LOCK"]:
            session = app.config["SESSIONS"].get(session_id)
            if session is None:
                return jsonify({"error": "Unknown game session."}), 404

            game = session.game

            if game.is_terminal():
                return jsonify({"error": "Game is already over. Start a new game."}), 400

            if game.get_current_player() != HUMAN_PLAYER:
                return jsonify({"error": "It is not the human turn."}), 400

            try:
                game.apply_move(column)
            except ValueError as error:
                return jsonify({"error": str(error)}), 400

            if game.is_terminal():
                return jsonify(
                    serialize_game_state(
                        session_id=session_id,
                        game=game,
                        message=build_terminal_message(game, human_just_moved=True),
                        agent_action=None,
                        agent_fallback_used=False,
                    )
                )

            agent_action, fallback_used = app.config["AGENT_POLICY"](game)
            game.apply_move(agent_action)

            return jsonify(
                serialize_game_state(
                    session_id=session_id,
                    game=game,
                    message=build_agent_message(
                        game=game,
                        agent_action=agent_action,
                        fallback_used=fallback_used,
                    ),
                    agent_action=agent_action,
                    agent_fallback_used=fallback_used,
                )
            )

    return app


def load_agent_policy(model_path: Path) -> AgentPolicy:
    if not model_path.exists():
        raise FileNotFoundError(f"Missing trained model at {model_path}")

    model = DQN.load(str(model_path))

    def policy(game: Connect4Game) -> tuple[int, bool]:
        legal_actions = game.get_legal_actions()
        observation = build_agent_observation(game)
        predicted_action, _ = model.predict(observation, deterministic=True)
        action = int(predicted_action)
        fallback_used = False

        if action not in legal_actions:
            fallback_used = True
            action = choose_fallback_action(legal_actions)

        return action, fallback_used

    return policy


def build_agent_observation(game: Connect4Game) -> dict[str, Any]:
    board = np.array(game.get_board(), dtype=np.int8)
    agent_view = np.zeros_like(board, dtype=np.int8)
    agent_view[board == AGENT_PLAYER] = Connect4Game.PLAYER_ONE
    agent_view[board == HUMAN_PLAYER] = Connect4Game.PLAYER_TWO
    return {
        "board": agent_view,
        "current_player": Connect4Game.PLAYER_ONE,
    }


def choose_fallback_action(legal_actions: list[int]) -> int:
    return min(legal_actions, key=lambda column: (abs(column - CENTER_COLUMN), column))


def serialize_game_state(
    *,
    session_id: str,
    game: Connect4Game,
    message: str,
    agent_action: int | None,
    agent_fallback_used: bool,
) -> dict[str, Any]:
    last_move = None
    if game.last_move is not None:
        last_move = {"row": game.last_move[0], "column": game.last_move[1]}

    return {
        "session_id": session_id,
        "board": game.get_board(),
        "current_player": game.get_current_player(),
        "legal_actions": game.get_legal_actions(),
        "winner": game.check_winner(),
        "is_draw": game.is_draw(),
        "is_terminal": game.is_terminal(),
        "last_move": last_move,
        "agent_action": agent_action,
        "agent_fallback_used": agent_fallback_used,
        "human_player": HUMAN_PLAYER,
        "agent_player": AGENT_PLAYER,
        "message": message,
    }


def build_terminal_message(game: Connect4Game, human_just_moved: bool) -> str:
    if game.is_draw():
        return "Draw. Start a new game to play again."

    if human_just_moved:
        return "You win. Start a new game to play again."

    return "Agent wins. Start a new game to play again."


def build_agent_message(
    *,
    game: Connect4Game,
    agent_action: int,
    fallback_used: bool,
) -> str:
    if game.is_terminal():
        return build_terminal_message(game, human_just_moved=False)

    if fallback_used:
        return (
            f"Agent moved in column {agent_action} using a fallback after an invalid "
            "prediction. Your turn."
        )

    return f"Agent moved in column {agent_action}. Your turn."


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000)