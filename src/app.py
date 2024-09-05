import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import seaborn as sns

# Hardcoded Spotify credentials
client_id = "e750458ec4d74c7b9ff9b79ae180225d"
client_secret = "be9fb56906844d088cae082c232b08b8"

# Initialize Spotify client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Lindsey Stirling's Spotify artist URI
artist_uri = "spotify:artist:378dH6EszOLFShpRzAQkVM"

# Fetch albums
results = spotify.artist_albums(artist_uri, album_type='album')
albums = results['items']

while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

# Create a list to store all tracks
all_tracks = []
# Fetch tracks for each album
for album in albums:
    album_tracks = spotify.album_tracks(album['id'])
    
    for track in album_tracks['items']:
        # Get track details including popularity
        track_info = spotify.track(track['id'])
        
        all_tracks.append({
            'name': track['name'],
            'album': album['name'],
            'popularity': track_info['popularity'],
            'duration_ms': track['duration_ms']
        })

# Convert to DataFrame
df = pd.DataFrame(all_tracks)

# Sort by popularity in descending order and get top 3
top_3_songs = df.sort_values('popularity', ascending=False).head(3)

print("Top 3 most popular songs:")
print(top_3_songs)

# Print all album names
print("\nAll albums:")
for album in set(df['album']):
    print(album)

# Convert duration from milliseconds to minutes
df['duration_min'] = df['duration_ms'] / 60000

# Create the scatter plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='duration_min', y='popularity')
plt.title("Song Duration vs. Popularity for Lindsey Stirling's Tracks")
plt.xlabel("Duration (minutes)")
plt.ylabel("Popularity")

# Add a trend line
sns.regplot(data=df, x='duration_min', y='popularity', scatter=False, color='red')

plt.tight_layout()
plt.savefig('duration_vs_popularity.png')
plt.close()

# Calculate correlation
correlation = df['duration_min'].corr(df['popularity'])

print(f"Correlation between duration and popularity: {correlation:.2f}")
print(f"\nNumber of tracks analyzed: {len(df)}")
print(f"Average duration: {df['duration_min'].mean():.2f} minutes")
print(f"Average popularity: {df['popularity'].mean():.2f}")

# Display top 5 most popular songs with their durations
top_5 = df.sort_values('popularity', ascending=False).head()
print("\nTop 5 most popular songs:")
print(top_5[['name', 'popularity', 'duration_min']])

# Display 5 least popular songs with their durations
bottom_5 = df.sort_values('popularity', ascending=True).head()
print("\n5 least popular songs:")
print(bottom_5[['name', 'popularity', 'duration_min']])
