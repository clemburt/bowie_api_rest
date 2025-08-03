# Table of Contents
- [Purpose](#purpose)
- [Installation](#installation)
- [Usage](#usage)
  - [Run the API REST](#run-the-api-rest)
  - [API Endpoints](#api-endpoints)
    - [Search tracks by title](#search-tracks-by-title)
    - [Search albums by title](#search-albums-by-title)
  - [Scripts](#scripts)
    - [Build .db file](#build-db-file)
- [Tests](#tests)
- [Documentation](#documentation)
- [License](#license)
- [Authors](#authors)

# Purpose
**bowie_api_rest** is a RESTful API built with FastAPI and SQLAlchemy to explore David Bowie's discography, using pdm and pydantic.

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

Expected response (for example):

```json
 [
  {
    "title": "The Rise and Fall of Ziggy Stardust and the Spiders from Mars",
    "year": 1972,
    "id": 4,
    "tracks": [
      {
        "title": "Five Years",
        "duration": "4:42",
        "id": 31
      },
      {
        "title": "Soul Love",
        "duration": "3:34",
        "id": 32
      },
      {
        "title": "Moonage Daydream",
        "duration": "4:40",
        "id": 33
      },
      {
        "title": "Starman",
        "duration": "4:10",
        "id": 34
      },
      {
        "title": "It Ain't Easy",
        "duration": "2:58",
        "id": 35
      },
      {
        "title": "Lady Stardust",
        "duration": "3:22",
        "id": 36
      },
      {
        "title": "Star",
        "duration": "2:47",
        "id": 37
      },
      {
        "title": "Hang On to Yourself",
        "duration": "2:40",
        "id": 38
      },
      {
        "title": "Ziggy Stardust",
        "duration": "3:13",
        "id": 39
      },
      {
        "title": "Suffragette City",
        "duration": "3:25",
        "id": 40
      },
      {
        "title": "Rock 'n' Roll Suicide",
        "duration": "2:58",
        "id": 41
      }
    ]
  },
  {
    "title": "Blackstar",
    "year": 2016,
    "id": 17,
    "tracks": [
      {
        "title": "Blackstar",
        "duration": "9:57",
        "id": 168
      },
      {
        "title": "'Tis a Pity She Was a Whore",
        "duration": "5:16",
        "id": 169
      },
      {
        "title": "Lazarus",
        "duration": "6:22",
        "id": 170
      },
      {
        "title": "Sue (Or in a Season of Crime)",
        "duration": "3:58",
        "id": 171
      },
      {
        "title": "Girl Loves Me",
        "duration": "4:50",
        "id": 172
      },
      {
        "title": "Dollar Days",
        "duration": "4:53",
        "id": 173
      },
      {
        "title": "I Can't Give Everything Away",
        "duration": "5:47",
        "id": 174
      }
    ]
  }
]
```

To search for albums with a title containing "scary monsters", run the following `curl` command:

```bash
curl -G 'http://127.0.0.1:8000/albums/by-title/' --data-urlencode 'album_title=scary monsters'
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
        "title": "It's No Game (No. 1)",
        "duration": "4:20",
        "id": 122
      },
      {
        "title": "Up the Hill Backwards",
        "duration": "2:43",
        "id": 123
      },
      {
        "title": "Scary Monsters (and Super Creeps)",
        "duration": "4:08",
        "id": 124
      },
      {
        "title": "Ashes to Ashes",
        "duration": "4:26",
        "id": 125
      },
      {
        "title": "Fashion",
        "duration": "4:48",
        "id": 126
      },
      {
        "title": "Teenage Wildlife",
        "duration": "6:51",
        "id": 127
      },
      {
        "title": "Scream Like a Baby",
        "duration": "3:36",
        "id": 128
      },
      {
        "title": "Kingdom Come",
        "duration": "2:49",
        "id": 129
      },
      {
        "title": "Because You're Young",
        "duration": "2:50",
        "id": 130
      },
      {
        "title": "Crossfire",
        "duration": "5:34",
        "id": 131
      },
      {
        "title": "You're Not Alone",
        "duration": "2:45",
        "id": 132
      },
      {
        "title": "Future Legend",
        "duration": "0:55",
        "id": 133
      },
      {
        "title": "Teenage Wildlife (Reprise)",
        "duration": "1:18",
        "id": 134
      }
    ]
  }
]
```

These examples should help you interact with the API REST and test various endpoints to search for albums and tracks. Make sure the API is running before sending these requests!

## Scripts
### Build .db file
This script *scripts/build_db.py* loads David Bowie album data from the JSON file *src/bowie_api_rest/db/bowie_discography.json*, validates it using **Pydantic v2**, and populates an SQLite database *src/bowie_api_rest/db/bowie_discography.db* with albums and tracks using **SQLAlchemy ORM**. This .db file is the default SQLite database loaded when no file is provided.

Features:
- Loads album data from a JSON file.
- Initializes or overwrites an SQLite database.
- Seeds the database with album and track information.

Run the script with:
```bash
pdm build_db
```

This will create or overwrite the SQLite database and populate it with the data.

# Tests
Run the test suite using:
```bash
pdm install -dG test
pdm test
```

The Docker image installs only production dependencies (--prod), so tests must be run explicitly with test group install:

```bash
docker run --rm \
  ghcr.io/clemburt/bowie_api_rest:latest \
  sh -c "pdm install -dG test && pdm test"
```

This will:
- Sync test dependencies
- Run all tests with coverage reporting

# Documentation
Build the sphinx documentation using
```bash
pdm install -dG doc
pdm doc
```

The Docker image installs only production dependencies (--prod), so doc must be run explicitly with doc group install:

```bash
docker run --rm \
  ghcr.io/clemburt/bowie_api_rest:latest \
  sh -c "pdm install -dG doc && pdm doc"
```

📚 [Documentation](https://clemburt.github.io/bowie_api_rest/)

# License
MIT License

# Authors
- [BURTSCHER Clément](https://github.com/clemburt)
