# Connect 4 Reinforcement Learning Tutorial Project

## Project Summary

This project uses Connect 4 as an applied reinforcement learning example for Assignment 2. The goal is to build a rule-correct Python simulator for the game, validate that the classic rules are enforced, wrap the simulator in a Gymnasium environment, and use a Jupyter notebook to train and evaluate an automated player. The final deliverable is a 6 to 8 minute tutorial video that explains the RL problem in terms of agent, environment, state, action, reward, and policy, shows how the system is implemented, and demonstrates what the trained agent learns through notebook visuals and optionally a web-based interface.

## Assignment Framing

- Topic: reinforcement learning for game strategy
- Game: Connect 4
- Required deliverable: tutorial video link
- Supporting deliverables: Python simulator, tests, Gymnasium environment, Jupyter notebook, and optionally a web demo, repository, slides, or diagrams

## Minimum Successful Demo

The minimum successful version of this project is:

- a Python Connect 4 simulator that enforces legal moves, wins, draws, and terminal states
- automated tests that validate the core rules
- a Gymnasium environment built on top of the simulator
- a Jupyter notebook that explains the RL formulation, runs training, and shows evaluation results
- a tutorial video that uses the notebook and training outputs to explain the project clearly

This minimum scope satisfies the assignment even if the optional web demo is not completed.

## Scope Boundary

### Must-Have Scope

- define the Connect 4 RL problem clearly
- implement the core Python game simulator
- validate rule enforcement with tests
- wrap the simulator as a Gymnasium environment
- train and evaluate an agent in a Jupyter notebook
- prepare visuals that show training behavior and learned outcomes
- record and submit the tutorial video link

### Stretch Scope

- build a web-based human-versus-agent demo
- compare more than one RL algorithm
- add a stronger opponent than a random baseline
- add action masking or self-play extensions
- prepare extra slides or diagrams beyond what is needed for the video

## Recommended Build Order

1. Finalize the simulator rules and API.
2. Write the validation tests.
3. Implement the pure Python game engine.
4. Wrap it in Gymnasium.
5. Build the notebook and run training.
6. Evaluate the agent and capture visuals.
7. Build the optional web demo if time allows.
8. Record, upload, and submit the tutorial video.

## Phase 1: Game Rules and Core Design

### Connect 4 Rules the Simulator Must Enforce

- The board has 6 rows and 7 columns.
- There are two players and they alternate turns.
- Each move selects exactly one column.
- A played piece drops to the lowest empty row in the selected column.
- A move is legal only if the selected column is within bounds and not full.
- A move is illegal if the column is out of bounds, the column is full, or the game is already over.
- A player wins immediately when they create a line of four of their own pieces.
- Winning lines can be horizontal, vertical, diagonal rising, or diagonal falling.
- The game is a draw when the board is full and neither player has won.
- Once the game reaches a win or draw state, no additional moves may be applied.

### Internal State Decisions

- Board size: 6 rows by 7 columns.
- Empty cell value: 0.
- Player one value: 1.
- Player two value: 2.
- Current player: stored explicitly as either 1 or 2.
- Terminal state: stored as a boolean flag.
- Winner: stored as 1, 2, or `None`.
- Draw state: inferred when the board is full and winner is `None`, or tracked explicitly if convenient.

This representation is simple enough for pure Python logic, NumPy conversion, Gymnasium observations, and notebook visualization.

### Legal and Illegal Move Definitions

Legal move:
- the action is an integer column index in the allowed range
- the chosen column still has at least one empty cell
- the game is not already finished

Illegal move:
- the action points outside the valid column range
- the chosen column is already full
- a move is attempted after a win or draw has already been reached

### Terminal Conditions

- Win: the active player forms four connected pieces in a row after a valid move.
- Draw: the board becomes full without any player forming four in a row.
- Terminal blocking: after either condition is reached, the simulator must reject any later move attempts.

### Minimal Simulator API Outline

The first Python simulator should expose a small, stable interface:

