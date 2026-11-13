"""Classic scores count completed rounds and survive reloads within the tab."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_classic_score_refresh_and_reset(page: Page, live_server, monkeypatch):
    """Wins score, ties do not, and refreshing cannot replay a round."""
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    page.goto(live_server)
    player = page.locator("#player-score")
    computer = page.locator("#computer-score")
    scissors = page.get_by_role("button", name="Scissors", exact=True)
    rock = page.get_by_role("button", name="Rock", exact=True)
    paper = page.get_by_role("button", name="Paper", exact=True)
    round_result = page.locator("[data-outcome]")

    expect(player).to_have_text("0")
    expect(computer).to_have_text("0")
    for score in ("1", "2"):
        scissors.click()
        expect(round_result).to_have_attribute("data-outcome", "win")
        expect(player).to_have_text(score)

    rock.click()
    expect(computer).to_have_text("1")

    # At 2–1, the player's Rock against Paper should bring the score to 2–2.
    rock.click()
    expect(round_result).to_have_attribute("data-outcome", "lose")
    expect(player).to_have_text("2")
    expect(computer).to_have_text("2")

    paper.click()
    expect(round_result).to_have_attribute("data-outcome", "tie")
    expect(player).to_have_text("2")
    expect(computer).to_have_text("2")

    rock.click()
    expect(computer).to_have_text("3")
    page.reload()
    expect(player).to_have_text("2")
    expect(computer).to_have_text("3")

    paper.click()
    expect(round_result).to_have_attribute("data-outcome", "tie")
    page.get_by_role("button", name="Reset Score").click()
    expect(player).to_have_text("0")
    expect(computer).to_have_text("0")
    expect(round_result).to_have_count(0)
    expect(page.get_by_label("This round’s choices")).to_have_count(0)
    page.reload()
    expect(player).to_have_text("0")
    expect(computer).to_have_text("0")
