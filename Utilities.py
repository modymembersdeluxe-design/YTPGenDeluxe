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
    effects_enabled: list[bool] = field(default_factory=lambda: [True] * 29)

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

    def concat_demuxer(self, output_file):
        concat_file = Path(self.temp_dir) / "concat.txt"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                output_file,
            ],
            check=True,
        )

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