- `reset()`
Resets the game to the initial empty board, sets player one as the current player, clears terminal state, and clears winner information.

- `get_board()`
Returns the current 6 by 7 board state.

- `get_current_player()`
Returns the active player identifier.

- `get_legal_actions()`
Returns the list of columns that can still accept a piece.

- `apply_move(column)`
Attempts to drop a piece into the specified column, updates the board, checks win or draw conditions, blocks illegal moves, and changes turns only after a valid non-terminal move.

- `check_winner()`
Returns the winner if one exists, otherwise `None`.

- `is_draw()`
Returns whether the current position is a draw.

- `is_terminal()`
Returns whether the game is finished by win or draw.

- `render()`
Returns or prints a simple human-readable board view for debugging and notebook display.

### Phase 1 Exit Criteria

Phase 1 is complete when:

- the rules are documented clearly enough to turn directly into tests
- the board and player representation are fixed
- legal and illegal actions are unambiguous
- win, draw, and post-game behavior are defined
- the first simulator API is stable enough to implement without redesigning core behavior

## Phase 2: Simulator Implementation Plan

### Board Representation Format

The simulator should store the board as a 6 by 7 two-dimensional structure with integer values.

Recommended format:
- use a list of 6 rows, where each row contains 7 integers
- use `0` for empty cells
- use `1` for player one pieces
- use `2` for player two pieces

This format is simple to inspect in Python, straightforward to print for debugging, and easy to convert into a NumPy array later.

### State Representation Format

The simulator state should include:

- `board`: the 6 by 7 grid
- `current_player`: the active player identifier
- `is_terminal`: whether the game is over
- `winner`: the winning player or `None`
- `last_move`: the most recent row and column if available

This state is easy to expose to Gymnasium because the board can become the base observation and the additional metadata can be carried in `info` or encoded later if needed.

### Simulator Structure Choice

Use a small class-based design.

Recommended approach:
- one `Connect4Game` class owns the board and state
- methods handle reset, legal actions, move application, terminal checks, and rendering
- internal helper methods handle repeated logic such as finding the landing row and checking four-in-a-row

This is the cleanest option because it keeps state transitions together and makes the same object reusable in tests, notebook experiments, Gymnasium wrapping, and a future demo interface.

### Planned Helper Methods

The simulator should be built around a few focused helpers:

- `reset()`
Creates a fresh board and resets all game state.

- `get_legal_actions()`
Returns the columns whose top cell is still empty.

- `_is_in_bounds(row, column)`
Checks whether a board coordinate is valid.

- `_get_drop_row(column)`
Finds the lowest empty row in a chosen column.

- `_place_piece(row, column, player)`
Writes a player value into the board.

- `_check_direction(row, column, row_delta, column_delta, player)`
Counts connected pieces in one direction.

- `_check_win_from_position(row, column, player)`
Checks horizontal, vertical, and both diagonal lines starting from the last move.

- `_is_board_full()`
Checks whether any legal actions remain.

- `apply_move(column)`
Validates the action, places the piece, updates terminal status, and switches turns if appropriate.

This keeps the implementation readable and makes individual behaviors easier to test.

### Text Render Format

The first render format should be simple text output intended for debugging and notebooks.

Recommended design:
- show the board row by row from top to bottom
- render empty cells as `.`
- render player one as `X`
- render player two as `O`
- print column labels `0 1 2 3 4 5 6` below the board

Example shape:

```text
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
X O X . . . .
0 1 2 3 4 5 6
```

This format is good enough for tests, terminal output, and notebook walkthroughs.

### Invalid Action Handling Plan

The pure simulator should reject invalid actions explicitly instead of silently correcting them.

Recommended behavior:
- if a column is out of bounds, raise a clear error
- if a column is full, raise a clear error
- if a move is attempted after terminal state, raise a clear error
- do not switch players or mutate the board when an invalid move is attempted

