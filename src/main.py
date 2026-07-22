"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from recommender import load_songs, recommend_songs, SCORING_STRATEGIES

# Max characters per line in the "Reasons" column before wrapping.
REASONS_WIDTH = 50


def print_recommendations_table(recommendations) -> None:
    """
    Prints recommendations as a simple ASCII table with columns:
    Rank, Title, Score, Reasons.

    `recommendations` is a list of (song, score, explanation) tuples,
    same as what recommend_songs() returns.
    """
    # Figure out how wide the "Title" column needs to be so every title fits.
    title_width = max([len(rec[0]["title"]) for rec in recommendations] + [len("Title")])

    headers = ("Rank", "Title", "Score", "Reasons")
    col_widths = (4, title_width, 7, REASONS_WIDTH)

    def make_border(left, middle, right):
        pieces = ["-" * (width + 2) for width in col_widths]
        return left + middle.join(pieces) + right

    def make_row(rank, title, score, reasons_line):
        return (
            f"| {rank:<{col_widths[0]}} "
            f"| {title:<{col_widths[1]}} "
            f"| {score:<{col_widths[2]}} "
            f"| {reasons_line:<{col_widths[3]}} |"
        )

    top_border = make_border("+", "+", "+")

    print(top_border)
    print(make_row(*headers))
    print(top_border)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Long explanations get wrapped onto extra lines within the same row,
        # instead of stretching the table sideways.
        reasons_lines = textwrap.wrap(explanation, width=REASONS_WIDTH) or [""]

        print(make_row(rank, song["title"], f"{score:.2f}", reasons_lines[0]))
        for extra_line in reasons_lines[1:]:
            print(make_row("", "", "", extra_line))

    print(top_border)


def choose_strategy():
    """
    Lets the user pick a scoring mode by name.
    See SCORING_STRATEGIES in recommender.py for the available modes.
    """
    print("Choose a scoring mode:")
    for key, strategy in SCORING_STRATEGIES.items():
        print(f"  {key} ({strategy.name})")

    choice = input("Mode [genre-first]: ").strip().lower() or "genre-first"
    return SCORING_STRATEGIES.get(choice, SCORING_STRATEGIES["genre-first"])


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Deep Intense Rock
    user_prefs = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95
    }

    strategy = choose_strategy()
    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

    print(f"\nTop recommendations ({strategy.name} mode):\n")
    print_recommendations_table(recommendations)


if __name__ == "__main__":
    main()
