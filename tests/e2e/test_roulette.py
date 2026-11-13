"""Browser checks for Roulette and its mode-specific scores."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_roulette_spin_and_mode_switch(page: Page, live_server, monkeypatch):
    """Scissors beats Paper after both spins, and switching confirms score loss."""
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    page.add_init_script("Math.random = () => 0.9;")
    page.clock.install()
    page.goto(live_server)
    classic = page.get_by_role("button", name="Classic", exact=True)
    roulette = page.get_by_role("button", name="Roulette", exact=True)
    dialog = page.get_by_role("dialog")
    player = page.locator("#player-score")
    computer = page.locator("#computer-score")
    spin = page.get_by_role("button", name="Spin", exact=True)
    stop = page.get_by_role("button", name="Stop", exact=True)
    status = page.locator("#spin-status")
    result = page.locator("[data-outcome]")

    roulette.click()
    expect(dialog).to_be_hidden()
    spin.click()
    expect(status).to_have_text("Your wheel is spinning.")
    expect(result).to_have_count(0)
    expect(player).to_have_text("0")
    stop.click()
    expect(status).to_have_text("You spun scissors. The computer is spinning.")
    expect(stop).to_be_hidden()
    expect(spin).to_be_disabled()
    expect(player).to_have_text("0")

    page.clock.fast_forward(950)
    expect(result).to_have_attribute("data-outcome", "win")
    choices = page.get_by_label("This round’s choices").locator(".choice-value")
    expect(choices.nth(0)).to_contain_text("Scissors")
    expect(choices.nth(1)).to_contain_text("Paper")
    expect(player).to_have_text("1")

    classic.click()
    expect(dialog).to_contain_text("The score will be reset. Will you continue?")
    dialog.get_by_role("button", name="Cancel").click()
    expect(roulette).to_have_attribute("aria-pressed", "true")
    expect(player).to_have_text("1")
    expect(result).to_have_attribute("data-outcome", "win")

    page.reload()
    expect(roulette).to_have_attribute("aria-pressed", "true")
    expect(player).to_have_text("1")
    classic.click()
    dialog.get_by_role("button", name="Continue").click()
    expect(classic).to_have_attribute("aria-pressed", "true")
    expect(player).to_have_text("0")
    expect(computer).to_have_text("0")
    roulette.click()
    expect(dialog).to_be_hidden()
    expect(player).to_have_text("0")
    expect(computer).to_have_text("0")
    expect(result).to_have_count(0)
