"""Problem 3: a social network with CSV persistence and extra-credit tests."""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from testif import testif

Network = dict[str, tuple[str, list[str]]]


def add_user(sn: Network, username: str, fullname: str) -> bool:
    """Add a user with no friends; return False for an existing username."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except (TypeError, ValueError) as error:
        print(f"Could not add the user: {error}")
        raise


def add_friend(sn: Network, user1: str, user2: str) -> bool:
    """Add a mutual link; reject missing users, self-links and existing links."""
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False
        if user2 in sn[user1][1] and user1 in sn[user2][1]:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except (TypeError, KeyError, IndexError, AttributeError) as error:
        print(f"Could not add the friendship: {error}")
        raise


def get_friends(sn: Network, user1: str, distance: int) -> list[str]:
    """Return unique friends within distance links in breadth-first order."""
    try:
        if not isinstance(distance, int) or isinstance(distance, bool) or distance < 1:
            raise ValueError("Distance must be a positive integer.")
        if user1 not in sn:
            return []
        seen, frontier, result = {user1}, [user1], []
        for _ in range(distance):
            following = []
            for user in frontier:
                for friend in sn[user][1]:
                    if friend not in seen:
                        seen.add(friend)
                        following.append(friend)
                        result.append(friend)
            frontier = following
            if not frontier:
                break
        return result
    except (TypeError, ValueError, KeyError, IndexError) as error:
        print(f"Could not find friends: {error}")
        raise


def save_network(filename: str, sn: Network) -> None:
    """Save headerless CSV rows: username, full name, then each friend."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname, *friends])
    except (OSError, UnicodeError, csv.Error, TypeError, ValueError) as error:
        print(f"Could not save the network: {error}")
        raise


def load_network(filename: str) -> Network:
    """Read a network saved by save_network, rejecting malformed rows."""
    try:
        network = {}
        with open(filename, newline="", encoding="utf-8") as file:
            for row in csv.reader(file):
                if len(row) < 2 or row[0] in network:
                    raise ValueError("Missing fields or duplicate username.")
                network[row[0]] = (row[1], row[2:])
        return network
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Could not load the network: {error}")
        raise


def test() -> None:
    """Test parts a-e with the supplied testif function (extra credit)."""
    try:
        sn = {}
        results = []
        for user, name in [("alice", "Alice Smith"), ("maria", "Maria Cortez"),
                           ("joe", "Joseph Adams"), ("eve", "Evelyn Cooper"),
                           ("david", "David Benson")]:
            results.append(testif(add_user(sn, user, name), f"add {user}"))
        results.append(testif(not add_user(sn, "alice", "Other"), "duplicate user"))
        for left, right in [("alice", "maria"), ("maria", "joe"),
                            ("joe", "eve"), ("maria", "david")]:
            results.append(testif(add_friend(sn, left, right), f"link {left}-{right}"))
        results.append(testif(not add_friend(sn, "alice", "missing"), "missing user"))
        results.append(testif(not add_friend(sn, "alice", "alice"), "self-link"))
        results.append(testif(not add_friend(sn, "alice", "maria"), "duplicate link"))
        results.append(testif(get_friends(sn, "alice", 1) == ["maria"], "distance 1"))
        results.append(testif(get_friends(sn, "alice", 2) == ["maria", "joe", "david"],
                              "distance 2"))
        results.append(testif(get_friends(sn, "alice", 20) ==
                              ["maria", "joe", "david", "eve"], "cycles"))
        results.append(testif(get_friends(sn, "unknown", 2) == [], "unknown user"))
        add_user(sn, "solo", 'Solo, "Student"')
        results.append(testif(get_friends(sn, "solo", 1) == [], "isolated user"))
        with TemporaryDirectory() as folder:
            filename = str(Path(folder) / "network.csv")
            save_network(filename, sn)
            results.append(testif(Path(filename).is_file(), "save network"))
            results.append(testif(load_network(filename) == sn, "CSV round trip"))
        if not all(results):
            raise AssertionError("A social network test failed.")
    except (OSError, ValueError, TypeError, AssertionError) as error:
        print(f"Social network tests could not complete: {error}")
        raise


def main() -> None:
    """Run the tests for all social network operations."""
    try:
        print("Student: Jorge Alfaro | FAU ID: Z23697022 | Problem 3")
        test()
    except (OSError, ValueError, TypeError, AssertionError) as error:
        print(f"Problem 3 could not finish: {error}")
        raise


if __name__ == "__main__":
    main()
