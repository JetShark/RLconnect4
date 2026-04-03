# Connect 4 RL Project Todo

## How to Use This Todo

Work phase by phase. Do not start the next phase until the validation items for the current phase are complete.

## Phase 0: Project Definition

- [x] Confirm the project topic is reinforcement learning for game strategy using Connect 4.
- [x] Confirm the tutorial goal: show how an RL agent can learn Connect 4 through interaction, reward, and policy improvement.
- [x] Confirm the required deliverable: a 6 to 8 minute tutorial video link that explains the RL project clearly.
- [x] Confirm the supporting deliverables: Python simulator, rule-validation tests, Gymnasium environment, Jupyter notebook, and optionally a web demo, repository, slides, or diagrams.
- [x] Decide what the minimum successful demo looks like for the assignment.
- [x] Decide what stretch goals are optional and can be dropped if time runs short.

### Validation

- [x] There is a one-paragraph project summary that explains the problem, the RL angle, and the planned demo.
- [x] There is a written scope boundary that separates must-have work from bonus work.
- [x] The must-have scope can satisfy the assignment even if the web demo is not completed.

## Phase 1: Game Rules and Core Design

- [x] Write down the exact Connect 4 rules the simulator must enforce.
- [x] Define the board size as 6 rows by 7 columns.
- [x] Define how players are represented internally.
- [x] Define how empty cells are represented.
- [x] Decide how to track the current player, terminal state, and winner.
- [x] Define what counts as a legal move.
- [x] Define what counts as an illegal move.
- [x] Define the terminal conditions: win and draw.
- [x] Decide how no further moves will be blocked after game end.
- [x] Define the minimal simulator API before writing code.

### Validation

- [x] There is a written rules section that covers move logic, win conditions, draw conditions, and illegal moves.
- [x] There is a written API outline listing reset, legal actions, apply move, win check, draw check, and state access.

## Phase 2: Simulator Implementation Plan

- [x] Choose the board representation format for the Python simulator.
- [x] Choose the state representation format that will also be easy to expose to Gymnasium later.
- [x] Decide whether the simulator will use a class-based design, function-based design, or a small hybrid.
- [x] Plan helper methods for dropping pieces, checking bounds, checking legal columns, and checking four-in-a-row.
- [x] Plan a text-based render format for debugging and notebook display.
- [x] Plan how errors or invalid actions will be reported.

### Validation

- [x] The simulator design is simple enough that the same core logic can be reused by tests, notebook training, and the web demo.
- [x] The planned board format can be easily converted into a NumPy array or Gymnasium observation.

## Phase 3: Rule Validation Test Plan

- [x] Create a list of required tests before implementing RL.
- [x] Add a test for empty board initialization.
- [x] Add a test for valid piece drop behavior.
- [x] Add a test for alternating turns.
- [x] Add a test for rejecting moves in full columns.
- [x] Add a test for horizontal win detection.
- [x] Add a test for vertical win detection.
- [x] Add a test for both diagonal win directions.
- [x] Add a test for draw detection.
- [x] Add a test that no moves are accepted after terminal state.
- [x] Add a test for reset behavior.

### Validation

- [x] Every written game rule from Phase 1 maps to at least one planned test.
- [x] There are no major rule cases left untested.

## Phase 4: Implement and Verify the Pure Python Simulator

- [x] Implement board creation and reset.
- [x] Implement current-player tracking.
- [x] Implement legal action detection.
- [x] Implement move application with gravity behavior.
- [x] Implement illegal move handling.
- [x] Implement horizontal win detection.
- [x] Implement vertical win detection.
- [x] Implement diagonal win detection.
- [x] Implement draw detection.
- [x] Implement terminal-state blocking.
- [x] Implement a simple board render for debugging.
- [x] Run the rule-validation tests.
- [x] Fix any failing simulator behavior before moving on.

### Validation

- [x] All simulator tests pass.
- [x] Manual spot checks confirm the board behaves like classic Connect 4.
- [x] The simulator can play a full game from start to finish without invalid state transitions.

## Phase 5: RL Problem Definition

