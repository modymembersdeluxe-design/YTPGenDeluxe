import random
import subprocess
from pathlib import Path


class EffectsFactory:
    def __init__(self, tool_box):
        self.tool_box = tool_box

    def pick_sound(self):
        files = list(Path(self.tool_box.getSOUNDS()).glob("*.mp3"))
        return str(random.choice(files))

    def pick_source(self):
        files = list(Path(self.tool_box.getSOURCES()).glob("*.mp4"))
        return str(random.choice(files))

    def pick_music(self):
        files = list(Path(self.tool_box.getMUSIC()).glob("*.mp3"))
        return str(random.choice(files))

    def run_ffmpeg(self, *args):
        subprocess.run(["ffmpeg", *args, "-v", "warning", "-nostdin", "-y"], check=True)

    def run_magick(self, *args):
        subprocess.run(["magick", *args], check=True)

    def effect_random_sound(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-i",
                self.pick_sound(),
                "-filter_complex",
                "[0:a]channelsplit=channel_layout=stereo[a1][a2];"
                "[1:a]volume=1,apad,channelsplit=channel_layout=stereo[a3][a4];"
                "[a1][a2][a3][a4]amerge=inputs=4,pan=stereo|c0<c0+c2|c1<c1+c3[out]",
                "-ac",
                "2",
                "-map",
                "0:v",
                "-map",
                "[out]",
                "-shortest",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_random_sound_mute(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-i",
                self.pick_sound(),
                "-filter_complex",
                "[1:a]volume=1,apad[aud]",
                "-map",
                "0:v",
                "-map",
                "[aud]",
                "-shortest",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_reverse(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "reverse", "-af", "areverse", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_speed_up(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-filter:v", "setpts=0.5*PTS", "-filter:a", "atempo=2.0", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_slow_down(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-filter:v", "setpts=2*PTS", "-filter:a", "atempo=0.5", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_chorus(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-af",
                "aecho=0.8:0.88:60:0.4",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_vibrato(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-af",
                "vibrato=f=6.5",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_low_pitch(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-filter:v",
                "setpts=2*PTS",
                "-af",
                "asetrate=44100*0.5,aresample=44100",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_high_pitch(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-filter:v",
                "setpts=0.5*PTS",
                "-af",
                "asetrate=44100*2,aresample=44100",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_dance(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "scale=iw*1.1:ih*1.1,eq=contrast=1.2", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_squidward(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "hue=s=0,eq=brightness=0.05", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_invert(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "negate", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_rainbow(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "hue=H=2*PI*t", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_flip(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "hflip", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_mirror(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-vf",
                "split[left][right];[left]hflip[left];[left][right]hstack",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_sus(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-af",
                "asetrate=44100*1.15,atempo=0.9",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_stutter_loop(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-filter_complex",
                "[0:v]tpad=stop_mode=clone:stop_duration=0.1[v];"
                "[0:a]aloop=loop=3:size=4410[a]",
                "-map",
                "[v]",
                "-map",
                "[a]",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)

    def effect_loop_frames(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "loop=loop=2:size=30:start=0", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_shuffle_frames(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg("-i", str(temp), "-vf", "shuffleframes=0:1:2:3", str(video))
        finally:
            temp.unlink(missing_ok=True)

    def effect_audio_crust(self, video):
        temp = Path(self.tool_box.getTempVideoName())
        Path(video).rename(temp)
        try:
            self.run_ffmpeg(
                "-i",
                str(temp),
                "-af",
                "volume=8,highpass=f=200,lowpass=f=3000",
                str(video),
            )
        finally:
            temp.unlink(missing_ok=True)
