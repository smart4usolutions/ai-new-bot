import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES)

credentials = flow.run_local_server(port=0)

youtube = googleapiclient.discovery.build(
    "youtube", "v3", credentials=credentials)

video_folder = "videos"

for i in range(1,4):

    video_file = f"{video_folder}/short{i}.mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"Daily AI News #{i}",
                "description": "Latest AI news in 60 seconds 🚀",
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
