import unix2base62

import json
import base64
import os
import re

from pathlib import Path
from datetime import date

file_name = os.getenv("FILE_NAME")
m3u8_url = os.getenv("M3U8_URL")
video_only = os.getenv("VIDEO_ONLY")
audio_only = os.getenv("AUDIO_ONLY")
cookies = os.getenv("TC_COOKIES")

info_json = 'info.json'
path = Path(info_json)

if path.is_file():
  with open(info_json, 'r') as openfile:
    response = json.load(openfile)
else:
  os.system("python tclivedl_check.py")
  with open(info_json, 'r') as openfile:
    response = json.load(openfile)

user_id = response['url'].split("/")[1]
stream_id = response['url'].split("/")[3]
stream_url = f"https://twitcasting.tv/{user_id}/metastream.m3u8/?mode=source"
cover_url = f"https://ssl.twitcasting.tv/{user_id}/thumb/{stream_id}"
user_id_safe = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "_", user_id.replace("c:",""))

today = date.today()
time_name = unix2base62.timename()

output = "%s %s [%s][%s]" % (user_id_safe, stream_id, today, time_name)

user_agent = "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36"
origin = "https://twitcasting.tv/"
referer = "https://twitcasting.tv/"
ffinit = '-stats -hide_banner -v error -thread_queue_size 8 -user_agent "%s" -headers "Cookies: %s" -headers "origin: %s" -headers "referer: %s"' % (user_agent, cookies, origin, referer)

print("downloading...")
download_cover = 'ffmpeg %s -i "%s" -c copy "DL/%s.jpg"' % (ffinit, cover_url, output)
os.system(download_cover)

print("downloading...")
download_source = 'ffmpeg %s -threads 8 -i "%s" -threads 8 -c copy -threads 8 "DL/%s.ts"' % (ffinit, stream_url, output)
os.system(download_source)

print("fixing...")
if audio_only == 'true' and video_only == 'true':
  fix_command = 'ffmpeg -hide_banner -i "DL/%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output, output)
elif audio_only == 'true':
  fix_command = 'ffmpeg -hide_banner -i "DL/%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)
elif video_only == 'true':
  fix_command = 'ffmpeg -hide_banner -i "DL/%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4"' % (output, output)
else:
  fix_command = 'ffmpeg -hide_banner -i "DL/%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)

os.system(fix_command)
cover_copy = "cp 'DL/%s.jpg' 'UL/%s.jpg'" % (output, output)

os.system(cover_copy)


