"""
API routes for album and track endpoints.

This module defines the API routes for interacting with albums and tracks in the David Bowie discography.
It includes routes to retrieve albums by track title, list all albums, and fetch albums by title.
"""

from collections.abc import Callable, Generator

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from bowie_api_rest.crud import get_albums_by_title, get_albums_containing_track
from bowie_api_rest.models import Album
from bowie_api_rest.schemas import AlbumRead, HealthResponse, TrackRead


# Initialize the API router for handling album and track endpoints
router = APIRouter()

# Placeholder for the session dependency to be set dynamically
_get_session_dependency: Callable[..., Generator[Session, None, None]] | None = None


def set_get_session_dependency(dep: Callable[..., Generator[Session, None, None]]) -> None:
    """
    Set the session dependency callable to provide a SQLAlchemy session.

    :param Callable[..., Generator[Session, None, None]] dep: Callable that returns a SQLAlchemy session generator.
    """
    global _get_session_dependency
    _get_session_dependency = dep


def get_session_placeholder() -> Generator[Session, None, None]:
    """
    Retrieve a SQLAlchemy session from the injected dependency.

    :raises RuntimeError: If the session dependency has not been set.
    :return: SQLAlchemy session generator.
    :rtype: Generator[Session, None, None]
    """
    if _get_session_dependency is None:
        raise RuntimeError("Session dependency has not been set")
    yield from _get_session_dependency()


def _get_session() -> Session:
    """
    Dependency function to provide a SQLAlchemy session for FastAPI routes.

    :return: A SQLAlchemy session instance.
    :rtype: Session
    """
    return next(get_session_placeholder())


# Create a FastAPI dependency singleton to avoid calling Depends() in function defaults
session_dependency = Depends(_get_session)


@router.get("/tracks/{track_title}/albums", response_model=list[AlbumRead])
def search_albums_containing_track(
    track_title: str,
    session: Session = session_dependency,
) -> list[AlbumRead]:
    """
    Retrieve all albums containing at least one track whose title partially matches the given string (case-insensitive).

    Only the matching tracks are included in each album's track list.

    :param str track_title: Partial track title to search for (case-insensitive).
    :param Session session: SQLAlchemy session (injected dependency).
    :raises HTTPException: When no albums or matching tracks are found.
    :return: List of albums with filtered matching tracks.
    :rtype: list[AlbumRead]
    """
    albums: list[Album] = get_albums_containing_track(session, track_title)

    if not albums:
        raise HTTPException(status_code=404, detail="No albums found for this track")

    lower_search = track_title.lower()
    result: list[AlbumRead] = []

    for album in albums:
        filtered_tracks = [t for t in album.tracks if lower_search in t.title.lower()]
        if filtered_tracks:
            track_reads = [TrackRead(id=t.id, title=t.title, duration=t.duration) for t in filtered_tracks]
            album_read = AlbumRead(id=album.id, title=album.title, year=album.year, tracks=track_reads)
            result.append(album_read)

    if not result:
        raise HTTPException(status_code=404, detail="No tracks found matching the query")

    return result


@router.get("/albums/", response_model=list[AlbumRead])
def list_albums(session: Session = session_dependency) -> list[AlbumRead]:
    """
    List all albums with their tracks.

    :param Session session: SQLAlchemy session (injected dependency).
    :return: List of all albums with tracks.
    :rtype: list[AlbumRead]
    """
    stmt = select(Album).options(selectinload(Album.tracks))
    albums = session.execute(stmt).scalars().all()
    return albums


@router.get("/albums/by-title/", response_model=list[AlbumRead])
def search_albums_by_title(
    album_title: str = Query(..., description="Title of the album to search (case-insensitive)"),
    session: Session = session_dependency,
) -> list[AlbumRead]:
    """
    Get albums by partial album title and return all matching albums with their tracks.

    :param str album_title: Partial title of the album to search.
    :param Session session: SQLAlchemy session (injected dependency).
    :raises HTTPException: If no album is found with the given title.
    :return: List of albums with tracks that match the partial title.
    :rtype: list[AlbumRead]
    """
    albums: list[Album] = get_albums_by_title(session, album_title)

    if not albums:
        raise HTTPException(status_code=404, detail="Album not found")

    return albums


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint to verify that the API is running.

    :return: Health status response model with status 'ok'.
    :rtype: HealthResponse
    """
    return HealthResponse(status="ok")
