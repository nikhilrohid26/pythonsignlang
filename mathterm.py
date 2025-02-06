import os
import yt_dlp
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# === CONFIGURATIONS ===
YOUTUBE_API_KEY = "AIzaSyBwLxuB1dzkasTBW-kc5D8aHVmqwNRFD1c"  # Your YouTube API Key
GOOGLE_DRIVE_CREDENTIALS = "C:/Users/Asus/OneDrive/Desktop/ProjectPY/zinc-authority-450114-m9-faa4e7a8a8e3.json"  # Path to your service account JSON file
UPLOAD_FOLDER_ID = "17b7dXxVkUPFMKFZTqzuTeU6Q_umKGvKA"  # Google Drive folder ID

# === FUNCTION TO SEARCH YOUTUBE ===
def search_youtube(math_term):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    search_response = youtube.search().list(
        q=f"{math_term} in sign language",
        part="id",
        maxResults=1,
        type="video"
    ).execute()
    
    if "items" in search_response and search_response["items"]:
        video_id = search_response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

# === FUNCTION TO DOWNLOAD VIDEO ===
def download_video(video_url, output_dir, video_name):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, f"{video_name}.%(ext)s"),
        "format": "bestvideo/best",
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# === FUNCTION TO UPLOAD VIDEO TO GOOGLE DRIVE ===
def upload_to_drive(file_path):
    creds = service_account.Credentials.from_service_account_file(GOOGLE_DRIVE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [UPLOAD_FOLDER_ID]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    return file.get("id")

# === MAIN FUNCTION ===
def main():
    # Get the user's name and greet them
    user_name = input("Please enter your name: ")
    print(f"Hello, {user_name}!")
    
    # Get the file name to save in Google Drive
    video_name = input("What should the file be saved as on Google Drive? ")
    
    video_url = "https://www.youtube.com/watch?v=Bq9Jw8ofSZ4"  # The fixed YouTube URL
    
    print(f"Downloading video from: {video_url}")
    output_directory = "MathSignVideos"
    download_video(video_url, output_directory, video_name)

    # Get the downloaded file
    video_files = os.listdir(output_directory)
    if not video_files:
        print("Download failed.")
        return
    
    # Use the correct downloaded file (webm in this case)
    video_path = os.path.join(output_directory, f"{video_name}.webm")  # Changed to .webm
    print(f"Uploading {video_name}.webm to Google Drive...")
    file_id = upload_to_drive(video_path)
    
    if file_id:
        print(f"Upload successful! Video link: https://drive.google.com/file/d/{file_id}/view")
        print(f"Thank you, {user_name}! Your video has been uploaded successfully.")
    else:
        print("Upload failed.")

if __name__ == "__main__":
    main()
