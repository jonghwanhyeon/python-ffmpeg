import asyncio
from ffmpeg import FFmpeg

# pip install ffpb

ffmpeg = (
  FFmpeg(executable='ffpb') # Tells FFmpeg we want to use a custom executable
  .input('video_lng.mp4')
  .output('out.mp4')
)

@ffmpeg.on('stderr')
def on_stderr(line):
  try:
    # p = line.split(':')[1].split('%')[0].lstrip() # get percentage
    p = line.split(':')[1].split('|')[1] # get a progressbar
  except:
    p = ''
  print(f'\r[{p}]', end='')

@ffmpeg.on('error')
def on_error(code):
  print('Error:', code)

@ffmpeg.on('completed')
def on_completed():
  print('\nCompleted')

asyncio.run(ffmpeg.execute())