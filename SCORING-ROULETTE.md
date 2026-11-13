# Running scores and Roulette Mode

Issue: [#3](https://github.com/timothyson39-wq/my-rps/issues/3)

## Agreed behavior

- Classic Mode keeps its existing move buttons. Each mode has its own player and computer scores, starting at 0–0. A win adds one point to the winner. A tie leaves both scores unchanged. There is no target score.
- Refreshing preserves the score within the current browser session and never awards the same point twice. Persistence across browser sessions is outside the feature scope.
- Reset Score clears the current mode’s scores and last round’s moves and result.
- Switching away from a mode with a nonzero score prompts: “The score will be reset. Will you continue?” Continue clears the mode being left and switches modes. Cancel preserves the current mode, scores, and last round. At 0–0, switching needs no prompt.
- In Roulette Mode, Spin starts one wheel for the player. Stop reveals the player’s random move, then the same wheel spins for the computer and stops automatically. The two moves are selected independently, so they can match. Once both moves are revealed, apply the Classic rules and score the round once.

## Planned checks

- A player win increments the player’s score. With the score at 2–1, Rock against Paper makes it 2–2. A tie keeps it at 2–2.
- Refresh preserves the score without awarding a second point. Reset Score returns the current mode to 0–0 and clears the last round.
- Check mode switching at 0–0 and both Continue and Cancel at a nonzero score. Confirm Continue resets only the mode being left.
- In Roulette Mode, verify the player stops the first spin and the computer’s spin stops automatically. Verify both moves, the rule-based result, and that the score updates once after both moves are revealed.

## Classic scoring verification

- `.venv/bin/python check.py` passed formatting, linting, 23 non-browser tests, and 7 Chromium tests. The [Classic scoring browser test](tests/e2e/test_classic_score.py) covers both winners, ties, refresh, and reset.
- In the browser, Paper beat the computer’s Rock and raised the score to 1–0. Refresh preserved 1–0. Reset Score returned it to 0–0 and cleared the round.

## Roulette verification

- The full `.venv/bin/python check.py` run passed formatting, linting, 23 non-browser tests, and 8 Chromium tests. The [Roulette browser test](tests/e2e/test_roulette.py) covers the two spins, scoring, refresh, and the mode switch prompt.
- In the browser, the player's Paper beat the computer's Rock and raised the Roulette score to 1–0. Cancel kept Roulette selected and preserved the score and round. Continue opened Classic at 0–0. Switching back to Roulette showed 0–0 without a prompt.
