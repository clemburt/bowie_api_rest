"""
Script to load David Bowie albums from JSON using Pydantic v2 BaseSettings
and populate a SQLite database using SQLAlchemy ORM.
The SQLite DB file is created in the same folder as the JSON file,
and will be overwritten if it already exists.
"""

from pathlib import Path
from typing import List, Self

from pydantic import FilePath, validate_call
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bowie_api_rest.config import DEFAULT_DB_PATH
from bowie_api_rest.models import Album, Base, Track
from bowie_api_rest.schemas_base import AlbumBase


class AlbumInput(AlbumBase):
    """
    Pydantic model representing an input album with tracks.

    :param List[List[str]] tracks: List of tracks as [title, duration].
    """

    tracks: List[List[str]]

    def to_album(self) -> Album:
        """Convert AlbumInput to SQLAlchemy Album instance."""
        return Album(title=self.title, year=self.year)

    def to_tracks(self, album: Album) -> List[Track]:
        """Convert tracks list to SQLAlchemy Track instances linked to album.

        :param album: Album instance to link tracks to.
        :type album: Album
        :return: List of Track instances.
        :rtype: List[Track]
        """
        return [Track(title=t, duration=d, album=album) for t, d in self.tracks]


class AlbumsConfig(BaseSettings):
    """
    Pydantic settings class to load albums data from JSON.

    :param albums_data: List of album inputs.
    """

    albums_data: List[AlbumInput]

    @classmethod
    @validate_call
    def from_json(cls, path: FilePath) -> Self:
        """
        Load and validate albums data from JSON file.

        :param FilePath path: Path to JSON file.
        :return: AlbumsConfig instance with validated data.
        :rtype: Self
        """
        return cls.model_validate_json(path.read_bytes())


def init_db(sqlite_path: Path) -> sessionmaker[Session]:
    """
    Initialize the SQLite database, overwrite if exists, create tables and return a session factory.

    :param Path sqlite_path: Path to SQLite database file.
    :return: SQLAlchemy session factory.
    :rtype: sessionmaker[Session]
    """
    # Overwrite existing DB file if present
    if sqlite_path.exists():
        sqlite_path.unlink()

    db_url = f"sqlite:///{sqlite_path.as_posix()}"
    engine = create_engine(db_url, echo=False, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)


def seed_database(
    albums: List[AlbumInput], session_factory: sessionmaker[Session]
) -> None:
    """
    Insert albums and their tracks into the database.

    :param List[AlbumInput] albums: List of AlbumInput instances.
    :param sessionmaker[Session] session_factory: SQLAlchemy session factory.
    """
    with session_factory() as session:
        for album_input in albums:
            album = album_input.to_album()
            session.add(album)
            session.flush()  # Populate album.id for foreign keys
            tracks = album_input.to_tracks(album)
            session.add_all(tracks)
        session.commit()
    print("✅ Database seeded with album data.")


if __name__ == "__main__":
    json_path = (
        Path(__file__).resolve().parent.parent
        / "src"
        / "bowie_api_rest"
        / "db"
        / "bowie_discography.json"
    )
    db_path = DEFAULT_DB_PATH

    print(f"📂 Loading album data from {json_path}")
    print(f"💾 Creating (or overwriting) SQLite database at {db_path}")

    # Load albums data from JSON using Pydantic v2
    config = AlbumsConfig.from_json(json_path)

    # Initialize DB and get session factory
    SessionLocal = init_db(db_path)

    # Seed the database
    seed_database(config.albums_data, SessionLocal)
