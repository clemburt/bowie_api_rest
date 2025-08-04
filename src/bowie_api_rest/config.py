"""
Manage the configuration of the application.

Load environment variables and define constants for file paths and other configuration parameters used across the project.
"""

import os
from pathlib import Path


# Configuration variables
DEFAULT_DB_PATH: Path = Path(os.getenv("DB_PATH", str(Path(__file__).resolve().parent / "db" / "bowie_discography.db")))
"""
This variable holds the default path to the SQLite database file used by the application.
It can be overridden by the `DB_PATH` environment variable loaded from the `.env` file.
If not defined, the default path will be relative to the current file's directory.
"""
