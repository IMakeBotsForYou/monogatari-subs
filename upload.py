from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
import google_auth_oauthlib.flow
import google.oauth2.credentials
import os
from time import sleep
from datetime import date
# --- CONFIG ---
CLIENT_SECRETS_FILE = "client_secret.json"  # OAuth2 credentials file
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
PLAYLIST_ID = "PL8zzso6aYp-BTpdl_1wWnegY92sDXBkbp"
SRT_FOLDER = "./"  # folder containing VIDEO_ID.srt files
# ---------------

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server()
    return build("youtube", "v3", credentials=creds)

def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append(item["contentDetails"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)
    return videos

def delete_japanese_captions(youtube, video_id):
    request = youtube.captions().list(
        part="snippet",
        videoId=video_id
    )
    response = request.execute()
    for item in response.get("items", []):
        lang = item["snippet"]["language"]
        if lang == "ja":
            cap_id = item["id"]
            print(f"Deleting old JP captions for {video_id}")
            youtube.captions().delete(id=cap_id).execute()

def upload_caption(youtube, video_id, filepath):
    media = MediaFileUpload(filepath, mimetype="application/octet-stream", resumable=True)
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "language": "ja",
                "name": f"Japanese {date.today()}",
                "videoId": video_id,
                "isDraft": False
            }
        },
        media_body=media
    )
    response = request.execute()
    print(f"Uploaded JP captions for {video_id}: {response['id']}")

import re

def sanitize_title(title: str) -> str:
    """Make a safe filename from a video title."""
    # Remove illegal characters for filenames
    safe = re.sub(r'[\\/*?:"<>|-]', "", title).replace("   ", " - ")
    # Strip spaces at ends
    safe = safe.strip()
    return safe

def get_videos_from_playlist(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="contentDetails,snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((video_id, title))
        request = youtube.playlistItems().list_next(request, response)
    return videos

def main():
    youtube = get_authenticated_service()
    videos = get_videos_from_playlist(youtube, PLAYLIST_ID)
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    countdown(12 * HOUR)
    for video_id, title in videos[22:]:
        safe_title = sanitize_title(title)
        srt_path = os.path.join(SRT_FOLDER, f"{safe_title}.srt")

        print(f"Looking for SRT: {srt_path}")

        if not os.path.exists(srt_path):
            print(f"⚠ No SRT for '{title}' ({video_id}), skipping.")
            continue

        delete_japanese_captions(youtube, video_id)
        upload_caption(youtube, video_id, srt_path)

import sys

def format_time(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

def countdown(seconds):
    for remaining in range(seconds, -1, -1):
        sys.stdout.write(f"\rTime left: {format_time(remaining)}")
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write("\rTime's up!            \n")  # overwrite the line         \n")  # Add spaces to overwrite the previous text

if __name__ == "__main__":
    main()