- [x] Write the RL mapping for Connect 4: agent, environment, state, action, reward, and policy.
- [x] Decide what the observation includes.
- [x] Decide whether current-player information will be included directly or encoded into the board representation.
- [x] Decide what action values correspond to the seven columns.
- [x] Decide how illegal moves will be handled during training.
- [x] Write the first reward design.
- [x] Decide what opponent the first training run will use.

### Validation

- [x] The RL definitions are specific enough to explain in the video without ambiguity.
- [x] The reward design does not conflict with the actual game rules.
- [x] The first opponent strategy is simple enough to train against and explain clearly.

## Phase 6: Gymnasium Environment Design

- [x] Define the Gymnasium action space.
- [x] Define the Gymnasium observation space.
- [x] Plan the `reset()` behavior.
- [x] Plan the `step()` behavior.
- [x] Decide what goes into `info` for debugging and evaluation.
- [x] Decide how reward, termination, and truncation will be reported.
- [x] Decide whether action masking will be used now or deferred as a stretch goal.

### Validation

- [x] The environment design matches Gymnasium expectations.
- [x] The environment does not duplicate game rules outside the simulator.
- [x] Illegal action handling is consistent and documented.

## Phase 7: Implement and Validate the Gymnasium Environment

- [x] Wrap the simulator inside a custom Gymnasium environment.
- [x] Implement `reset()`.
- [x] Implement `step()`.
- [x] Return observations in the planned format.
- [x] Return rewards in the planned format.
- [x] Return termination and truncation flags correctly.
- [x] Include useful `info` fields for debugging.
- [x] Run environment smoke tests.
- [x] Run short manual episodes to inspect transitions.

### Validation

- [x] The environment resets without error.
- [x] A valid action updates the board correctly.
- [x] Invalid actions are handled exactly as designed.
- [x] Win, loss, and draw states produce the expected outputs.
- [x] The environment can run for multiple episodes in a row without leaking state.

## Phase 8: Notebook Structure and Training Setup

- [x] Create the Jupyter notebook structure for the tutorial.
- [x] Add a short markdown introduction to the project.
- [x] Add a section explaining the RL formulation.
- [x] Add a section walking through the simulator.
- [x] Add a section walking through the Gymnasium environment.
- [x] Add a section for training configuration.
- [x] Add a section for evaluation and plots.
- [x] Add a section for limitations and future directions.
- [x] Decide what Python libraries will be used for training and visualization.
- [x] Decide what seed or reproducibility settings will be recorded.

### Validation

- [x] The notebook tells a coherent story from problem definition to results.
- [x] The notebook sections match the parts of the assignment video.
- [x] The notebook can be used as both a development artifact and a presentation artifact.

## Phase 9: Initial Training Run

- [x] Choose a first RL algorithm that is realistic for the assignment scope.
- [x] Set a small baseline training configuration.
- [x] Train against a random opponent first.
- [x] Record reward per episode or per evaluation window.
- [x] Record win rate against the chosen opponent.
- [x] Record draw rate and illegal move count if relevant.
- [x] Save a trained model checkpoint if supported by the chosen stack.
- [x] Log enough outputs to explain progress in the video.

### Validation

- [x] The training run completes end to end.
- [x] There is at least one quantitative sign of learning or non-learning.
- [x] The outputs are clear enough to show in the notebook and video.

## Phase 10: Evaluation and Behavior Review

- [x] Run evaluation games after training.
- [x] Compare trained behavior against the random baseline.
- [x] Capture example board states from wins, losses, and draws.
- [x] Identify at least one success pattern the agent learned.
- [x] Identify at least one weakness or failure mode.
- [x] Decide whether another training pass is worthwhile.

### Validation

- [x] There is evidence for what the agent learned.
- [x] There is evidence for what the agent still does poorly.
- [x] The evaluation results are simple enough to explain in under one minute of video time.

## Phase 11: Optional Web Demo Planning