This is the safest behavior for the core engine because it prevents hidden bugs. The Gymnasium wrapper can later translate these errors into rewards or penalties as needed for RL training.

### Reuse Plan Across the Project

The same simulator implementation should be the single source of truth for game logic.

- tests should call the simulator directly
- the Gymnasium environment should wrap the simulator rather than reimplement rules
- the notebook should use simulator renders and state inspection for explanations
- the optional web demo should call into the backend simulator rather than copying rule logic in the frontend

This avoids divergence between the training environment and the demonstration environment.

### NumPy and Gymnasium Compatibility

The chosen board format is compatible with RL tooling because:

- it can be converted directly to a NumPy array with shape `(6, 7)`
- it can be copied safely without complex object handling
- it can later be expanded to include current-player information if needed
- it works cleanly as the basis for an observation space

### Phase 2 Exit Criteria

Phase 2 is complete when:

- the board and state storage formats are fixed
- the simulator uses a single reusable class-based design
- the helper method plan is specific enough to implement directly
- the render output is simple and stable
- invalid actions have a clear handling policy
- the design supports tests, Gymnasium, notebook work, and the optional web demo without duplicating game logic

## Phase 3: Rule Validation Test Plan

### Test Strategy

The simulator should be tested before any RL work begins. The tests should validate rule enforcement, state transitions, and terminal behavior directly against the Phase 1 specification.

Recommended testing approach:
- write unit tests against the pure `Connect4Game` simulator
- keep each test focused on one rule or one state transition
- use short move sequences that are easy to read and reason about
- prefer explicit board assertions over indirect behavior when possible
- verify both the positive case and the failure case for important rules

### Required Test List

#### 1. Empty Board Initialization

Purpose:
- verify that a new game starts in a clean, valid state

Checks:
- board shape is 6 by 7
- every cell is `0`
- current player is player one
- terminal state is false
- winner is `None`
- all seven columns are legal actions

#### 2. Valid Piece Drop Behavior

Purpose:
- verify that gravity is enforced correctly

Checks:
- a piece placed in an empty column lands in the bottom row
- a second piece in the same column lands directly above the first
- no other cells change unexpectedly

#### 3. Alternating Turns

Purpose:
- verify that turn order changes only after valid moves

Checks:
- player one moves first
- after one valid move, current player becomes player two
- after the next valid move, current player becomes player one again

#### 4. Rejecting Moves in Full Columns

Purpose:
- verify that full columns cannot accept more pieces

Checks:
- after six valid moves in the same column, that column is no longer legal
- a seventh move in that column raises the expected error
- board state does not change after the invalid move attempt
- current player does not change after the invalid move attempt

#### 5. Horizontal Win Detection

Purpose:
- verify that four connected pieces in a row end the game

Checks:
- a move sequence creates four adjacent pieces for one player in the same row
- winner is set correctly
- terminal state becomes true immediately after the winning move

#### 6. Vertical Win Detection

Purpose:
- verify that vertical wins are recognized correctly

Checks:
- a move sequence creates four connected pieces for one player in the same column
- winner is set correctly
- terminal state becomes true immediately after the winning move

#### 7. Diagonal Rising Win Detection

Purpose:
- verify detection of a bottom-left to top-right diagonal

Checks:
- a legal move sequence creates a rising diagonal of four for one player
- winner is set correctly
- terminal state becomes true immediately after the winning move

#### 8. Diagonal Falling Win Detection

Purpose:
- verify detection of a top-left to bottom-right diagonal

Checks:
- a legal move sequence creates a falling diagonal of four for one player
- winner is set correctly
- terminal state becomes true immediately after the winning move

#### 9. Draw Detection

Purpose:
- verify that a full board without a winner is recognized as a draw

Checks:
- the board becomes full
- no winner is recorded
- draw state is true
- terminal state is true
- no legal actions remain

Note:
- the board pattern used for this test must avoid accidental four-in-a-row creation

#### 10. Rejecting Moves After Terminal State

