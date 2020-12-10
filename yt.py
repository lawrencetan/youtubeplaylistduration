from googleapiclient.discovery import build
import os
import re
from datetime import timedelta

api_key=os.environ.get('api_key')

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds=0

nextPageToken = None

while True:
	pl_request = youtube.playlistItems().list(
	         part='contentDetails',
	         #modify to playlist ID
		     playlistId="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
	         maxResults=50,
	         pageToken=nextPageToken
	        )

	pl_response=pl_request.execute()

	# print(pl_response)
	# print ('xxxxxxxxxx')
	vid_ids = []

	for item in pl_response['items']:
		vid_ids.append(item['contentDetails']['videoId'])

	# print(vid_ids)
	# print(','.join(vid_ids))
	# print()

	vid_request = youtube.videos().list(
			part='contentDetails',
			id=','.join(vid_ids)
		)

	vid_response = vid_request.execute()

	# print(vid_response)
	# print()


	for item in vid_response['items']:
		duration = item['contentDetails']['duration']
		
		hours = hours_pattern.search(duration)
		minutes = minutes_pattern.search(duration)
		seconds = seconds_pattern.search(duration)
		
		hours = int(hours.group(1)) if hours else 0
		minutes = int(minutes.group(1)) if minutes else 0
		seconds = int(seconds.group(1)) if seconds else 0

		video_seconds = timedelta(
				hours = hours, 
				minutes = minutes, 
				seconds = seconds, 
			).total_seconds()


		#print(duration)
		#print(video_seconds)
		#print(hours, minutes, seconds)
		#print()
		#print (pl_response.get('nextPageToken'))
		total_seconds += video_seconds

	#check if there's any page left in the playlist response
	nextPageToken = pl_response.get('nextPageToken')

	if not nextPageToken:
		break

total_seconds = int(total_seconds)
#print(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'Total time of playlist: {hours} hours {minutes} minutes {seconds} seconds')


