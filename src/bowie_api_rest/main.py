"""
Main application entry point for the David Bowie Albums API.

This module creates and configures the FastAPI app, including
database initialization, session dependency injection, and route registration.
"""

from fastapi import FastAPI
from pydantic import FilePath
from sqlalchemy.orm import sessionmaker

from bowie_api_rest import routes
from bowie_api_rest.config import DEFAULT_DB_PATH
from bowie_api_rest.database import FileDatabaseConfig, create_session_dependency, get_session_factory, init_db


def create_app(db_path: FilePath | None = DEFAULT_DB_PATH) -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    :param Optional[FilePath] db_path: Optional path to the SQLite database file. Defaults to DEFAULT_DB_PATH.
    :return: Configured FastAPI application instance.
    :rtype: FastAPI
    """
    app_instance = FastAPI(title="David Bowie Albums API")

    # Create the database engine from the given file path
    engine = FileDatabaseConfig.from_db_file(db_path).engine

    # Initialize the database schema (create tables if they do not exist)
    init_db(engine)

    # Create a SQLAlchemy session factory for managing database sessions
    session_factory: sessionmaker = get_session_factory(engine)

    # Create a FastAPI-compatible dependency for providing DB sessions
    get_session = create_session_dependency(session_factory)

    # Inject the session dependency into the routes module
    routes.set_get_session_dependency(get_session)

    # Include all API routes from the routes module
    app_instance.include_router(routes.router)

    return app_instance


# Instantiate the FastAPI app with the default database path
app: FastAPI = create_app()
