import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, date

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

uploaded_links = []

# ---------------- AUTH ---------------- #
creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

# ---------------- LOG FUNCTION ---------------- #
def log_upload(video_file, status, info=""):
    with open("upload_log.txt", "a") as log:
        log.write(f"{datetime.now()} | {video_file} | {status} | {info}\n")

# ---------------- UPLOAD ---------------- #
video_folder = "videos"

if not os.path.exists(video_folder):
    print("❌ videos folder not found")
    exit()

videos = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

if not videos:
    print("❌ No videos found")
    exit()

today = date.today()

for video in videos:
    video_file = os.path.join(video_folder, video)

    try:
        print(f"⬆ Uploading: {video_file}")

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": f"Daily AI News {today} #Shorts #AI",
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

        video_id = response.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"✅ Uploaded: {video_file}")
        print(f"🔗 URL: {video_url}")

        uploaded_links.append(video_url)
        log_upload(video_file, "SUCCESS", video_url)

    except Exception as e:
        print(f"❌ Failed: {video_file}")
        print(str(e))

        log_upload(video_file, "FAILED", str(e))

# ---------------- SAVE LINKS ---------------- #
with open("uploaded_links.txt", "a") as f:
    for link in uploaded_links:
        f.write(link + "\n")

print("🎯 Upload process completed")
