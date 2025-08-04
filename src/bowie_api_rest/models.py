"""
SQLAlchemy ORM models for albums and tracks.

This file contains the SQLAlchemy ORM models used for representing albums and their tracks in the database.
It defines the `Album` and `Track` models, which are used for interacting with the album and track data.
"""

from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, relationship


# Base class for all models
Base = declarative_base()


class Track(Base):
    """
    ORM model for a track.

    :param int id: Unique identifier for the track.
    :param str title: Title of the track.
    :param str duration: Duration of the track in mm:ss format.
    :param Optional[int] album_id: Foreign key to the associated album.
    :param Optional[Album] album: Reference to the associated Album object.
    """

    __tablename__ = "track"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String, nullable=False)
    duration: Mapped[str] = Column(String, nullable=False)  # Format: mm:ss

    album_id: Mapped[int | None] = Column(Integer, ForeignKey("album.id"), nullable=True)
    album: Mapped[Optional["Album"]] = relationship("Album", back_populates="tracks")


class Album(Base):
    """
    ORM model for an album.

    :param int id: Unique identifier for the album.
    :param str title: Title of the album.
    :param int year: Release year of the album.
    :param List[Track] tracks: List of associated Track objects.
    """

    __tablename__ = "album"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String, nullable=False)
    year: Mapped[int] = Column(Integer, nullable=False)

    tracks: Mapped[list[Track]] = relationship("Track", back_populates="album", cascade="all, delete-orphan")
