import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
use_ffmpeg = os.getenv("USE_FFMPEG")

output = "%s [%s]" % (file_name, unix2base62.timename())
# metadata = '-metadata:g encoding_tool="GA.00.00"'
download_command = 'streamlink --retry-open 3 --retry-streams 30 --retry-max 300 --stream-segment-threads 8 --force-progress -o "output/%s.ts" "%s" best' % (output, m3u8_url)
os.system(download_command)
