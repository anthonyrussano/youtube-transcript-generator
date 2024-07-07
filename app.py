import os
import configparser
import argparse
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

# Read the API key from the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")
API_KEY = config["YouTube"]["api_key"]

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)


def get_video_id_from_url(url):
    """
    Extract the video ID from a YouTube URL.
    """
    if "v=" in url:
        return url.split("v=")[-1]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1]
    else:
        return None


def get_video_title(video_id):
    """
    Get the title of a YouTube video using its ID.
    """
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    if response["items"]:
        return response["items"][0]["snippet"]["title"]
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
        return str(e)


def save_transcript_to_file(title, transcript):
    """
    Save the transcript to a text file named after the video title.
    """
    # Clean title to create a valid filename
    valid_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"{valid_title}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transcript saved to {filename}")


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="YouTube Video Transcript Extractor")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    # Extract video ID from URL
    video_id = get_video_id_from_url(args.url)

    if not video_id:
        print("Invalid YouTube URL")
        return

    # Get video title
    title = get_video_title(video_id)
    if title:
        print(f"Title: {title}")
    else:
        print("Could not retrieve video title")

    # Get video transcript
    transcript = get_transcript(video_id)
    if transcript:
        save_transcript_to_file(title, transcript)
    else:
        print("Could not retrieve video transcript")


if __name__ == "__main__":
    main()