- [x] Decide whether the demo will be human-vs-agent, agent-vs-agent, or both.
- [x] Decide how the frontend will send moves to the Python backend.
- [x] Decide how the frontend will receive board updates and end-state results.
- [x] Decide how the UI will prevent illegal moves.
- [x] Decide how the UI will display current player, winner, and draw outcomes.
- [x] Decide whether the interface needs model selection or reset controls.

### Validation

- [x] The web demo only presents the game and does not reimplement game logic.
- [x] The integration path from frontend to Python backend is simple and explainable.
- [x] The project still has a complete notebook-based demonstration path if the web demo is dropped.

## Phase 12: Optional Web Demo Implementation and Validation

- [ ] Build a minimal board display.
- [ ] Add column selection input.
- [ ] Connect frontend moves to backend simulator or environment logic.
- [ ] Show the agent move response.
- [ ] Show game-end messages.
- [ ] Add reset functionality.
- [ ] Prevent illegal interactions in the UI.
- [ ] Run full demo games manually.

### Validation

- [ ] A human can complete a full game against the agent in the browser.
- [ ] The UI state remains consistent with backend game state.
- [ ] Game outcomes shown in the UI match the simulator results.

## Phase 13: Video Preparation

- [ ] Write a short spoken outline for the 6 to 8 minute tutorial.
- [ ] Prepare a 1-minute problem introduction.
- [ ] Prepare a 1 to 2 minute RL concepts explanation.
- [ ] Prepare a 2 to 3 minute method walkthrough.
- [ ] Prepare a 1-minute results section.
- [ ] Prepare a short challenges and future directions section.
- [ ] Capture notebook visuals.
- [ ] Capture gameplay visuals from the notebook or web demo.
- [ ] Prepare one chart that shows training progress.
- [ ] Prepare one diagram that shows the RL loop.
- [ ] Do one rehearsal run to verify timing.
- [ ] Check that visuals are readable at normal playback size.
- [ ] Check that narration is clear and easy to follow.

### Validation

- [ ] Every assignment section has a matching visual or demonstration.
- [ ] The explanation uses correct RL terminology.
- [ ] The planned runtime fits within the target video length.
- [ ] The visuals are readable without pausing constantly.
- [ ] The narration and flow are clear enough for a viewer who has not seen the code.

## Phase 14: Final Review

- [ ] Confirm the simulator rules are correct.
- [ ] Confirm tests still pass.
- [ ] Confirm the Gymnasium environment still behaves correctly.
- [ ] Confirm the notebook runs in order.
- [ ] Confirm there is at least one working demonstration path for the video: notebook or web demo.
- [ ] If the web demo is included, confirm it works for the recorded demonstration path.
- [ ] Confirm the video clearly explains agent, environment, state, action, reward, and policy.
- [ ] Confirm the final deliverables are organized and ready to share.

### Final Validation Gate

- [ ] The project can be explained clearly as an applied RL system.
- [ ] The technical pieces support each other cleanly: simulator, tests, environment, notebook, and demo.
- [ ] The tutorial demonstrates both implementation understanding and RL concepts, matching the assignment rubric.

## Phase 15: Recording and Submission

- [ ] Record the final tutorial video.
- [ ] Export the final video in a shareable format.
- [ ] Upload the video to YouTube, Vimeo, Loom, or Google Drive.
- [ ] Verify that the uploaded video plays correctly from start to finish.
- [ ] Confirm the share settings allow the instructor to view it.
- [ ] Copy the final video link into the submission notes.
- [ ] Decide whether to include optional supporting material such as the notebook, repository, or slides.
- [ ] Verify that every submitted link opens correctly.

### Validation

- [ ] A valid video link exists and is ready to submit.
- [ ] The uploaded video matches the final reviewed version.
- [ ] Any optional supporting materials are organized and accessible.

## Suggested Build Order

1. Finish project definition and scope.
2. Lock down the rules and simulator design.
3. Write rule-validation tests.
4. Implement the pure Python simulator.
5. Wrap it as a Gymnasium environment.
6. Build the notebook and run initial training.
7. Evaluate the trained agent.
8. Build the web demo.
9. Record visuals and produce the tutorial video.