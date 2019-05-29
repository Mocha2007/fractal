cd %~dp0
ffmpeg -f image2 -r 30 -i %05d.png -vcodec libx264 -crf 0 -preset veryslow -c:a libmp3lame -b:a 320k newton.mp4
exit