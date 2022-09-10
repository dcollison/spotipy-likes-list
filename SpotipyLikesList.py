from math import ceil
from auth import *
from config import *
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up API to read User Information
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

# Get Username
username = sp.me()['id']

# Go through liked tracks and add information to lists
years, quarters, track_ids = [], [], []
offset = 0
results = sp.current_user_saved_tracks(result_limit,offset)
while results['items'] != []:
    for idx, item in enumerate(results['items']):
        dt_object = datetime.datetime.strptime(item['added_at'],dt_format)
        if dt_object.year >= oldest_year:
            years.append(dt_object.year)
            quarters.append(ceil(dt_object.month/increment))
            track_ids.append(item['track']['id'])
            print("To be added to playlist \"{}.{}\": {} - {}".format(dt_object.year, ceil(dt_object.month/3), item['track']['artists'][0]['name'], item['track']['name']))
    offset += result_limit
    results = sp.current_user_saved_tracks(result_limit,offset)

# Set up API to create playlists
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

# Go through liked tracks found and add them to the appropriate playlist
existing_playlists = {}
for i in range(len(years)):
    playlist_name = "{}.{}".format(years[i],quarters[i])
    if playlist_name not in existing_playlists.keys():
        this_playlist = sp.user_playlist_create(user=username,name=playlist_name + " [SpotipyLikesList]",public=False,collaborative=False,description='Created using Spotipylist.')
        existing_playlists[playlist_name] = this_playlist['id']
    sp.user_playlist_add_tracks(user=username,playlist_id=existing_playlists[playlist_name], tracks=[track_ids[i]])

print("Added {} tracks to {} playlists.".format(len(track_ids), len(existing_playlists)))