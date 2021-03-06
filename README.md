# Gluer

This program makes it easy to create great videos by combining random chunks from other videos.

## Prerequisite
To build and run this application, you will need the following tools:

- [python](https://www.python.org/downloads/) - Python is an interpreted, high-level and general-purpose programming language.
- [ffpmeg](https://ffmpeg.org/download.html) - A complete, cross-platform solution to record, convert and stream audio and video.
  - Ubuntu: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: [download exe files](https://ffmpeg.org/download.html#build-windows) and add it to the [`PATH` environment variable](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))


## Usage
```bash
usage: gluer [-h] [-output path] input

positional arguments:
  input         The path to the folder with video and audio files.

optional arguments:
  -h, --help    show this help message and exit
  -output path  The path to the output file (default: output.mp4).
```

## Example
Get 5 to 10 videos from [Pexels](https://www.pexels.com/search/videos/cloud/):

![Pexels Screenshot](screenshots/pexels-screenshot.png)

Get 1 audio from [YouTube Audio Library](https://youtube.com/audiolibrary):

![Pexels Screenshot](screenshots/youtube-audio-library.png)

Put all of them to the same folder (e.g. `/tmp/src`):

![Pexels Screenshot](screenshots/finder-src-folder.png)

Open Terminal, navigate to the Gluer folder and run the following command:

```bash
./gluer -output /tmp/output.mp4 /tmp/src
```

The result of the manipulation above is available on YouTube:

[![Video Screenshot](https://img.youtube.com/vi/wGfS8M6qrnw/0.jpg)](https://www.youtube.com/watch?v=wGfS8M6qrnw)
