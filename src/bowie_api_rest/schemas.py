"""
Pydantic models for serializing albums and tracks in API responses.

This module defines Pydantic models used for serializing album and track data to be sent in API responses.
It includes models for reading track and album data, including the list of tracks in an album.
"""

from typing import List
from pydantic import ConfigDict
from bowie_api_rest.schemas_base import AlbumBase, TrackBase


class BaseConfigModel(TrackBase):
    """
    Base Pydantic model with common configuration.

    This base class sets the Pydantic model configuration to
    allow model population from ORM objects via `from_attributes=True`.

    :cvar ConfigDict model_config: Pydantic configuration dictionary enabling ORM mode.
    """
    model_config = ConfigDict(from_attributes=True)


class TrackRead(TrackBase):
    """
    Pydantic model for reading track data.

    :param int id: Track identifier.
    """
    id: int


class AlbumRead(AlbumBase):
    """
    Pydantic model for reading album data with related tracks.

    :param int id: Album identifier.
    :param List[TrackRead] tracks: List of tracks in the album.
    """
    id: int
    tracks: List[TrackRead] = []
