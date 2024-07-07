# Youtube Transcript Generator
## Description
## Getting Started

- Rename the file named `config.ini.example` to `config.ini`.
- Open the file and replace `YOUR_YOUTUBE_API_KEY` with your actual API key.
  - See instructions below for obtaining a Youtube Data API Key

### Obtaining a Youtube Data API Key

- Step 1: Create a Google Cloud Project
  - Go to the Google Cloud Console: Google Cloud Console.
    - https://console.cloud.google.com/
- Create a new project:
  - Click on the project dropdown at the top of the page.
  - Click on "New Project."
  - Enter the project name and select your billing account (if required).
  - Click "Create."
- Step 2: Enable the YouTube Data API
  - Navigate to the API Library:
    - In the Google Cloud Console, click on the hamburger menu (three horizontal lines) in the upper left corner.
    - Select "APIs & Services" and then "Library."
    - Search for the YouTube Data API:
    - In the API Library, search for "YouTube Data API v3."
    - Click on the "YouTube Data API v3" result.
  - Enable the API:
    - Click the "Enable" button to enable the YouTube Data API for your project.
- Step 3: Create API Credentials
  - Navigate to the Credentials Page:
  - After enabling the API, click on the "Create Credentials" button.
  - Alternatively, you can go to "APIs & Services" -> "Credentials" in the left-hand menu.
  - Create an API Key:
    - Click on the "Create credentials" dropdown and select "API key."
  - Your API key will be created and displayed. Copy this key and keep it secure.
