import os
import unix2base62

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
use_ffmpeg = os.getenv("USE_FFMPEG")

output = "%s [%s]" % (file_name, unix2base62.timename())
# metadata = '-metadata:g encoding_tool="GA.00.00"'
if(use_ffmpeg):
  download_command = 'ffmpeg -i "%s" -c copy %s.ts' % (m3u8_url, output)
else:
  download_command = 'streamlink -o "%s.ts" %s best' % (output, m3u8_url)
os.system(download_command)

if audio_only == video_only:
  fix_command = 'ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output, output)
elif audio_only == 'true':
  fix_command = 'ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)
elif video_only == 'true':
  fix_command = 'ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4"' % (output, output)
else:
  fix_command = 'ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)

os.system(fix_command)
