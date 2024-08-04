import os
import argparse
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from unidecode import unidecode

def get_api_key():
    return os.environ.get('YOUTUBE_API_KEY')

youtube = build("youtube", "v3", developerKey=get_api_key())

def get_video_id_from_url(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed\/|v\/|youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:watch\?v=)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if response["items"]:
            return response["items"][0]["snippet"]["title"]
    except Exception as e:
        print(f"Error retrieving video title: {e}")
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None

def slugify(text):
    text = unidecode(text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text

def save_transcript_to_file(title, transcript):
    os.makedirs("transcripts", exist_ok=True)
    slugified_title = slugify(title)
    filename = f"transcripts/{slugified_title}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcript saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving transcript: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Transcript Extractor")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    if not get_api_key():
        print("YouTube API key not found in environment variables.")
        return

    video_id = get_video_id_from_url(args.url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    title = get_video_title(video_id)
    if title:
        print(f"Title: {title}")
    else:
        print("Could not retrieve video title")
        return

    transcript = get_transcript(video_id)
    if transcript:
        if save_transcript_to_file(title, transcript):
            print("Transcript extracted and saved successfully.")
        else:
            print("Failed to save transcript.")
    else:
        print("Could not retrieve video transcript")
        # Ensure the directory exists before creating the file
        os.makedirs("transcripts", exist_ok=True)
        with open("transcripts/.no_transcript", "w") as f:
            f.write(f"No transcript available for video: {args.url}")
        print("Created .no_transcript file")

if __name__ == "__main__":
    main()
