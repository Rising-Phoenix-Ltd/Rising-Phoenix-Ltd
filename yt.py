import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'web_client_yt.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def upload_vid_to_yt(title, description, file):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    request_body = {
        'snippet': {
            'categoryI': 20,
            'title': title,
            'description': description,
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(file)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

# upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

# service.thumbnails().set(
#     videoId=response_upload.get('id'),
#     media_body=MediaFileUpload('thumbnail.png')
# ).execute()
