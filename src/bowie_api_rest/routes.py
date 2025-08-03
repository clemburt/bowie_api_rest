"""
API routes for album and track endpoints.

This module defines the API routes for interacting with albums and tracks in the David Bowie discography.
It includes routes to retrieve albums by track title, list all albums, and fetch albums by title.
"""

from typing import Callable, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from bowie_api_rest.crud import (get_albums_by_title,
                                 get_albums_containing_track)
from bowie_api_rest.models import Album
from bowie_api_rest.schemas import AlbumRead, HealthResponse, TrackRead

# Initialize the API router for handling album and track endpoints
router = APIRouter()

# Placeholder for the session dependency to be set dynamically
_get_session_dependency: Optional[Callable[..., Session]] = None


def set_get_session_dependency(dep: Callable[..., Session]) -> None:
    """
    Set the session dependency callable to provide a SQLAlchemy session.

    :param Callable[..., Session] dep: Callable that returns a SQLAlchemy session generator.
    """
    global _get_session_dependency
    _get_session_dependency = dep


def get_session_placeholder() -> Session:
    """
    Retrieve a SQLAlchemy session from the injected dependency.

    :raises RuntimeError: If the session dependency has not been set.
    :return: SQLAlchemy session instance.
    :rtype: Session
    """
    if _get_session_dependency is None:
        raise RuntimeError("Session dependency has not been set")
    # Consume the generator to get the session instance
    return next(_get_session_dependency())


@router.get("/tracks/{track_title}/albums", response_model=List[AlbumRead])
def search_albums_containing_track(
    track_title: str, session: Session = Depends(get_session_placeholder)
) -> List[AlbumRead]:
    """
    Retrieve all albums containing at least one track whose title partially matches the given string (case-insensitive).
    Only the matching tracks are included in each album's track list.

    :param str track_title: Partial track title to search for (case-insensitive).
    :param Session session: SQLAlchemy session (injected dependency).
    :raises HTTPException: When no albums or matching tracks are found.
    :return: List of albums with filtered matching tracks.
    :rtype: List[AlbumRead]
    """
    albums: List[Album] = get_albums_containing_track(session, track_title)

    # If no albums are found, raise HTTPException
    if not albums:
        raise HTTPException(status_code=404, detail="No albums found for this track")

    lower_search: str = track_title.lower()
    result: List[AlbumRead] = []

    # Iterate through albums and filter tracks based on the search string
    for album in albums:
        filtered_tracks = [t for t in album.tracks if lower_search in t.title.lower()]
        if filtered_tracks:
            # Convert filtered tracks to Pydantic models
            track_reads = [
                TrackRead(id=t.id, title=t.title, duration=t.duration)
                for t in filtered_tracks
            ]
            # Create AlbumRead model with filtered tracks only
            album_read = AlbumRead(
                id=album.id, title=album.title, year=album.year, tracks=track_reads
            )
            result.append(album_read)

    # If no matching tracks are found, raise HTTPException
    if not result:
        raise HTTPException(
            status_code=404, detail="No tracks found matching the query"
        )

    return result


@router.get("/albums/", response_model=List[AlbumRead])
def list_albums(session: Session = Depends(get_session_placeholder)) -> List[AlbumRead]:
    """
    List all albums with their tracks.

    :param Session session: SQLAlchemy session (injected dependency).
    :return: List of all albums with tracks.
    :rtype: List[AlbumRead]
    """
    # Query all albums and include their associated tracks
    stmt = select(Album).options(selectinload(Album.tracks))
    albums = session.execute(stmt).scalars().all()
    return albums


@router.get("/albums/by-title/", response_model=List[AlbumRead])
def search_albums_by_title(
    album_title: str = Query(
        ..., description="Title of the album to search (case-insensitive)"
    ),
    session: Session = Depends(get_session_placeholder),
) -> List[AlbumRead]:
    """
    Get albums by partial album title and return all matching albums with their tracks.

    :param str album_title: Partial title of the album to search.
    :param Session session: SQLAlchemy session (injected dependency).
    :raises HTTPException: If no album is found with the given title.
    :return: List of albums with tracks that match the partial title.
    :rtype: List[AlbumRead]
    """
    albums: List[Album] = get_albums_by_title(session, album_title)

    # If no albums are found, raise HTTPException
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
