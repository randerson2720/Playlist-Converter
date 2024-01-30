import requests
import json
from ytmusicapi import YTMusic

# access token
ACCESS_TOKEN = ''

# playlist id
playlist_id = "p.AWXoLZ4HPAq1eD"
# API endpoint
get_playlist_api = f'https://api.music.apple.com/v1/me/library/playlists/{playlist_id}'

# no longer have an authorization token due to having to pay $99
headers = {
    'Authorization': 'BEARER ACCESS_TOKEN'
}

response = requests.get(get_playlist_api, headers=headers)

# check to see if request was successful
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
    apple_music_playlist = response.json
    # save data
    with open('playlist_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
else:
    print("Failed to fetch the data: ", response.status_code)

# get the track data (song name and artist)
tracks = [(track['attributes']['name'], track['attributes']['artistName'])
          for track in apple_music_playlist['data'][0]['relationships']['tracks']['data']]

# authenticate youtube music
ytmusic = YTMusic('oauth.json')

# Create a new playlist in youtube music
playlist_name = apple_music_playlist['data'][0]['attributes']['name']
playlist_description = "Transferred from Apple Music"
new_playlist_id = ytmusic.create_playlist(playlist_name, playlist_description)

# add each track on youtube music and add it to the youtube playlist
for track_name, artist_name in tracks:
    search_results = ytmusic.search(f"{track_name} {artist_name}")
    for result in search_results:
        if result['resultType'] == 'song':
            ytmusic.add_playlist_items(new_playlist_id, [result['videoId']])
            # adds the first matching song and moves on to the next one
            break

# test
print("Playlist transferred successfully.")

