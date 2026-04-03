const state = {
    sessionId: null,
    snapshot: null,
};

const boardElement = document.getElementById("board");
const columnControlsElement = document.getElementById("column-controls");
const statusMessageElement = document.getElementById("status-message");
const turnIndicatorElement = document.getElementById("turn-indicator");
const outcomeIndicatorElement = document.getElementById("outcome-indicator");
const newGameButtonElement = document.getElementById("new-game-button");

newGameButtonElement.addEventListener("click", startNewGame);

document.addEventListener("DOMContentLoaded", () => {
    startNewGame();
});

async function startNewGame() {
    const response = await fetch("/api/new-game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });
    const payload = await response.json();
    state.sessionId = payload.session_id;
    updateView(payload);
}

async function submitMove(column) {
    const response = await fetch("/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: state.sessionId, column }),
    });

    const payload = await response.json();
    if (!response.ok) {
        statusMessageElement.textContent = payload.error || "Move failed.";
        return;
    }

    updateView(payload);
}

function updateView(snapshot) {
    state.snapshot = snapshot;
    statusMessageElement.textContent = snapshot.message;
    turnIndicatorElement.textContent = snapshot.is_terminal
        ? "Finished"
        : snapshot.current_player === snapshot.human_player
            ? "Human"
            : "Agent";

    outcomeIndicatorElement.textContent = buildOutcomeLabel(snapshot);
    renderColumnControls(snapshot);
    renderBoard(snapshot.board, snapshot);
}

function buildOutcomeLabel(snapshot) {
    if (snapshot.is_draw) {
        return "Draw";
    }
    if (snapshot.winner === snapshot.human_player) {
        return "Human win";
    }
    if (snapshot.winner === snapshot.agent_player) {
        return "Agent win";
    }
    return "In progress";
}

function renderColumnControls(snapshot) {
    columnControlsElement.innerHTML = "";

    for (let column = 0; column < 7; column += 1) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "column-button";
        button.textContent = `Drop ${column}`;
        button.disabled = snapshot.is_terminal || !snapshot.legal_actions.includes(column);
        button.addEventListener("click", () => submitMove(column));
        columnControlsElement.appendChild(button);
    }
}

function renderBoard(board, snapshot) {
    boardElement.innerHTML = "";

    for (const row of board) {
        for (const cell of row) {
            const cellElement = document.createElement("div");
            cellElement.className = buildCellClass(cell, snapshot);
            boardElement.appendChild(cellElement);
        }
    }
}

function buildCellClass(cell, snapshot) {
    if (cell === snapshot.human_player) {
        return "cell human";
    }
    if (cell === snapshot.agent_player) {
        return "cell agent";
    }
    return "cell";
}