Purpose:
- verify that no moves are allowed after a win or draw

Checks:
- after a winning position, any additional move raises the expected error
- after a draw position, any additional move raises the expected error
- board state does not change after the invalid move attempt

#### 11. Reset Behavior

Purpose:
- verify that reset returns the simulator to the initial state

Checks:
- after a partially played or terminal game, `reset()` clears the board
- current player returns to player one
- winner becomes `None`
- terminal state becomes false
- all seven columns become legal again

### Additional Recommended Edge Tests

These are not strictly required to finish Phase 3, but they are worth planning now:

- out-of-bounds negative column index is rejected
- out-of-bounds large column index is rejected
- legal actions shrink correctly as columns fill
- `render()` reflects board state correctly after a few moves
- `last_move` updates correctly after valid moves if tracked explicitly

### Rule-to-Test Coverage Map

- Board starts empty: covered by empty board initialization and reset behavior.
- Board is 6 by 7: covered by empty board initialization.
- Players alternate turns: covered by alternating turns.
- Pieces fall to the lowest empty row: covered by valid piece drop behavior.
- Full columns are illegal: covered by rejecting moves in full columns.
- Horizontal wins count: covered by horizontal win detection.
- Vertical wins count: covered by vertical win detection.
- Rising diagonals count: covered by diagonal rising win detection.
- Falling diagonals count: covered by diagonal falling win detection.
- Full board with no winner is a draw: covered by draw detection.
- No moves after terminal state: covered by rejecting moves after terminal state.

### Test Execution Order

Recommended order when the simulator is implemented:

1. empty board initialization
2. valid piece drop behavior
3. alternating turns
4. rejecting moves in full columns
5. horizontal win detection
6. vertical win detection
7. diagonal rising win detection
8. diagonal falling win detection
9. draw detection
10. rejecting moves after terminal state
11. reset behavior

This order starts with the most basic state behavior and moves toward more complex terminal logic.

### Phase 3 Exit Criteria

Phase 3 is complete when:

- every rule from Phase 1 has at least one planned test
- the required test list covers normal play, invalid actions, and terminal states
- the win tests include horizontal, vertical, and both diagonal patterns
- draw and reset behavior are explicitly covered
- the test plan is specific enough to implement directly in a test framework

## Phase 4: Pure Python Simulator Implementation

### Implemented Files

- `connect4.py`: contains the `Connect4Game` simulator
- `tests/test_connect4.py`: contains the rule-validation test suite

### Implemented Simulator Behavior

The pure Python simulator now includes:

- board creation and reset behavior
- explicit current-player tracking
- legal action detection based on open columns
- gravity-based move application
- invalid action rejection for out-of-bounds columns, full columns, and post-terminal moves
- horizontal, vertical, and both diagonal win detection
- draw detection when the board is full without a winner
- terminal-state blocking after win or draw
- a text render method using `.`, `X`, and `O`

### Implemented Test Coverage

The current test suite validates:

- empty board initialization
- valid piece drop behavior
- alternating turns
- rejecting full-column moves
- horizontal win detection
- vertical win detection
- diagonal rising win detection
- diagonal falling win detection
- draw detection
- rejecting moves after terminal win and terminal draw states
- out-of-bounds action rejection
- reset behavior
- render output shape and symbols

### Validation Result

Phase 4 validation was completed by running the unit test suite against the simulator implementation.

Current result:
- 13 tests run
- 13 tests passed
- 0 failures
- 0 errors

### Phase 4 Exit Criteria

Phase 4 is complete when:

- the simulator implementation matches the documented rules and API
- the validation tests pass cleanly
- invalid state transitions are blocked
- the engine is stable enough to be wrapped in Gymnasium next

## Phase 5: RL Problem Definition

### RL Mapping for Connect 4

The first reinforcement learning setup will treat the trained player as a single learning agent that acts as player one.

