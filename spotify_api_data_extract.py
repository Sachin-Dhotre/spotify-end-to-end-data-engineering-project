import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os 
import boto3
from datetime import datetime


def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    # Authenticate with correct argument names
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    # Example playlist ID
    uri='spotify:artist:5fvTHKKzW44A9867nPDocM'
    spotify_data = sp.artist_albums(uri, album_type='album')

    filename = 'spotify_data_' + str(datetime.now()) + '.json'
   
    client = boto3.client('s3')
    client.put_object(Body=json.dumps(spotify_data), Bucket="spotify-etl-project-sachin-dhotre", Key="raw_data/to_processed/" + filename)