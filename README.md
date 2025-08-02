# bowie_api_rest
# Table of Contents
- [Purpose](#purpose)
- [Installation](#installation)
- [Usage](#usage)
  - [Run the API REST](#run-the-api-rest)
  - [API Endpoints](#api-endpoints)
    - [Search tracks by title](#search-tracks-by-title)
    - [Search albums by title](#search-albums-by-title)
- [Tests](#tests)
- [Documentation](#documentation)
- [Docker Notes](#docker-notes)
- [License](#license)
- [Authors](#authors)

# Purpose
A RESTful API built with FastAPI and SQLAlchemy to explore David Bowie's discography, using pdm and pydantic.

The API provides endpoints to retrieve albums, tracks, and search for specific albums or tracks by title. It uses SQLAlchemy for database interactions and includes an in-memory or file-based SQLite database to store album and track data.

# Installation
Make sure you have [PDM](https://pdm.fming.dev/) installed.

```bash
pdm install
```

If running inside Docker, you can use the published image:

```bash
docker pull ghcr.io/clemburt/bowie_api_rest:latest
```

# Usage
## Run the API REST
To run the API REST locally, you can use the following command to start the FastAPI app with Uvicorn:

```bash
uvicorn bowie_api_rest.main:app --reload --host 0.0.0.0 --port 8000
```

This will start the API server on http://127.0.0.1:8000. You can then make API requests as shown in the examples above.

## API Endpoints
You can interact with the API REST using the following endpoints. These can be tested and accessed using `curl` or any other HTTP client.

### Search tracks by title
This endpoint returns albums that contain tracks matching the provided track title (case-insensitive). Partial matches for track titles are supported.

**Endpoint**: `/tracks/{track_title}/albums`

**Examples**:

To search for albums containing tracks with the partial title "Fa" (case-insensitive), run the following `curl` command:

```bash
curl 'http://127.0.0.1:8000/tracks/Fa/albums'
```

Expected response (for example):

```json
[
  {
    "title": "Diamond Dogs",
    "year": 1974,
    "id": 7,
    "tracks": [
      {
        "title": "Chant of the Ever Circling Skeletal Family",
        "duration": "4:46",
        "id": 76
      }
    ]
  },
  {
    "title": "Young Americans",
    "year": 1975,
    "id": 8,
    "tracks": [
      {
        "title": "Fascination",
        "duration": "3:43",
        "id": 79
      },
      {
        "title": "Fame",
        "duration": "4:12",
        "id": 83
      }
    ]
  },
  {
    "title": "Lodger",
    "year": 1979,
    "id": 12,
    "tracks": [
      {
        "title": "Fantastic Voyage",
        "duration": "2:55",
        "id": 112
      }
    ]
  },
  {
    "title": "Scary Monsters (and Super Creeps)",
    "year": 1980,
    "id": 13,
    "tracks": [
      {
        "title": "Fashion",
        "duration": "4:48",
        "id": 126
      }
    ]
  }
]
```

To search for albums containing tracks with the title "Fashion" (case-insensitive), run the following `curl` command:

```bash
curl 'http://127.0.0.1:8000/tracks/Fashion/albums'

```

Expected response (for example):

```json
 [
  {
    "title": "Scary Monsters (and Super Creeps)",
    "year": 1980,
    "id": 13,
    "tracks": [
      {
        "title": "Fashion",
        "duration": "4:48",
        "id": 126
      }
    ]
  }
]
```

### Search albums by title
This endpoint allows you to search for albums by a partial album title (case-insensitive). Partial matches for album titles are supported.

**Endpoint:** /albums/by-title/

**Examples:**

To search for albums with a title containing "star", run the following `curl` command:

```bash
curl -G 'http://127.0.0.1:8000/albums/by-title/' --data-urlencode 'album_title=star'
```

To search for albums with a title containing "scary monsters", run the following `curl` command:

```bash
curl -G 'http://127.0.0.1:8000/albums/by-title/' --data-urlencode 'album_title=scary monsters'
```

These examples should help you interact with the API REST and test various endpoints to search for albums and tracks. Make sure the API is running before sending these requests!

# Tests
Run the test suite using:
```bash
pdm test
```

This will:
- Sync test dependencies
- Run all tests with coverage reporting

# Documentation
Build the sphinx documentation using
```bash
pdm doc
```

📚 [Documentation](https://clemburt.github.io/bowie_api_rest/)

# Docker Notes
The image installs only production dependencies (--prod), so tests must be run explicitly with dev install:

```bash
docker run --rm \
  ghcr.io/clemburt/bowie_api_rest:latest \
  sh -c "pdm install -G test && pdm test"
```

# License
MIT License

# Authors
- [BURTSCHER Clément](https://github.com/clemburt)