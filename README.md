# Gluer

This program makes it easy to create great videos by combining random chunks from other videos.

## Prerequisite
To build and run this application, you will need the following tools:

- [python](https://www.python.org/downloads/) - Python is an interpreted, high-level and general-purpose programming language.
- [ffpmeg](https://ffmpeg.org/download.html) - A complete, cross-platform solution to record, convert and stream audio and video.

## Usage
```bash
usage: gluer [-h] [-i path] [-o path]

optional arguments:
  -h, --help  show this help message and exit
  -i path     The path to the folder with video and audio files.
  -o path     The path to the output file (default: output.mp4).
```

## Example
- Get 5 videos from [Pexels](https://pexels.com/videos/)
- Get 1 audio from [YouTube Audio Library](https://youtube.com/audiolibrary)
- Put all of them to the same folder (e.g. `/tmp/src`)
- Run `./gluer.py -i /tmp/src -o output.mp4`