- Agent: the policy being trained to choose Connect 4 columns.
- Environment: the Connect 4 simulator plus the environment wrapper that applies the agent move, advances the opponent turn, and returns the resulting transition.
- State: the full simulator state consisting of the board, current player, terminal flag, winner, and last move.
- Observation: the board plus an explicit current-player indicator exposed to the agent.
- Action: one discrete choice from the seven board columns.
- Reward: a scalar returned after each environment step to reflect win, loss, draw, invalid move, or neutral progress.
- Policy: the mapping from observation to a probability distribution or preference over the seven columns.

This framing keeps the RL explanation aligned with the existing simulator while still fitting standard Gymnasium training loops.

### First Observation Design

The initial observation should include:

- the current 6 by 7 board grid
- the current player identifier

Recommended interpretation:

- board values remain `0` for empty, `1` for player one, and `2` for player two
- current player is provided separately as a scalar flag rather than hidden inside the board encoding

This choice is more explicit than trying to infer turn order from the board alone. It also keeps the observation close to the simulator's source-of-truth state, which makes debugging easier in the notebook and in early environment tests.

### Current-Player Encoding Decision

Current-player information will be included directly, not inferred indirectly from the board.

Reasoning:

- it avoids ambiguity when the environment is reset or when later variants change which side the agent controls
- it keeps the observation definition easy to explain in the video
- it reduces unnecessary preprocessing before the first training run

If a later experiment wants an agent-centric encoding such as `1`, `0`, and `-1`, that can be treated as a later optimization rather than the baseline design.

### Action Definition

The action set is fixed to the seven legal board columns:

- action `0` maps to the leftmost column
- action `1` maps to column 1
- action `2` maps to column 2
- action `3` maps to column 3
- action `4` maps to column 4
- action `5` maps to column 5
- action `6` maps to the rightmost column

The action space therefore stays stable even when some columns are temporarily full. Legality is handled by the environment, not by changing the action meanings during play.

### Illegal Move Handling During Training

Illegal actions will be handled as explicit training errors rather than silently corrected.

Baseline handling policy:

- the environment accepts actions in the fixed range `0` through `6`
- if the chosen column is full or the action is otherwise invalid, the environment returns a negative reward
- the episode terminates immediately after an illegal action
- the `info` dictionary should record that the episode ended due to an invalid move

This preserves the simulator's strict rule enforcement and gives the agent a clear signal that invalid moves are bad. Action masking can be considered later as a stretch improvement, but it will not be part of the first baseline.

### First Reward Design

The initial reward design should stay simple and easy to justify:

- win: `+1.0`
- loss: `-1.0`
- draw: `0.0`
- valid non-terminal move: `0.0`
- illegal move: `-1.0`

This reward scheme is intentionally sparse. It matches the game objective directly and avoids reward shaping that might encourage unnatural short-term behavior before the baseline system is working.

If the notebook later shows that learning is too slow or unstable, small shaping terms can be explored as a documented extension rather than mixed into the first experiment.

### First Opponent Choice

The first training run should use a random opponent that selects uniformly from the currently legal columns.

This is the right baseline because:

- it is easy to implement correctly
- it is easy to explain in the tutorial video
- it gives the agent a non-trivial but manageable learning target
- it creates a clear comparison point for later experiments against stronger opponents or self-play

### Phase 5 Exit Criteria

Phase 5 is complete when:

- the RL mapping from Connect 4 to agent, environment, state, observation, action, reward, and policy is written explicitly
- the baseline observation includes the board and a direct current-player indicator
- the action mapping is fixed to columns `0` through `6`
- illegal move handling is defined as a negative terminal outcome for the baseline environment
- the reward design is sparse and consistent with actual game outcomes
- the first opponent is fixed as a random legal-action policy

## Phase 6: Gymnasium Environment Design

### Environment Role

The Gymnasium environment should be a thin wrapper around `Connect4Game`, not a second implementation of Connect 4.

Responsibilities of the wrapper:

