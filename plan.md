# Plan for Connect 4 for Assignment 2 RL Tutorial

## Goal

Build a clear project plan for a Python-based Connect 4 reinforcement learning tutorial that starts with a rule-correct game simulator, then turns that simulator into a Gymnasium environment, uses a Jupyter notebook for training and analysis, and finishes with a simple web interface for demonstration in the assignment video.

## Recommended Project Framing

Use topic 8 from the assignment: reinforcement learning for game strategy.

Connect 4 is a good fit because:
- it has clear states, actions, rewards, and terminal conditions
- the rules are simple enough to explain in a short tutorial
- it naturally supports simulation and automated self-play
- the learned policy can be demonstrated visually in a web interface

## Step-by-Step Plan

### 1. Define the teaching objective first

Decide that the tutorial will answer one main question: how can an agent learn to play Connect 4 by interacting with an environment and improving from reward feedback?

Set the outcome for the video:
- explain Connect 4 as an RL problem
- show a valid game simulator that enforces the rules
- show how the simulator becomes a Gymnasium environment
- show notebook-based training results
- show the trained agent playing in a browser-based demo

### 2. Define the project architecture before coding

Split the future project into five parts:
- core game logic in Python
- rule validation and automated tests
- Gymnasium environment wrapper
- Jupyter notebook for training and plots
- lightweight web interface for human-vs-agent or agent-vs-agent demos

This separation keeps the design clean and makes the tutorial easier to explain.

### 3. Specify the Connect 4 game rules to enforce

Write down the exact rules the simulator must support:
- the board is 6 rows by 7 columns
- two players alternate turns
- a move drops a piece into a column, filling from the bottom upward
- a move is invalid if the selected column is full
- the game ends when a player connects four horizontally, vertically, or diagonally
- the game also ends in a draw when the board is full and no player has won
- no moves should be accepted after a terminal state

This step is important because the RL environment will only be as correct as the simulator underneath it.

### 4. Plan the board representation

Choose a simple internal representation for the board before implementation.

Recommended design decisions:
- represent the board as a 2D array or matrix with numeric values such as 0 for empty, 1 for player one, and 2 for player two
- track the current player explicitly
- track whether the game is over
- track the winner or draw outcome
- expose helper methods for legal actions, applying a move, checking victory, and resetting the game

Keep the representation easy to inspect because the notebook and web interface will both need to display it.

### 5. Plan the simulator API

Define the minimal behavior the simulator should provide.

The future Python game engine should conceptually support:
- reset the board to an initial state
- return the current board state
- list legal columns
- apply a move for the current player
- reject illegal actions cleanly
- detect wins, draws, and terminal states
- switch turns only after valid moves
- optionally render the board in text form for debugging

This makes the simulator usable both for testing and for wrapping inside Gymnasium.

### 6. Plan rule-validation tests before RL work

Before any training, validate that the classic game rules are enforced correctly.

Plan tests for at least these cases:
- empty board initializes correctly
- a piece falls to the lowest open row in a column
- turns alternate correctly after valid actions
- a full column rejects additional moves
- horizontal win detection works
- vertical win detection works
- both diagonal win directions work
- draw detection works when the board is full without a winner
- terminal games reject further actions
- board reset clears all state

This is a critical step because RL training on a broken environment produces misleading results.

### 7. Define the RL formulation in Connect 4 terms

Map the game directly to RL concepts for the tutorial.

- Agent: the automated Connect 4 player being trained
- Environment: the Connect 4 game simulator
- State: the current board plus whose turn it is
- Action: selecting one of the seven columns
- Reward: a numeric signal for win, loss, draw, illegal move, or intermediate behavior
- Policy: the strategy the agent uses to choose columns

Also plan to explain exploration vs exploitation using Connect 4 examples, such as trying new columns during training versus choosing the best-known move later.

### 8. Decide on the observation and action spaces for Gymnasium

Plan how the simulator will be exposed as a Gymnasium environment.

Recommended design:
- action space: seven discrete actions, one for each column
- observation space: the 6x7 board plus current-player information
- legal action handling: either mask invalid moves or penalize illegal actions consistently
- reset method: start a new game and return the initial observation
- step method: apply the action, update state, compute reward, and report termination or truncation

Keep the environment interface simple so it can work with standard RL tooling.

### 9. Design the reward strategy carefully

Plan the reward function before training because it drives agent behavior.

A reasonable initial reward plan is:
- positive reward for winning
- negative reward for losing
- small neutral or near-zero reward for non-terminal valid moves
- small draw reward
- negative reward for illegal moves

Note in the plan that reward design is one of the challenges to discuss in the video, because poor rewards can create bad strategies or unstable training.

### 10. Decide how the opponent will be handled

Choose a staged approach for opponents so the project stays manageable.

