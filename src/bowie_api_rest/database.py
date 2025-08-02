"""
Database connection and initialization using SQLAlchemy with dynamic configuration.
"""
from typing import Generator, Self, Callable

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, FilePath

from bowie_api_rest.models import Base


class DatabaseConfig(BaseModel):
    """
    Base database configuration model using SQLAlchemy.

    :param Engine engine: SQLAlchemy Engine instance.
    """
    engine: Engine

    # Allow non-serializable types like SQLAlchemy Engine
    model_config = dict(arbitrary_types_allowed=True)

    def create_engine(self) -> Engine:
        """
        Return the configured SQLAlchemy engine.

        :return: SQLAlchemy Engine instance.
        :rtype: Engine
        """
        return self.engine


class FileDatabaseConfig(DatabaseConfig):
    """
    Database configuration for a file-based SQLite database.

    :param FilePath db_file: Path to the SQLite database file.
    """
    db_file: FilePath

    @classmethod
    def from_db_file(cls, db_file: FilePath) -> Self:
        """
        Create a FileDatabaseConfig instance from a SQLite database file path.

        :param FilePath db_file: Path to the SQLite database file.
        :return: FileDatabaseConfig instance.
        :rtype: Self
        :raises ValueError: If the db_file does not exist.
        """
        # Create SQLAlchemy engine for SQLite
        engine: Engine = create_engine(f"sqlite:///{db_file}", future=True)
        return cls(engine=engine, db_file=db_file)


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    """
    Create a SQLAlchemy session factory from a given engine.

    :param Engine engine: SQLAlchemy Engine instance.
    :return: Configured sessionmaker factory.
    :rtype: sessionmaker[Session]
    """
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db(engine: Engine) -> None:
    """
    Create all tables in the database using the given engine.

    :param Engine engine: SQLAlchemy Engine instance.
    """
    Base.metadata.create_all(bind=engine)


def create_session_dependency(session_factory: sessionmaker[Session]) -> Callable[[], Generator[Session, None, None]]:
    """
    Create a FastAPI-compatible dependency function that yields a SQLAlchemy session.

    This function can be used with FastAPI's `Depends()` system
    to inject a session into route handlers.

    :param sessionmaker[Session] session_factory: SQLAlchemy session factory.
    :return: Callable dependency function that yields a session.
    :rtype: Callable[[], Generator[Session, None, None]]
    """
    def get_session() -> Generator[Session, None, None]:
        # Context-managed session with automatic cleanup
        with session_factory() as session:
            yield session

    return get_session
