"""Rules for one independent round of Rock, Paper, Scissors."""


def determine_winner(player: str, computer: str) -> str:
    """Return 'win', 'lose', or 'tie' for valid lowercase moves."""
    if player == computer:
        return "tie"
    winning_pairs = {("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")}
    if (player, computer) in winning_pairs:
        return "win"
    return "lose"
