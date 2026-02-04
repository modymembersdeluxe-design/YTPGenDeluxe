import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class YTPSettings:
    min_clip_duration: float = 0.2
    max_clip_duration: float = 0.4
    max_clips: int = 20
    insert_transition_clips: bool = True
    transition_probability: int = 15
    effect_probability: int = 30
    allow_effect_stacking: bool = True
    max_stack_level: int = 3
    preserve_original_audio: bool = True
    ytp_effects_name: str = "Default"
    effects_enabled: list[bool] = field(default_factory=lambda: [True] * 30)

    def effect_names(self):
        return [
            "Random Sound",
            "Random Sound (Mute OG)",
            "Reverse Clip",
            "Speed Up",
            "Slow Down",
            "Chorus Effect",
            "Vibrato / Pitch Bend",
            "High Pitch",
            "Low Pitch",
            "Dance Mode",
            "Squidward Mode",
            "Invert Colors",
            "Rainbow Overlay",
            "Flip / Mirror",
            "Mirror Mode",
            "Sus Effect",
            "Stutter Loop",
            "Loop Frames",
            "Shuffle Frames",
            "Audio Crust",
            "Image Overlay (resources/images)",
            "Meme Overlay (resources/memes)",
            "Meme Sound (resources/meme_sounds)",
            "Resource Sound Mix (resources/sounds)",
            "Overlay Video (resources/overlay_videos)",
            "Advert Overlay (resources/adverts)",
            "Error/Glitch Overlay (resources/errors)",
            "Spadinner Overlay (resources/spadinner)",
            "Spadinner Sound (resources/spadinner_sounds)",
            "YTP Generated Chaos (small export)",
        ]


class ToolBox:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or os.getcwd())
        self.sources_dir = self.base_dir / "sources"
        self.temp_dir = self.base_dir / "temp"
        self.sounds_dir = self.base_dir / "sounds"
        self.music_dir = self.base_dir / "music"
        self.resources_dir = self.base_dir / "resources"
        self.output_dir = self.base_dir / "output"

        self.resource_subfolders = [
            "images",
            "memes",
            "meme_sounds",
            "sounds",
            "overlay_videos",
            "adverts",
            "errors",
            "spadinner",
            "spadinner_sounds",
        ]

    def ensure_project_structure(self):
        for folder in [
            self.sources_dir,
            self.temp_dir,
            self.sounds_dir,
            self.music_dir,
            self.resources_dir,
            self.output_dir,
        ]:
            folder.mkdir(parents=True, exist_ok=True)

        for name in self.resource_subfolders:
            (self.resources_dir / name).mkdir(parents=True, exist_ok=True)

        for file_name in ["intro.mp4", "outro.mp4"]:
            path = self.resources_dir / file_name
            if not path.exists():
                path.touch()

    def get_temp(self):
        return str(self.temp_dir)

    def getTempVideoName(self):
        return str(self.temp_dir / "temp.mp4")

    def getSOURCES(self):
        return str(self.sources_dir)

    def getSOUNDS(self):
        return str(self.sounds_dir)

    def getMUSIC(self):
        return str(self.music_dir)

    def get_resources_dir(self):
        return str(self.resources_dir)

    def get_resource_subdir(self, name):
        return str(self.resources_dir / name)

    def build_concat_file(self, clip_paths, include_intro_outro=True):
        concat_file = Path(self.temp_dir) / "concat.txt"
        with open(concat_file, "w", encoding="utf-8") as file_handle:
            if include_intro_outro:
                intro = self.resources_dir / "intro.mp4"
                if intro.exists() and intro.stat().st_size > 0:
                    file_handle.write(f"file '{intro.as_posix()}'\n")

            for clip_path in clip_paths:
                file_handle.write(f"file '{Path(clip_path).as_posix()}'\n")

            if include_intro_outro:
                outro = self.resources_dir / "outro.mp4"
                if outro.exists() and outro.stat().st_size > 0:
                    file_handle.write(f"file '{outro.as_posix()}'\n")
        return str(concat_file)

    def preview(self, output_file):
        subprocess.run(["ffplay", output_file], check=True)

    def copy_video(self, source, dest):
        shutil.copyfile(source, dest)

    def snip_video(self, source, start, end, dest):
        duration = max(0.01, end - start)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(start),
                "-t",
                str(duration),
                "-i",
                source,
                "-c",
                "copy",
                dest,
            ],
            check=True,
        )

    def concat_demuxer(self, output_file, concat_file=None):
        concat_path = concat_file or str(Path(self.temp_dir) / "concat.txt")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_path,
                "-c",
                "copy",
                output_file,
            ],
            check=True,
        )
        if not self.has_audio_stream(output_file):
            self.add_silent_audio(output_file)

    def get_length(self, source):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                source,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def has_audio_stream(self, source):
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "a",
                "-show_entries",
                "stream=codec_type",
                "-of",
                "csv=p=0",
                source,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())

    def add_silent_audio(self, source):
        temp_path = Path(source).with_suffix(".audio.mp4")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                source,
                "-f",
                "lavfi",
                "-i",
                "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-shortest",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                str(temp_path),
            ],
            check=True,
        )
        Path(source).unlink(missing_ok=True)
        temp_path.replace(source)
