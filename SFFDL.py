import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
use_ffmpeg = os.getenv("USE_FFMPEG")

output = "%s [%s]" % (file_name, unix2base62.timename())
# metadata = '-metadata:g encoding_tool="GA.00.00"'
if use_ffmpeg == 'true':
  download_command = 'ffmpeg -hide_banner -i "%s" -c copy "%s.ts"' % (m3u8_url, output)
elif audio_only == 'true':
  download_command = 'streamlink --retry-open 3 --retry-streams 30 --retry-max 300 --stream-segment-threads 8 --force-progress -o "%s.ts" "%s" audio_only,audio_opus,audio,best' % (output, m3u8_url)
else:
  download_command = 'streamlink --retry-open 3 --retry-streams 30 --retry-max 300 --stream-segment-threads 8 --force-progress -o "%s.ts" "%s" best' % (output, m3u8_url)
os.system(download_command)

if audio_only == 'true' and video_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output, output)
elif audio_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)
elif video_only == 'true':
  fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4"' % (output, output)
else:
  fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)

os.system(fix_command)
