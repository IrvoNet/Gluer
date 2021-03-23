#!/usr/bin/python3
import argparse
import os
import platform
import shutil
import subprocess
import sys
import uuid

from random import randrange
from time import gmtime, strftime

is_windows = 'Windows' == platform.system()
ffmpeg = 'ffmpeg.exe' if is_windows else 'ffmpeg'
ffprobe = 'ffprobe.exe' if is_windows else 'ffprobe'

videos = []
audios = []

prefix = str(uuid.uuid4())[0:8]
tmpcut = os.path.join('tmp', '%s-cut.mp4' % prefix)
tmpout = os.path.join('tmp', '%s-out.mp4' % prefix)
tmptmp = os.path.join('tmp', '%s-tmp.mp4' % prefix)


def _get_next_video():
    video = videos.pop(0)
    videos.append(video)
    return video


def _get_video_duration(filepath):
    result = subprocess.run(
        [ffprobe, '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return int(float(result.stdout))


def _cut_video(filepath, start_offset, duration):
    # usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...
    # -v loglevel         set logging level "-v error"
    # -y                  overwrite output files
    # -an                 disable audio
    # -ss time_off        set the start time offset
    # -t duration         record or transcode "duration" seconds of audio/video
    # -vf filter_graph    set video filters
    scale = '1920:1080' # 1280:720
    cmd = '''%s -hide_banner -v error -y \
            -an -i "%s" \
            -vf "scale=%s:force_original_aspect_ratio=decrease,pad=%s:-1:-1:color=black" \
            -ss %s -t %s %s'''
    os.system(cmd % (
        ffmpeg,
        filepath, 
        scale, scale, 
        strftime('%H:%M:%S', gmtime(start_offset)),
        strftime('%H:%M:%S', gmtime(duration)), 
        tmpcut
    ))


def _add_fade_effects():
    duration = _get_video_duration(tmpcut) - 1
    cmd = '''%s -hide_banner -v error -y \
            -i %s \
            -vf "fade=type=in:duration=1,fade=type=out:duration=1:start_time=%s" \
            -c:a copy %s''' % (ffmpeg, tmpcut, duration, tmptmp)
    os.system(cmd)
    _rename(tmptmp, tmpcut)


def _concat_videos():
    if not os.path.isfile(tmpout):
        _rename(tmpcut, tmpout)
    else:
        try:
            cmd = '''%s -hide_banner -v error -y \
                    -fflags +discardcorrupt \
                    -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s'''
            os.system(cmd % (ffmpeg, tmpcut, '%s.ts' % tmpcut))
            os.system(cmd % (ffmpeg, tmpout, '%s.ts' % tmpout))

            os.system('''%s -hide_banner -v error -y \
                        -i "concat:%s.ts|%s.ts" \
                        -c copy %s''' % (ffmpeg, tmpout, tmpcut, tmpout))
            os.unlink('%s.ts' % tmpcut)
            os.unlink('%s.ts' % tmpout)
        except:
            # Windows
            os.system('''%s -hide_banner -v error -y \
                        -i "concat:%s|%s" \
                        -c copy %s''' % (ffmpeg, tmpout, tmpcut, tmpout))


def _add_music():
    audio = audios.pop()
    os.system('''%s -hide_banner -v error \
                -i %s -i "%s" -map 0:v -map 1:a -c:v copy \
                -shortest \
                -metadata title="Gluer by IrvoNet" \
                %s''' % (ffmpeg, tmpout, audio, tmptmp))
    _rename(tmptmp, tmpout)


def _run():
    cut_length = 10
    iterations = len(videos)
    duration = _get_video_duration(audios[0])
    print('Music duration: %s seconds' % duration)

    cut_length = duration / len(videos)
    if cut_length > 15:
        cut_length /= 2
        iterations *= 2
    print('Chunk duration: %s seconds' % int(cut_length))

    print('Processed 0%', end='\r')
    for counter in range(iterations):
        video = _get_next_video()
        duration = _get_video_duration(video)
        max_range = int(duration - cut_length)
        start_seconds = max_range > 0 and randrange(max_range) or 0

        _cut_video(video, start_seconds, cut_length)
        _add_fade_effects()
        _concat_videos()
        print('Processed %s%%' % int((counter + 1) / (iterations + 1) * 100), end='\r')

    _add_music()
    print('Processed 100%')
    print('Output duration is %s seconds' % _get_video_duration(tmpout))


def _find_media(src):
    if src and os.path.isdir(src):
        src = os.path.abspath(src)
        dirs = os.listdir(src)
        for filename in dirs:
            ext = os.path.splitext(filename)[1]
            filepath = os.path.join(src, filename)
            if '.mp4' == ext: videos.append(filepath)
            elif '.mp3' == ext: audios.append(filepath)
        print('Found %s video and %s audio files' % (len(videos), len(audios)))
    else:
        print('No such directory: "%s"' % src)

def _rename(src: str, dst: str):
    """Renames the file `src` to `dst`.

    Args:
        src: A source file path.
        dst: A new file path.

    See: https://docs.python.org/3/library/os.html#os.rename
    """
    if os.path.isfile(src):
        os.path.isfile(dst) and os.unlink(dst)
        os.rename(src, dst)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='The path to the folder with video and audio files.')
    parser.add_argument(
        '-output', metavar='path', default='output.mp4', 
        help='The path to the output file (default: output.mp4).')
    args = parser.parse_args()

    _find_media(args.input)
    if videos and audios:
        os.path.isdir('tmp') or os.makedirs('tmp')
        os.path.isfile(args.output) and os.unlink(args.output)
        _run()
        _rename(tmpout, args.output)
        shutil.rmtree('tmp')
    else:
        print('No video or audio files to process.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Aborted')
    exit(0)
