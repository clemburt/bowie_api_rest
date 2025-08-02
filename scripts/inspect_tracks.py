"""
Inspect track titles stored in the database for debugging purposes.

This script is useful to detect discrepancies in track title formatting,
such as invisible characters, special punctuation, or case differences
that may prevent search queries from matching expected results.
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from bowie_api_rest.models import Track
from bowie_api_rest.database import engine


def get_all_track_titles(session: Session) -> List[str]:
    """
    Retrieve all track titles from the database.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy session.

    Returns
    -------
    List[str]
        List of track titles found in the database.
    """
    result = session.scalars(select(Track.title)).all()
    return result


def print_track_titles_with_repr(titles: List[str]) -> None:
    """
    Print track titles using repr() to visualize hidden characters.

    Parameters
    ----------
    titles : List[str]
        List of track titles to inspect.
    """
    print("🎵 Track titles in database (raw repr):\n")
    for title in titles:
        print(f"- {repr(title)}")


if __name__ == "__main__":
    with Session(engine) as session:
        titles = get_all_track_titles(session)
        print_track_titles_with_repr(titles)
