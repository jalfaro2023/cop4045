"""Problem 4: rank director-actor collaborations and actor box office."""

import csv
from pathlib import Path

DATA_DIRECTORY = Path(__file__).resolve().parent


def read_movies(filename: str, value_column: str) -> dict[tuple[str, str], float]:
    """Map (title, year) to a numeric value from a CSV with a header."""
    with open(filename, newline="", encoding="utf-8") as file:
        return {(row["Title"], row["Year"]): float(row[value_column])
                for row in csv.DictReader(file)}


def read_casts(filename: str) -> dict[tuple[str, str], tuple[str, list[str]]]:
    """Map (title, year) to (director, actors) from the headerless cast CSV."""
    with open(filename, newline="", encoding="utf-8") as file:
        return {(row[0], row[1]): (row[2], row[3:]) for row in csv.reader(file)}


def display_ranking(totals: dict, limit: int | None = None) -> None:
    """Print descending totals; None displays all and zero displays none."""
    if limit is not None and limit < 0:
        raise ValueError("The display limit cannot be negative.")
    ranking = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    for rank, (key, total) in enumerate(ranking[:limit], 1):
        if isinstance(key, tuple):
            print(f"{rank:2}. {(key[0], key[1], total)}")
        else:
            print(f"{rank:2}. {key}: ${total:,.0f}")


def display_top_collaborations(limit: int | None = None) -> None:
    """Rank director-actor pairs by number of shared top-rated movies."""
    rated = read_movies(str(DATA_DIRECTORY / "imdb-top-rated.csv"), "IMDb Rating")
    casts = read_casts(str(DATA_DIRECTORY / "imdb-top-casts.csv"))
    totals = {}
    for movie in rated:
        director, actors = casts[movie]
        for actor in set(actors):
            pair = (director, actor)
            totals[pair] = totals.get(pair, 0) + 1
    display_ranking(totals, limit)


def display_top_actors(limit: int | None = None) -> None:
    """Rank actors by the sum of their movies' top-grossing box office."""
    grossing = read_movies(str(DATA_DIRECTORY / "imdb-top-grossing.csv"),
                          "USA Box Office")
    casts = read_casts(str(DATA_DIRECTORY / "imdb-top-casts.csv"))
    totals = {}
    for movie, amount in grossing.items():
        for actor in set(casts[movie][1]):
            totals[actor] = totals.get(actor, 0) + int(amount)
    display_ranking(totals, limit)


def main() -> None:
    """Demonstrate both rankings, each limited to ten entries."""
    print("Student: Jorge Alfaro | FAU ID: Z23697022 | Problem 4")
    print("Top director-actor collaborations")
    display_top_collaborations(10)
    print("\nTop actors by USA box office")
    display_top_actors(10)


if __name__ == "__main__":
    main()
