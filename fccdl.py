import os

url = os.getenv("URL")
audio_only = os.getenv("AUDIO_ONLY")

args = '--threads 8 --wait --log-level debug -o "output/(%(channel_id)s)_[%(date)s]_%(channel_name)s_%(title)s.%(ext)s" ' + url

if audio_only == 'true':
  download_command = 'sudo fc2-live-dl --quality sound %s ' % (args)
else:
  download_command = 'sudo fc2-live-dl -x --wait-for-quality-timeout 15 %s ' % (args)

os.system(download_command)

# if audio_only == 'true' and video_only == 'true':
#   fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output, output)
# elif audio_only == 'true':
#   fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)
# elif video_only == 'true':
#   fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -c copy -map_metadata -1 -movflags +faststart "UL/%s.mp4"' % (output, output)
# else:
#   fix_command = 'sudo ffmpeg -hide_banner -i "%s.ts" -vn -c:a copy -map_metadata -1 -movflags +faststart "UL/%s.m4a"' % (output, output)

# os.system(fix_command)
