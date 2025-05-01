import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO

def album(results):
    album_list = []
    for row in results['items']:
        album_id = row['id']
        album_name =row['name']
        album_total_track =row['total_tracks']
        album_external_url =row['external_urls']['spotify']
        album_release_date =row['release_date']
        album_artist_id = ', '.join(artist['id'] for artist in row['artists'])
        album_artist_name =', '.join(artist['name'] for artist in row['artists'])
        album_element = {'album_id':album_id, 'album_name':album_name, 'album_total_track':album_total_track, 'album_external_url':album_external_url,
                        'album_release_date': album_release_date, 'album_artist_id': album_artist_id, 'album_artist_name':album_artist_name}
        album_list.append(album_element)
    return album_list

def artists(results):
    album_artist_list = []
    for row in results['items']:
        for key, value in row.items():
            if key=="artists":
                for artist in value:
                    album_element = {'album_artist_id': artist['id'], 'album_artist_name':artist['name'], 'album_artist_external_url':artist['external_urls']['spotify']}
                    album_artist_list.append(album_element)
    return album_artist_list



def lambda_handler(event, context):
    s3= boto3.client('s3')
    Bucket = "spotify-etl-project-sachin-dhotre"
    key = "raw_data/to_processed/"
    spotify_data=[]
    spotify_key=[]
    for file in s3.list_objects(Bucket=Bucket, Prefix=key)['Contents']:
        if file['Key'].endswith('.json'):
            response = s3.get_object(Bucket=Bucket, Key=file['Key'])
            content = response['Body']
            jsonContent = json.loads(content.read())
            spotify_data.append(jsonContent)
            spotify_key.append(file['Key'])
    
    for data in spotify_data:
        album_list = album(data)
        artist_list = artists(data)

        album_df = pd.DataFrame.from_dict(album_list)
        album_df = album_df.drop_duplicates(subset=['album_id'])


        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset=['album_artist_id'])

        album_df['album_release_date']= pd.to_datetime(album_df['album_release_date'])

        album_key= "transformed_data/album_data/album_tranformed_" + str(datetime.now()) + ".csv"
        album_buffer=StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
        print("Album data loaded successfully")

        artist_key= "transformed_data/artist_data/artist_tranformed_" + str(datetime.now()) + ".csv"
        artist_buffer=StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)
        print("Artist data loaded successfully")

    s3_resource = boto3.resource('s3')
    for key in spotify_key:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, "raw_data/processed/"+key.split('/')[-1])
        s3_resource.Object(Bucket, key).delete()
        print("Raw data moved to processed folder")





        
            

    
    
