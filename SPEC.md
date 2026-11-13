# Rock, Paper, Scissors

## RPS-001: Play a round

**Purpose:** one person plays a quick round against the computer.

- Choose rock, paper, or scissors. The computer chooses one move for that round.
- Display both choices and the result: **You win!**, **Computer wins**, or **It’s a tie**.
- Choosing again starts an independent round. No score or saved history.
- Keep the supplied interface and server. Name/color changes can wait until the rules work.

### Expected results

Results are from the **player’s perspective**. `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`. Inputs are the lowercase moves below; the supplied server rejects other choices.

| Player | Computer | Expected return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Agreed plan

- Implement `determine_winner(player, computer)` for all nine expected results above. Keep the supplied interface and server, display both choices and the correct result, and allow another independent round. No score or saved history; scoring is a later feature.
- Predicted matchup: the player chooses Rock and the computer chooses Paper. Paper beats Rock, so return `lose` and display **Computer wins**. This valid losing round is a positive test case.
- Add nine explicit unit cases with literal expected results and a submitted-round integration test using the real rules with a fixed computer choice in `tests/test_game.py`.
- Keep the supplied missing/unsupported-input checks: reject invalid moves such as `lizard` with HTTP 400 and a helpful message before calling the rules.
- Add a real-browser round and replay in `tests/e2e/test_round.py`, fixing only the computer choice and using the real rules and HTTP requests.
- Run `.venv/bin/python check.py`, review the diff, discuss the test for Rock versus Paper, and have the student play and describe a round before recording feature completion. Keep meaningful checks intact.

### Checks

Before coding, agree this small test plan with AI:

| Level | Cases and evidence |
| --- | --- |
| Unit — positive | All nine literal expected results above, including valid losses and ties. |
| Integration — positive | A submitted round uses the real rule function and displays both choices and the correct result. Fix the computer choice for the test. |
| Integration — negative | Reuse supplied missing/unsupported-move tests: HTTP 400 and a helpful explanation, without calling the rules. A crash is not the intended result. |
| E2E — positive | Add a real-browser round and replay in tests/e2e/test_round.py using the supplied live_server/page fixtures. Fix only the computer choice; use real rules and real HTTP. |

Use `unit`, `integration`, and `e2e` pytest markers. Run `.venv/bin/python check.py` for Black, Pylint, fast tests, and browser checks; then review the diff. Keep shared settings and meaningful assertions intact. The student still plays, inspects a rule and its test, and gives feedback. Browser automation does not establish every aspect of usability or application performance.

### Work record

- Issue: https://github.com/timothyson39-wq/my-rps/issues/1
- Pull request / CI: [PR #2](https://github.com/timothyson39-wq/my-rps/pull/2) and [Python checks run](https://github.com/timothyson39-wq/my-rps/actions/runs/43445679579).
- Implementation: [Winner rules](game.py) implement all nine outcomes for independent rounds. [Rule and request tests](tests/test_game.py) cover the expected results and a real submitted loss; [browser round and replay](tests/e2e/test_round.py) use real rules.
- Checks: `.venv/bin/python check.py` passed Black, Pylint, 23 non-browser tests, and 6 Chromium tests. Reviewed the diff and new test files against the spec; `git diff --check` passed. Existing missing/invalid-input checks remain intact.
- Student review: after clarification that the displayed Python snippet was test code rather than a Bash command, the student explained that returning `win` for Rock versus Paper would fail the expected `lose` assertion.
- Browser observation: the student chose Scissors, the computer chose Rock, and the page displayed Computer wins with “A rematch is one click away.” The student explained that Rock beats Scissors. The student also confirmed that Tab and Enter play another round and display its result.