- reset simulator state at the start of each episode
- accept the agent action as a column index
- apply the agent move through the simulator
- apply the random opponent move when the game is still active
- translate simulator outcomes into Gymnasium observations, rewards, and flags
- expose useful episode metadata in `info`

This keeps the simulator as the single source of truth for legal moves, wins, draws, and terminal behavior.

### Action Space Definition

The baseline Gymnasium action space should be:

- `gymnasium.spaces.Discrete(7)`

Action mapping:

- `0` through `6` map directly to the seven board columns

This matches the Phase 5 action definition exactly and avoids any remapping layer between the agent and the simulator.

### Observation Space Definition

The baseline observation space should be a dictionary so the board and turn indicator stay explicit:

- `board`: `gymnasium.spaces.Box(low=0, high=2, shape=(6, 7), dtype=np.int8)`
- `current_player`: `gymnasium.spaces.Discrete(3)`

Recommended observation structure:

```python
{
	"board": np.ndarray(shape=(6, 7), dtype=np.int8),
	"current_player": 1 or 2,
}
```

Using a `Dict` observation keeps the first implementation easy to inspect and debug. It also matches the Phase 5 decision to expose current-player information directly instead of encoding it indirectly into board values.

### Reset Behavior

The environment `reset()` method should follow Gymnasium's standard contract.

Planned behavior:

- call `super().reset(seed=seed)` so seeding integrates with Gymnasium correctly
- create or reset the wrapped `Connect4Game` instance
- ensure the agent starts as player one for the baseline setup
- return the initial observation and an `info` dictionary

The initial observation should contain:

- an empty 6 by 7 board
- `current_player` set to player one

The initial `info` dictionary should include at least:

- `legal_actions`
- `winner`
- `is_draw`
- `last_move`
- `invalid_action`

At reset time these values should indicate a fresh non-terminal game.

### Step Behavior

The environment `step(action)` method should represent one full training transition from the learning agent's perspective.

Baseline step sequence:

1. validate that the episode is not already finished
2. try to apply the agent action through `Connect4Game`
3. if the action is illegal, return the unchanged observation, reward `-1.0`, `terminated=True`, `truncated=False`, and mark the transition as an invalid action in `info`
4. if the agent move wins the game, return reward `+1.0`, `terminated=True`, `truncated=False`
5. if the agent move fills the board and causes a draw, return reward `0.0`, `terminated=True`, `truncated=False`
6. if the game is still active, sample a random opponent move from the current legal actions
7. apply the opponent move through the simulator
8. if the opponent wins, return reward `-1.0`, `terminated=True`, `truncated=False`
9. if the opponent causes a draw, return reward `0.0`, `terminated=True`, `truncated=False`
10. otherwise return reward `0.0`, `terminated=False`, `truncated=False`

This design means each Gymnasium step covers one agent decision and, when appropriate, one opponent response. That produces a clean single-agent RL loop without exposing a separate multi-agent turn protocol in the baseline project.

### Info Dictionary Design

The `info` dictionary should make debugging and notebook inspection easier without changing the core observation.

Recommended fields:

- `legal_actions`: list of currently available columns after the full step completes
- `winner`: `None`, `1`, or `2`
- `is_draw`: boolean draw indicator
- `last_move`: most recent `(row, column)` tuple from the simulator
- `invalid_action`: boolean flag for illegal agent actions
- `opponent_action`: opponent column for that step, or `None` if no opponent move occurred

These fields are enough to inspect transitions, plot metrics later, and explain episode outcomes in the notebook.

### Reward, Termination, and Truncation Rules

The environment should report outcomes according to the following baseline policy:

- agent win: reward `+1.0`, `terminated=True`, `truncated=False`
- opponent win: reward `-1.0`, `terminated=True`, `truncated=False`
- draw: reward `0.0`, `terminated=True`, `truncated=False`
- illegal action: reward `-1.0`, `terminated=True`, `truncated=False`
- normal non-terminal transition: reward `0.0`, `terminated=False`, `truncated=False`