Recommended progression:
1. start with the agent playing against a random opponent
2. evaluate against a rule-based opponent if time allows
3. mention self-play as an extension or bonus direction

This creates a clear teaching path and avoids unnecessary complexity too early.

### 11. Plan the notebook workflow for training and explanation

Use a Jupyter notebook as the teaching artifact for the implementation section.

The notebook should be organized into planned sections:
- project overview and RL framing
- imports and setup
- simulator walkthrough
- environment walkthrough
- training configuration
- training execution
- metrics and plots
- sample game demonstrations
- discussion of limitations and next steps

This structure supports both the assignment and the final video.

### 12. Choose a realistic training scope for the tutorial

Keep the training plan small enough to finish and explain clearly.

Plan to show:
- a baseline before training
- reward or win-rate trends over time
- a few example matches after training
- at least one failure mode or imperfect behavior to keep the tutorial honest

Do not over-scope the experiment. For the assignment, a clear and understandable result is better than a highly optimized agent.

### 13. Plan what metrics to collect

Decide in advance what evidence will be shown in the video.

Recommended metrics:
- episode reward over time
- win rate against a random opponent
- draw rate
- illegal move count if applicable
- example board states or move sequences from trained play

These metrics will help explain what the agent actually learned.

### 14. Plan the web-based demo as a presentation layer

Treat the web app as a thin interface on top of the trained model and simulator.

Recommended responsibilities for the future web demo:
- render the 6x7 board clearly
- let a human click a column to make a move
- display the agent response
- prevent illegal moves in the UI
- show win, loss, or draw results
- optionally offer human-vs-agent and agent-vs-agent modes

Keep the browser interface lightweight. Its job is to demonstrate behavior clearly for the video, not to be a production application.

### 15. Plan how Python components will connect to the web demo

Before implementation, decide on a simple integration strategy.

Recommended architecture:
- keep all game logic and inference in Python
- expose a small interface that receives a board state or game session state and returns the next agent action
- use the web layer only for input, display, and calling the backend

This avoids duplicating game rules in both Python and JavaScript.

### 16. Define validation checkpoints for each phase

Set clear milestones so progress can be checked before moving on.

Checkpoint 1:
- the simulator correctly enforces all Connect 4 rules

Checkpoint 2:
- automated tests confirm valid and invalid game scenarios

Checkpoint 3:
- the Gymnasium environment resets and steps correctly

Checkpoint 4:
- notebook training runs and records usable metrics

Checkpoint 5:
- the trained agent can be demonstrated through a browser interface

Checkpoint 6:
- the final video has visuals for every assignment section

### 17. Plan the tutorial video structure around the project

Map the technical work directly to the required assignment sections.

Problem introduction:
- explain Connect 4 as a strategy game where RL can learn move selection through interaction and reward

RL concepts:
- identify agent, environment, state, action, reward, and policy using the simulator

Method or implementation:
- show the simulator design, rule checks, Gymnasium wrapper, and notebook training workflow

Results or example behavior:
- show reward or win-rate improvement and a short gameplay demo

Challenges and future directions:
- discuss reward shaping, training instability, sample efficiency, opponent quality, and self-play extensions

### 18. Plan the visuals needed for the video

List the visuals to prepare in advance:
- a static diagram of the RL loop for Connect 4
- a board diagram showing rows, columns, and valid actions
- a short snippet of simulator logic or pseudocode
- a chart of training progress
- one or two final gameplay clips from the web interface

These visuals will make the tutorial easier to follow than narration alone.

### 19. Plan a minimal deliverable and a stretch deliverable

Minimal deliverable:
- rule-correct Connect 4 simulator
- automated rule-validation tests
- Gymnasium environment
- notebook showing training and results
- simple web demo against the trained agent

Stretch deliverable:
- compare random opponent versus stronger scripted opponent
- compare two RL approaches
- add self-play discussion or implementation
- add action masking and explain why it matters

This protects the project from becoming too large while still leaving room for bonus marks.

### 20. Define the order of future implementation work

When implementation starts later, follow this order:
1. build the pure Python Connect 4 simulator
2. write and pass rule-validation tests
3. wrap the simulator in a Gymnasium environment
4. create the training notebook
5. train and evaluate the agent
6. build the web-based demo
7. record visuals and prepare the tutorial video

## Risks to Watch

- starting RL training before the game rules are fully validated
- designing rewards that encourage unnatural behavior
- making the web demo too complex
- spending too much time on agent optimization instead of tutorial clarity
- trying to explain too many RL ideas in a short video

## Suggested Final Deliverables

- a Python Connect 4 simulator with enforced rules
- tests that prove rule correctness
- a Gymnasium environment for RL training
- a Jupyter notebook showing training and results
- a browser-based demo for presentation
- a 6 to 8 minute tutorial video aligned to the assignment rubric

