import spotipy
import sys
import spotipy.util as util
import json
import os

songListUri = []
masterListUri = []
newUri = []
master = ''

username = '1218957434'

scope = "playlist-modify-public"
token = util.prompt_for_user_token(username, scope, client_id='', client_secret='', redirect_uri='https://www.spotify.com/')
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
print('Successfully logged in')

playlists = spotifyObject.user_playlists(user, limit=50, offset=0)

for playlist in playlists['items']:
    playlistId = playlist['id']
    results = spotifyObject.playlist(playlist_id, fields='tracks, next, name')
    playlistName = results['name']
    
    if '--' not in playlistName:
        print('------------------------')
        print('Playlist Name ' + playlistName)
        tracks = results['tracks']
        tempLen = []
        for track in tracks['items']:
            trackName = track['track']['name']
            trackuri = track['track']['id']
            if playlistName == 'MasterPlaylist':
                masterListUri.append(trackuri)
                master = playlist['id']
            else:
                songListUri.append(trackuri)
            tempLen.append(trackuri)

        while tracks['next']:
            tracks = spotifyObject.next(tracks)
            for track in tracks['items']:
                trackName = track['track']['name']
                trackuri = track['track']['id']
                if playlistName == 'MasterPlaylist':
                    masterListUri.append(trackuri)
                elif trackuri not in songListUri:
                    songListUri.append(trackuri)
                tempLen.append(trackuri)
        print(len(tempLen))

print(len(songListUri))
print(master)

spotifyObject.trace = False
for uri in songListUri:
    if uri not in masterListUri and uri != None:
        if len(newUri) < 100:
            if uri == '4bXERByegZZubIis3htEcQ?si=4adf41042f374bf0':
                print('Cloud Generator Found')
        newUri.append(uri)
        else:
            print('Adding array to Spotify')
            #adding tracks
            spotifyObject.user_playlist_add_tracks(username, master, newUri)
            newUri.clear()
if len(newUri) > 0:
    spotifyObject.user_playlist_add_tracks(username, master, newUri)
    newUri.clear()