The baseline environment does not need time-limit truncation, so `truncated` should remain `False` unless a later wrapper adds an external episode cap.

### Action Masking Decision

Action masking will be deferred for the first implementation.

Baseline decision:

- do not include an action mask in the observation space yet
- do expose `legal_actions` in `info` for debugging and later extensions
- keep invalid-action penalties enabled so the baseline agent learns from mistakes directly

This keeps the first environment simple and consistent with the sparse-reward baseline. Action masking remains a valid improvement for later experiments, but it is not required to complete the initial tutorial.

### Phase 6 Exit Criteria

Phase 6 is complete when:

- the Gymnasium action space is fixed as `Discrete(7)`
- the observation space is defined explicitly as board data plus current-player information
- the `reset()` method contract is documented with initial observation and `info` contents
- the `step()` method contract is documented for valid actions, invalid actions, wins, losses, and draws
- `info` fields are defined for debugging and evaluation support
- reward, termination, and truncation behavior are fixed for the baseline environment
- action masking is explicitly deferred as a later extension rather than left ambiguous

## Phase 7: Implement and Validate the Gymnasium Environment

### Implemented Files

- `connect4_env.py`: contains the `Connect4Env` Gymnasium wrapper
- `tests/test_connect4_env.py`: contains environment validation tests
- `requirements.txt`: records the baseline Gymnasium and NumPy dependencies

### Implemented Environment Behavior

The Gymnasium environment now includes:

- a `Discrete(7)` action space mapped directly to the seven columns
- a `Dict` observation containing the board array and current-player indicator
- Gymnasium-compatible `reset()` behavior with observation and `info` output
- `step()` behavior that applies one agent move and then one opponent move when the game continues
- invalid-action handling that returns reward `-1.0` and ends the episode
- sparse terminal rewards for win, loss, and draw outcomes
- `info` fields for legal actions, winner, draw status, last move, invalid actions, and opponent action
- text rendering delegated to the underlying simulator

### Implementation Notes

The environment wraps `Connect4Game` directly and does not reimplement move legality or win detection.

The default opponent policy is random over legal actions. The implementation also allows an opponent policy to be injected when constructing `Connect4Env`, which keeps the baseline behavior unchanged while making environment tests deterministic and easier to validate.

### Implemented Validation Coverage

The environment test suite now validates:

- `reset()` returns the expected initial observation and `info`
- a valid agent action updates the board correctly and triggers the opponent turn
- invalid actions return the documented negative terminal transition
- an agent win returns reward `+1.0`
- an opponent win returns reward `-1.0`
- a draw returns reward `0.0`
- repeated resets do not leak episode state between runs

### Validation Result

Phase 7 validation was completed by running the full unit test suite for both the simulator and environment.

Current result:
- 20 tests run
- 20 tests passed
- 0 failures
- 0 errors

### Phase 7 Exit Criteria

Phase 7 is complete when:

- the simulator is wrapped inside a reusable Gymnasium environment
- `reset()` and `step()` follow the Phase 6 design
- observations, rewards, and terminal flags match the documented baseline contract
- invalid moves are handled consistently without bypassing simulator rules
- the environment can run across repeated episodes without leaking state
- automated tests cover reset behavior, normal transitions, and terminal outcomes

## Phase 8: Notebook Structure and Training Setup

### Implemented Files

- `connect4_rl_tutorial.ipynb`: contains the tutorial notebook structure and baseline setup
- `requirements.txt`: now includes the plotting dependency used by the notebook

### Implemented Notebook Structure

The notebook now includes these sections in order:

- project introduction
- RL formulation
- simulator walkthrough
- Gymnasium environment walkthrough
- training configuration
- evaluation and plot plan
- limitations and future directions

This structure matches the planned tutorial flow and can be used both as a development notebook and as the main visual artifact for the assignment video.

### Recorded Setup Decisions

The notebook now records the baseline setup choices for later training work:

