import os
import configparser
import argparse
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from unidecode import unidecode


def get_api_key():
    """
    Read the API key from the config.ini file.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["YouTube"]["api_key"]


# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=get_api_key())


def get_video_id_from_url(url):
    """
    Extract the video ID from a YouTube URL.
    """
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
    """
    Get the title of a YouTube video using its ID.
    """
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        if response["items"]:
            return response["items"][0]["snippet"]["title"]
    except Exception as e:
        print(f"Error retrieving video title: {e}")
    return None


def get_transcript(video_id):
    """
    Get the transcript of a YouTube video using its ID.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


def slugify(text):
    """
    Convert text to a URL-friendly slug.
    """
    # Convert to ASCII
    text = unidecode(text)
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


def save_transcript_to_file(title, transcript):
    """
    Save the transcript to a text file in the 'transcripts' folder using a slugified filename.
    """
    # Create 'transcripts' folder if it doesn't exist
    os.makedirs("transcripts", exist_ok=True)

    # Create slugified filename
    slugified_title = slugify(title)
    filename = f"transcripts/{slugified_title}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcript saved to {filename}")
    except Exception as e:
        print(f"Error saving transcript: {e}")


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Transcript Extractor")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

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
        save_transcript_to_file(title, transcript)
    else:
        print("Could not retrieve video transcript")


if __name__ == "__main__":
    main()
