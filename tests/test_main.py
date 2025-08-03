import pytest
from fastapi.testclient import TestClient

from bowie_api_rest.main import \
    app  # Assuming FastAPI app is in the main module


@pytest.fixture(scope="module")
def client():
    """
    Setup and teardown for the FastAPI test client.
    This fixture provides a reusable client instance for testing.
    """
    with TestClient(app) as client:
        yield client


def test_search_tracks_in_albums(client: TestClient):
    """
    Test searching for albums containing a specific track title.
    This test checks that the track is included in the returned album data.
    """
    # Searching for "Space Oddity" in albums
    response = client.get("/tracks/Space Oddity/albums")
    assert response.status_code == 200
    albums = response.json()

    # Assert that "Space Oddity" appears in the expected album "David Bowie"
    found_album = next(
        (album for album in albums if album["title"] == "David Bowie"), None
    )
    assert found_album is not None, "Album 'David Bowie' not found in the response"
    track_titles = [track["title"] for track in found_album["tracks"]]
    assert "Space Oddity" in track_titles


def test_search_tracks_case_insensitive(client: TestClient):
    """
    Test searching for tracks in albums case-insensitively.
    This checks that track titles are matched regardless of case.
    """
    response = client.get("/tracks/space oddity/albums")  # Case-insensitive search
    assert response.status_code == 200
    albums = response.json()

    # Check that the album with "Space Oddity" is still returned
    found_album = next(
        (album for album in albums if album["title"] == "David Bowie"), None
    )
    assert found_album is not None
    track_titles = [track["title"] for track in found_album["tracks"]]
    assert "Space Oddity" in track_titles


def test_search_tracks_partial_title(client: TestClient):
    """
    Test searching for albums by a partial track title.
    This checks if albums containing tracks with partial titles are returned.
    """
    response = client.get(
        "/tracks/Space/albums"
    )  # Searching with a partial track title
    assert response.status_code == 200
    albums = response.json()

    # Check that at least one album with a track containing "Space" is returned
    assert len(albums) > 0
    found_album = next(
        (album for album in albums if "David Bowie" in album["title"]), None
    )
    assert found_album is not None
    track_titles = [track["title"] for track in found_album["tracks"]]
    assert any("Space" in title for title in track_titles)


def test_search_albums_by_title(client: TestClient):
    """
    Test searching for albums by partial title.
    This checks if albums with a matching partial title are returned.
    """
    response = client.get(
        "/albums/by-title/?album_title=Hunky"
    )  # Partial album title search
    assert response.status_code == 200
    albums = response.json()

    # Assert that the album "Hunky Dory" is returned
    assert len(albums) > 0
    found_album = next(
        (album for album in albums if album["title"] == "Hunky Dory"), None
    )
    assert found_album is not None


def test_search_albums_case_insensitive(client: TestClient):
    """
    Test searching for albums by title, case-insensitively.
    This checks if the search is case-insensitive and still matches albums.
    """
    response = client.get(
        "/albums/by-title/?album_title=hunky dory"
    )  # Case-insensitive search
    assert response.status_code == 200
    albums = response.json()

    # Assert that the album "Hunky Dory" is found regardless of case
    assert len(albums) > 0
    found_album = next(
        (album for album in albums if album["title"] == "Hunky Dory"), None
    )
    assert found_album is not None


def test_search_album_by_exact_title(client: TestClient):
    """
    Test searching for albums by exact title.
    This checks that only albums with an exact match for the title are returned.
    """
    response = client.get(
        "/albums/by-title/?album_title=Diamond Dogs"
    )  # Exact album title search
    assert response.status_code == 200
    albums = response.json()

    # Assert that the album "Diamond Dogs" is returned and no other albums are present
    assert len(albums) == 1
    assert albums[0]["title"] == "Diamond Dogs"


def test_search_multiple_tracks(client: TestClient):
    """
    Test searching for multiple tracks within an album.
    This checks if multiple tracks exist within the album.
    """
    response = client.get(
        "/tracks/Young/albums"
    )  # Searching for multiple tracks with partial title
    assert response.status_code == 200
    albums = response.json()

    assert len(albums) > 0
    found_album = next(
        (album for album in albums if album["title"] == "Young Americans"), None
    )
    assert found_album is not None
    track_titles = [track["title"] for track in found_album["tracks"]]

    # Assert that at least one of the tracks contains "Young" and another contains "Americans"
    assert any("Young" in title for title in track_titles)
    assert any("Americans" in title for title in track_titles)


def test_search_album_by_year(client: TestClient):
    """
    Test searching for albums by year.
    This checks if albums are correctly filtered by the release year.
    """
    response = client.get(
        "/albums/by-title/?album_title=The Man Who Sold the World"
    )  # Album with exact title
    assert response.status_code == 200
    albums = response.json()

    # Check that the album "The Man Who Sold the World" is present
    found_album = next(
        (album for album in albums if album["title"] == "The Man Who Sold the World"),
        None,
    )
    assert found_album is not None
    assert found_album["year"] == 1970


def test_search_album_with_track_duration(client: TestClient):
    """
    Test searching albums with tracks having specific durations.
    This checks that the duration of a track matches the expected value.
    """
    response = client.get("/tracks/Modern Love/albums")
    assert response.status_code == 200
    albums = response.json()

    # Assert that the track "Modern Love" exists in one of the albums and check the duration
    found_album = next(
        (album for album in albums if album["title"] == "Let's Dance"), None
    )
    assert found_album is not None
    track = next(
        (track for track in found_album["tracks"] if track["title"] == "Modern Love"),
        None,
    )
    assert track is not None
    assert track["duration"] == "4:48"


def test_search_for_non_existent_track(client: TestClient):
    """
    Test searching for a non-existent track in the albums database.
    This checks that the API handles searches with no results correctly.
    """
    response = client.get("/tracks/NonExistentTrack/albums")
    assert response.status_code == 404
    assert response.json() == {"detail": "No albums found for this track"}


def test_search_for_non_existent_album(client: TestClient):
    """
    Test searching for a non-existent album in the albums database.
    This checks that the API handles searches with no results correctly.
    """
    response = client.get("/albums/by-title/?album_title=NonExistentAlbum")
    assert response.status_code == 404
    assert response.json() == {"detail": "Album not found"}
