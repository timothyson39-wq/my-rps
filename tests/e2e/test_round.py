"""A real browser plays and replays rounds using the actual game rules."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_round_and_replay(page: Page, live_server, monkeypatch):
    """Rock loses to Paper, then Scissors wins a fresh round against Paper."""
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    page.goto(live_server)
    expect(page.get_by_role("heading", name="Your next move?")).to_be_visible()
    expect(page.get_by_role("status")).to_have_count(0)

    page.get_by_role("button", name="Rock", exact=True).click()

    choices = page.get_by_label("This round’s choices").locator(".choice-value")
    expect(choices).to_have_count(2)
    expect(choices.nth(0)).to_contain_text("Rock")
    expect(choices.nth(1)).to_contain_text("Paper")
    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "lose")
    expect(
        page.get_by_role("heading", name="Computer wins", exact=True)
    ).to_be_visible()
    expect(page.get_by_role("status")).to_have_count(0)

    page.get_by_role("button", name="Scissors", exact=True).click()

    expect(choices).to_have_count(2)
    expect(choices.nth(0)).to_contain_text("Scissors")
    expect(choices.nth(1)).to_contain_text("Paper")
    expect(page.locator("[data-outcome]")).to_have_attribute("data-outcome", "win")
    expect(page.get_by_role("heading", name="You win!", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Computer wins", exact=True)).to_have_count(
        0
    )
