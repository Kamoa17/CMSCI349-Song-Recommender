import unittest
from unittest.mock import Mock

# pylint: disable=import-error
from app.api.spotify import parse_track_info

class SpotifyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_spotify_track_info = {
            "album": {
                "album_type": "album",
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/0rZp7G3gIH6WkyeXbrZnGi"
                        },
                        "href": "https://api.spotify.com/v1/artists/0rZp7G3gIH6WkyeXbrZnGi",
                        "id": "0rZp7G3gIH6WkyeXbrZnGi",
                        "name": "Novo Amor",
                        "type": "artist",
                        "uri": "spotify:artist:0rZp7G3gIH6WkyeXbrZnGi",
                    }
                ],
                "available_markets": [
                    "AD",
                    "CA",
                    "GB",
                ],  # truncated for testing purposes
                "external_urls": {
                    "spotify": "https://open.spotify.com/album/0tWckYjFI6ioZptLr42J3p"
                },
                "href": "https://api.spotify.com/v1/albums/0tWckYjFI6ioZptLr42J3p",
                "id": "0tWckYjFI6ioZptLr42J3p",
                "images": [
                    {
                        "height": 640,
                        "url": "https://i.scdn.co/image/ab67616d0000b273bb7f4860ea8f7f6515756252",
                        "width": 640,
                    },
                    {
                        "height": 300,
                        "url": "https://i.scdn.co/image/ab67616d00001e02bb7f4860ea8f7f6515756252",
                        "width": 300,
                    },
                    {
                        "height": 64,
                        "url": "https://i.scdn.co/image/ab67616d00004851bb7f4860ea8f7f6515756252",
                        "width": 64,
                    },
                ],
                "name": "Birthplace",
                "release_date": "2018-10-19",
                "release_date_precision": "day",
                "total_tracks": 10,
                "type": "album",
                "uri": "spotify:album:0tWckYjFI6ioZptLr42J3p",
            },
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/0rZp7G3gIH6WkyeXbrZnGi"
                    },
                    "href": "https://api.spotify.com/v1/artists/0rZp7G3gIH6WkyeXbrZnGi",
                    "id": "0rZp7G3gIH6WkyeXbrZnGi",
                    "name": "Novo Amor",
                    "type": "artist",
                    "uri": "spotify:artist:0rZp7G3gIH6WkyeXbrZnGi",
                }
            ],
            "available_markets": ["AD", "CA", "GB"],  # truncated for testing purposes
            "disc_number": 1,
            "duration_ms": 234080,
            "explicit": False,
            "external_ids": {"isrc": "GB45A1801029"},
            "external_urls": {
                "spotify": "https://open.spotify.com/track/5PzWVmfzu7rePAuFkxPQf0"
            },
            "href": "https://api.spotify.com/v1/tracks/5PzWVmfzu7rePAuFkxPQf0",
            "id": "5PzWVmfzu7rePAuFkxPQf0",
            "is_local": False,
            "name": "Repeat Until Death",
            "popularity": 72,
            "preview_url": "https://p.scdn.co/mp3-preview/f40d26ba35f4a7068f5290e610bb42d173fa8a73?cid=d5e8c13c03c74750be767d2c6d82e850",
            "track_number": 9,
            "type": "track",
            "uri": "spotify:track:5PzWVmfzu7rePAuFkxPQf0",
        }
        self.track = Mock()
        self.track.configure_mock(id="0rZp7G3gIH6WkyeXbrZnGi", hello="lol")

    def test_parse_track_info(self):
        self.assertIsNotNone(parse_track_info(self.test_spotify_track_info))

    def test_get_track_metadata(self):
        track_metadata = self.track
        self.assertEqual(track_metadata.id, "0rZp7G3gIH6WkyeXbrZnGi")


if __name__ == "__main__":
    unittest.main()
