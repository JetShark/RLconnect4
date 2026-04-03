import unittest

from web_demo import create_app


def deterministic_agent_policy(game):
    legal_actions = game.get_legal_actions()
    return legal_actions[0], False


class WebDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(agent_policy=deterministic_agent_policy)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_index_page_renders(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Play against the trained agent", response.data)

    def test_new_game_returns_initial_state(self) -> None:
        response = self.client.post("/api/new-game")
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["current_player"], 1)
        self.assertEqual(payload["legal_actions"], [0, 1, 2, 3, 4, 5, 6])
        self.assertFalse(payload["is_terminal"])
        self.assertIsNone(payload["winner"])
        self.assertEqual(payload["message"], "Your turn. You are X and the agent is O.")

    def test_move_endpoint_applies_human_and_agent_moves(self) -> None:
        start_response = self.client.post("/api/new-game")
        session_id = start_response.get_json()["session_id"]

        response = self.client.post(
            "/api/move",
            json={"session_id": session_id, "column": 3},
        )
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["board"][5][3], 1)
        self.assertEqual(payload["board"][5][0], 2)
        self.assertEqual(payload["agent_action"], 0)
        self.assertFalse(payload["is_terminal"])

    def test_new_game_after_progress_returns_fresh_state(self) -> None:
        first_response = self.client.post("/api/new-game")
        first_session_id = first_response.get_json()["session_id"]
        self.client.post("/api/move", json={"session_id": first_session_id, "column": 3})

        second_response = self.client.post("/api/new-game")
        payload = second_response.get_json()

        self.assertNotEqual(first_session_id, payload["session_id"])
        self.assertTrue(all(cell == 0 for row in payload["board"] for cell in row))
        self.assertEqual(payload["legal_actions"], [0, 1, 2, 3, 4, 5, 6])

    def test_full_game_can_complete_via_api(self) -> None:
        response = self.client.post("/api/new-game")
        state = response.get_json()

        for _ in range(20):
            if state["is_terminal"]:
                break

            legal_actions = state["legal_actions"]
            human_action = max(action for action in legal_actions if action != 0)
            move_response = self.client.post(
                "/api/move",
                json={"session_id": state["session_id"], "column": human_action},
            )
            self.assertEqual(move_response.status_code, 200)
            state = move_response.get_json()

        self.assertTrue(state["is_terminal"])
        self.assertIn("game", state["message"].lower())


if __name__ == "__main__":
    unittest.main()