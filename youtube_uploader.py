import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

creds = None

# Load existing token
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# If no valid credentials available, login once
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    # Save token for future runs
    with open("token.json", "w") as token:
        token.write(creds.to_json())

youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

video_folder = "videos"

for i in range(2,3):

    video_file = f"{video_folder}/short{i}.mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"Daily AI News #{i} #Shorts",
                "description": "Latest AI news in 60 seconds 🚀\n\n#AI #TechNews #Shorts",
                "tags": ["AI", "Artificial Intelligence", "Tech News"],
                "categoryId": "28"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(video_file)
    )

    response = request.execute()

    print(f"✅ Uploaded {video_file}")
