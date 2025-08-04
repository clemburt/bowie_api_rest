"""Data access layer for querying album and track information."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from bowie_api_rest.models import Album, Track


def get_albums_by_title(session: Session, album_title_part: str) -> list[Album]:
    """
    Retrieve all albums that match a partial album title (case-insensitive).

    :param Session session: SQLAlchemy session to perform the query.
    :param str album_title_part: Partial album title to search for (case-insensitive).
    :return: List of albums matching the search criteria, with their tracks.
    :rtype: List[Album]
    """
    # Build a SELECT statement to find albums with titles matching the substring
    stmt = (
        select(Album)
        .where(func.lower(Album.title).like(f"%{album_title_part.lower()}%"))
        .options(selectinload(Album.tracks))  # Eager load tracks
    )

    # Execute the query and get all albums matching the partial title
    albums: list[Album] = session.execute(stmt).scalars().all()
    return albums


def get_albums_containing_track(session: Session, track_title_part: str) -> list[Album]:
    """
    Retrieve all albums that contain at least one track with a title containing the given substring, case-insensitive.

    The tracks of each album are eagerly loaded.

    :param Session session: SQLAlchemy session to perform the query.
    :param str track_title_part: Substring to search for in track titles (case-insensitive).
    :return: List of albums matching the search criteria, with their tracks.
    :rtype: List[Album]
    """
    # Build a SELECT statement to find albums where at least one track title matches the substring
    stmt = (
        select(Album)
        .join(Album.tracks)
        .where(func.lower(Track.title).like(f"%{track_title_part.lower()}%"))
        .options(selectinload(Album.tracks))  # Eager load tracks
        .distinct()  # Ensure uniqueness of albums
    )

    # Execute the query and extract unique album results
    albums: list[Album] = session.execute(stmt).unique().scalars().all()
    return albums
