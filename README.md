# Spotipy Likes List

Creates Spotify playlists from your liked tracks, grouped chronologically.

## Setup

### Authentication

Requires setting up an app through
the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) as follows:

1. Copy "auth_example.py" and rename it to "auth.py"
2. Create a new app in the Spotify Developer Dashboard
3. Paste the "Client ID" into auth.py.
4. Paste the "Client Secret" into auth.py.
5. Go to "Edit Settings" and add "http://localhost:8888/" to "Redirect URIs".

## User Config

- ```oldest_year```: Set this to stop playlists containing liked tracks added in a year older than
  the specified value being created.

- ```increment```: Size of the grouping of playlists, in months.

## Run

Run using "SpotipyLikesList.py"

## Credits

Created by [Dale Collison](https://github.com/dcollison) using
the [Spotipy Library](https://spotipy.readthedocs.io/en/master/).

