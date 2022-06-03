import requests
import unix2base62

import json
import base64
import os

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
cookies = os.getenv("TC_COOKIES")


b64_site = "dHdpdGNhc3RpbmcudHY="
tw_site = base64.b64decode(b64).decode("ascii")
tw_url = f"https://{tw_site}/userajax.php?c=islive&u={user_id}"

response = requests.get(url).json()

user_id = response['url'].split("/")[1]
stream_id = response['url'].split("/")[3]
today = date.today()
time_name = unix2base62.timename()
user_id_safe = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "_", user_id.replace("c:",""))

output = "%s %s [%s][%s]" % (user_id_safe, stream_id, today, time_name)

args = '-l info --retry-open 3 --retry-streams 30 --retry-max 300 --stream-segment-threads 8 --force-progress --http-cookie "%s" -o "%s.ts" "%s"' % (cookies, output, m3u8_url)

download_command = 'streamlink %s best' % (args)
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
