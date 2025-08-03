"""
Pydantic models for album and track data.

This module defines the Pydantic models for reading track and album data. The models are used to
validate and serialize the input and output data for the API endpoints.
"""

from pydantic import BaseModel


class TrackBase(BaseModel):
    """
    Pydantic model for reading track data.

    :param str title: Track title.
    :param str duration: Track duration in mm:ss format.
    """

    title: str
    duration: str  # mm:ss format


class AlbumBase(BaseModel):
    """
    Pydantic model for reading album data with related tracks.

    :param str title: Album title.
    :param int year: Release year of the album.
    """

    title: str
    year: int