- reproducibility seed: `7`
- environment libraries: `gymnasium` and `numpy`
- visualization library: `matplotlib`
- planned training stack for Phase 9: `stable-baselines3` and `torch`
- baseline opponent: random legal-action policy
- observation format: `dict(board, current_player)`
- action masking: deferred

### Validation Result

Phase 8 validation was completed by executing representative notebook cells after configuring the notebook kernel.

Validated notebook content:

- import and setup cell
- simulator walkthrough demo cell
- Gymnasium environment walkthrough demo cell
- training configuration cell
- evaluation and plotting scaffold cell

Current result:
- notebook created successfully
- notebook kernel configured successfully
- 5 representative code cells executed successfully
- no notebook setup errors encountered during validation

### Phase 8 Exit Criteria

Phase 8 is complete when:

- the notebook has a clear section structure from problem framing through later evaluation
- the notebook includes both explanatory markdown and working demonstration cells
- baseline library choices and seed settings are recorded explicitly
- the notebook is usable as both a build artifact and a presentation artifact
- later training and evaluation work can be added without restructuring the notebook

## Phase 9: Initial Training Run

### Implemented Files

- `connect4_rl_tutorial.ipynb`: now contains the baseline DQN training run, metric logging, result summary, and plots
- `requirements.txt`: now includes `stable-baselines3` and `torch` for the training stack
- `models/connect4_dqn_phase9.zip`: saved model checkpoint from the baseline training run

### Algorithm Choice

The first RL algorithm is a baseline `DQN` agent using Stable-Baselines3 with the `MultiInputPolicy` policy type.

This is a reasonable first choice because:

- the action space is discrete
- the observation is a small dictionary with board and current-player data
- DQN is easy to explain in a short tutorial compared with more advanced methods
- it is sufficient for demonstrating an end-to-end RL training loop in the assignment scope

### Baseline Training Configuration

The first training run used the following baseline setup:

- opponent: random legal-action policy
- total timesteps: `2000`
- evaluation interval: `500` timesteps
- evaluation episodes per window: `20`
- learning rate: `1e-4`
- replay buffer size: `5000`
- learning starts: `100`
- batch size: `64`
- discount factor: `0.99`
- train frequency: `4`
- target update interval: `250`
- exploration fraction: `0.3`
- final exploration epsilon: `0.05`
- seed: `7`

This configuration is intentionally small so the notebook run finishes quickly and produces usable outputs for the tutorial.

### Logged Outputs

The notebook now records:

- mean evaluation reward per evaluation window
- win rate against the random opponent
- draw rate
- invalid-action count during evaluation
- recent training reward from the monitor wrapper
- a saved model checkpoint for later evaluation

### Validation Result

Phase 9 validation was completed by running the baseline DQN training cell in the notebook end to end.

Observed metrics over the run:

- at `500` timesteps: mean evaluation reward `0.6`, win rate `0.8`, draw rate `0.0`, invalid-action count `4`
- at `1000` timesteps: mean evaluation reward `0.6`, win rate `0.8`, draw rate `0.0`, invalid-action count `4`
- at `1500` timesteps: mean evaluation reward `0.8`, win rate `0.9`, draw rate `0.0`, invalid-action count `2`
- at `2000` timesteps: mean evaluation reward `0.8`, win rate `0.9`, draw rate `0.0`, invalid-action count `2`

Interpretation:

- the run completed successfully from initialization through checkpoint saving
- the evaluation metrics show early improvement against the random opponent
- recent training reward remained noisy at `-1.0`, which is useful to discuss as a sign that learning is still unstable during exploration

### Phase 9 Exit Criteria

Phase 9 is complete when:

- a realistic first RL algorithm is chosen and run successfully
- the baseline configuration is recorded clearly enough to reproduce the run
- training is performed against the random opponent baseline
- metric outputs are logged in a form suitable for plots and video explanation
- a model checkpoint is saved for later evaluation in Phase 10
- the notebook shows at least one quantitative sign of learning or non-learning