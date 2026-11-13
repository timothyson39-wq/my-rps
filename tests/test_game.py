"""Real rule outcomes and a submitted round for RPS-001."""

import pytest

import app as web
from game import determine_winner


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_all_matchups(player, computer, expected):
    """Each literal spec outcome must hold from the player's perspective."""
    assert determine_winner(player, computer) == expected


@pytest.mark.integration
def test_submitted_rock_loses_to_paper(monkeypatch):
    """A real request uses the rules and displays both moves and the loss."""
    monkeypatch.setitem(web.app.config, "TESTING", True)
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    with web.app.test_client() as client:
        response = client.post("/", data={"move": "rock"})
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert 'data-outcome="lose"' in page
    assert "Computer wins" in page
    assert "You chose" in page and "Computer chose" in page
    assert 'class="choice-value">Rock ' in page
    assert 'class="choice-value">Paper ' in page
    assert "game rules not built yet" not in page
