# YTP Deluxe Edition (Tkinter)

YTP Deluxe Edition is a Python/Tkinter front-end for a Windows 7/8.1-compatible YouTube Poop (YTP) editor. It provides:

- Source browsers for video, audio, image/GIF files plus a list for online URLs.
- Toggleable audio/video effects (random sound, reverse, speed up/down, chorus, vibrato, and resource overlays).
- Randomized clip generator with configurable clip duration, count, and effect probability.
- FFmpeg-based export pipeline with FFplay preview support.

## Project Layout

```
Main.py
Utilities.py
YTPGenerator.py
ytpplus/
  EffectsFactory.py
sources/
temp/
sounds/
music/
resources/
output/
```

`Utilities.ToolBox` auto-creates required folders, including resource subfolders:

- `resources/images`
- `resources/memes`
- `resources/meme_sounds`
- `resources/sounds`
- `resources/overlay_videos`
- `resources/adverts`
- `resources/errors`
- `resources/spadinner`
- `resources/spadinner_sounds`

It also creates placeholders for `resources/intro.mp4` and `resources/outro.mp4`.
If those files contain media, they are automatically prepended/appended during concat.

## Running

```
python Main.py
```

FFmpeg (ffmpeg, ffprobe, ffplay) should be available on the PATH.
