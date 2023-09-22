from math import ceil
import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from auth import *
from config import *

if __name__ == "__main__":
    # Set up API to read User Information
    scope = "user-library-read"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
        )
    )

    username = sp.me()["id"]

    # Gather tracks into playlists
    playlists: dict[str, list[str]] = {}

    offset = 0

    results = sp.current_user_saved_tracks(result_limit, offset)

    while results["items"]:
        for item in results["items"]:
            dt_object = datetime.datetime.strptime(item["added_at"], dt_format)

            if dt_object.year < oldest_year:
                continue

            playlist_name = f"{dt_object.year}.{ceil(dt_object.month / increment)}"

            if playlist_name not in playlists:
                playlists[playlist_name] = []

            playlists[playlist_name].append(item["track"]["id"])

            print(
                f"Added to playlist "
                f"'{dt_object.year}.{ceil(dt_object.month / increment)}': "
                f"{item['track']['name']} - "
                f"{', '.join([x['name'] for x in item['track']['artists']])}"
            )

        offset += result_limit
        results = sp.current_user_saved_tracks(result_limit, offset)

    # Set up API to create playlists
    scope = "playlist-modify-private"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
        )
    )

    for playlist_name, playlist_tracks in reversed(playlists.items()):
        pl = sp.user_playlist_create(
            user=username,
            name=playlist_name + " [SpotipyLikesList]",
            public=False,
            collaborative=False,
            description="Created using SpotipyLikesList.",
        )

        sp.playlist_add_items(playlist_id=pl["id"], items=playlist_tracks)

    total_tracks = sum(len(x) for x in playlists.values())
    print(f"Added {total_tracks} tracks to {len(playlists)} playlists.")
