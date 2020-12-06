from googleapiclient.discovery import build
import os

api_key=os.environ.get('api_key')

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
            part='statistics',
           # forUsername='schafer5',
            forUsername='NetworkChuck',
        )

response=request.execute()

print(response)
