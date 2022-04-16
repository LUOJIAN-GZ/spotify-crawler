import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np
import pandas as pd
file_name='features_crawl_from_webapi'
os.environ['SPOTIPY_CLIENT_ID']='CLIENT_ID'
os.environ['SPOTIPY_CLIENT_SECRET']='SECRET'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

df  =pd.read_csv('2022-03-16-23-15-32_EXPORT_CSV_4995691_521_0.csv',usecols=[1,2,3])#chunksize定义一次读取的块的大小，即一次读取多少行数据


df=df.drop_duplicates(['Title','Artist','SongID'])
    # data=np.array(chunk)
    # final=data.tolist()
#77007
j=100
i=0
while j<77300:
    data_raw=df[i:j]
    data=np.array(data_raw)
    final=data.tolist()

    song_id=[]
    for l in final:
        song_id.append(l[2])
    results = spotify.audio_features(tracks=song_id)
    final_result=[]
    for m in results:
        if m==None:
            m={}
        final_result.append(m)
    final_df = pd.DataFrame(final_result, columns=["danceability", "energy", "key", "loudness", "mode", "speechiness","acousticness","instrumentalness","liveness","valence","tempo","type","id","uri","track_href","analysis_url","duration_ms","time_signature"])
    finals=pd.merge(data_raw,final_df,how='left',left_on='SongID',right_on='id')
    if finals.shape[0]!=100:
        print('HERE NOT RIGHT!!!!!!!!',j)
        print('HERE NOT RIGHT!!!!!!!!',j)
        print('HERE NOT RIGHT!!!!!!!!',j)
        print('HERE NOT RIGHT!!!!!!!!',j)
        print('HERE NOT RIGHT!!!!!!!!',j)

    with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
        finals.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')
    i+=100
    j+=100
    print(j)

# final = []
# with open(f"{file_name}.csv", "a+", newline='', encoding='utf-8-sig') as csvfile:
#     final_df.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig', mode='a')

# os.environ['SPOTIPY_CLIENT_ID']='db9ba27ceda54319a79f39a12d1fd080'
# os.environ['SPOTIPY_CLIENT_SECRET']='0d9471b5bd3a43e5ade9dca886066df0'
#
# #SPOTIPY_REDIRECT_URI='your-app-redirect-url'
#
# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
#
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# results = spotify.audio_features(tracks=['1riPE3NCV1OBmSXqpYiMJY'])
#
# print(results)
