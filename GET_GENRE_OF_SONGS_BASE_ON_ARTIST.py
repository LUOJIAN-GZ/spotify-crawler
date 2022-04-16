import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
import os
import numpy as np
import pandas as pd
file_name='genre_data'
df=pd.read_csv('features_crawl_from_webapi.csv',usecols=[2])
data=df['SongID'].values.tolist()
os.environ['SPOTIPY_CLIENT_ID']='CLIENT_ID'
os.environ['SPOTIPY_CLIENT_SECRET']='CLIENT_SECRET'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

data_temp=[]
artist_temp=[]
data_raw=[]
count=0
total_count=0
for i in data:
    data_raw.append(i)
    data_temp.append('spotify:track:'+i)
    count+=1
    total_count+=1
    if count==50:
        count=0
        result=spotify.tracks(data_temp)
        temp_song_result=[]
        for track in result['tracks']:
            temp_song_result.append((track['id'],track['artists'][0]['id']))
            artist_temp.append('spotify:artist:'+track['artists'][0]['id'])
        song_df = pd.DataFrame(temp_song_result, columns=["SongID", "artist1"])

        result=spotify.artists(artist_temp)

        temp_artist_result=[]
        for artist in result['artists']:
            if artist['genres']:
                temp_artist_result.append((artist['id'],artist['genres'][0]))
            else:
                artist['genres'].append('Unknow')
        artist_df = pd.DataFrame(temp_artist_result, columns=["artist2", "genre"])
        song_artist=''
        artist_df.drop_duplicates(subset='artist2',keep='first',inplace=True)
        song_artist = pd.merge(song_df, artist_df, how='left', left_on='artist1', right_on='artist2')
        song_artist.drop(['artist1','artist2'],axis=1,inplace=True)
        with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
            song_artist.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')
        print(total_count)
        data_temp=[]
        artist_temp=[]
        data_raw=[]
        song_df=''
        artist_df=''
else:
    result = spotify.tracks(data_temp)
    temp_song_result = []
    for track in result['tracks']:
        temp_song_result.append((track['id'], track['artists'][0]['id']))
        artist_temp.append('spotify:artist:' + track['artists'][0]['id'])
    song_df = pd.DataFrame(temp_song_result, columns=["SongID", "artist1"])

    result = spotify.artists(artist_temp)

    temp_artist_result = []
    for artist in result['artists']:
        if artist['genres']:
            temp_artist_result.append((artist['id'], artist['genres'][0]))
        else:
            artist['genres'].append('Unknow')
    artist_df = pd.DataFrame(temp_artist_result, columns=["artist2", "genre"])
    song_artist = ''
    artist_df.drop_duplicates(subset='artist2', keep='first', inplace=True)
    song_artist = pd.merge(song_df, artist_df, how='left', left_on='artist1', right_on='artist2')
    song_artist.drop(['artist1', 'artist2'], axis=1, inplace=True)
    with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
        song_artist.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')
    print(total_count)
    data_temp = []
    artist_temp = []
    data_raw = []
    song_df = ''
    artist_df = ''
