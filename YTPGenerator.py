import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor

from ytpplus.EffectsFactory import EffectsFactory


class YTPGenerator:
    def __init__(
        self,
        util,
        output,
        min_dur=0.2,
        max_dur=0.4,
        max_clips=20,
        insert_transition_clips=True,
        transition_probability=15,
        effect_probability=30,
        allow_effect_stacking=True,
        max_stack_level=3,
        effects=None,
    ):
        self.toolBox = util
        self.effectsFactory = EffectsFactory(util)
        self.sourceList = []

        self.OUTPUT_FILE = output
        self.MIN_STREAM_DURATION = min_dur
        self.MAX_STREAM_DURATION = max_dur
        self.MAX_CLIPS = max_clips

        self.insertTransitionClips = insert_transition_clips
        self.transitionProbability = transition_probability
        self.effectProbability = effect_probability

        self.allowEffectStacking = allow_effect_stacking
        self.maxEffectStackLevel = max_stack_level

        self.effects = effects or [True] * 20

        self.done = False
        self.doneCount = 0
        self.ex = None
        self.progress_callback = None

    def add_source(self, source_name):
        self.sourceList.append(source_name)

    def go(self, progress_callback=None):
        if not self.sourceList:
            print("No sources added...")
            return

        self.progress_callback = progress_callback
        if os.path.exists(self.OUTPUT_FILE):
            os.remove(self.OUTPUT_FILE)

        num_effects = self.number_effects_selected()
        job_dir = self.toolBox.get_temp()
        os.makedirs(job_dir, exist_ok=True)

        def process_clip(i):
            nonlocal num_effects
            if self.ex is not None:
                return

            try:
                clip_to_work_with = os.path.join(job_dir, f"video{i}.mp4")

                if (
                    random.randint(1, self.transitionProbability) == self.transitionProbability
                    and self.insertTransitionClips
                ):
                    self.toolBox.copy_video(self.effectsFactory.pick_source(), clip_to_work_with)
                else:
                    source_to_pick = random.choice(self.sourceList)
                    source_length = float(self.toolBox.get_length(source_to_pick))
                    start = random.uniform(0, max(0, source_length - self.MAX_STREAM_DURATION))
                    end = start + random.uniform(self.MIN_STREAM_DURATION, self.MAX_STREAM_DURATION)
                    self.toolBox.snip_video(source_to_pick, start, end, clip_to_work_with)

                self._update_progress(0.5 / (self.MAX_CLIPS + 1))

                if random.randint(0, 99) < self.effectProbability and num_effects > 0:
                    stack_level = 1
                    if self.allowEffectStacking:
                        stack_level = random.randint(1, min(num_effects, self.maxEffectStackLevel))

                    visited = [False] * 20
                    for _ in range(stack_level):
                        invalid_effect = True
                        while invalid_effect:
                            effect = random.randint(0, 19)
                            if self.effects[effect] and not visited[effect]:
                                self.apply_effect(clip_to_work_with, effect)
                                visited[effect] = True
                                invalid_effect = False

            except Exception as exc:
                print(f"YTPGEN CLIP {i} ERROR: Could not be created")
                self.ex = exc

            self._update_progress(0.5 / (self.MAX_CLIPS + 1))
            print(f"YTPGEN CLIP {i} DONE: {round(self.doneCount*100)}% Complete")

        with ThreadPoolExecutor() as executor:
            executor.map(process_clip, range(self.MAX_CLIPS))

        concat_file = os.path.join(job_dir, "concat.txt")
        with open(concat_file, "w", encoding="utf-8") as file_handle:
            for i in range(self.MAX_CLIPS):
                clip_path = os.path.join(job_dir, f"video{i}.mp4")
                if os.path.exists(clip_path):
                    file_handle.write(f"file 'video{i}.mp4'\n")

        try:
            self.toolBox.concat_demuxer(self.OUTPUT_FILE)
        finally:
            self.clean_up()
            self._update_progress(1.0 / (self.MAX_CLIPS + 1))
            print(f"YTPGEN CONCAT DONE: {round(self.doneCount*100)}% Complete")
            self.done = True

        if self.ex is not None:
            raise self.ex

    def apply_effect(self, clip, effect):
        effect_map = {
            0: self.effectsFactory.effect_random_sound,
            1: self.effectsFactory.effect_random_sound_mute,
            2: self.effectsFactory.effect_reverse,
            3: self.effectsFactory.effect_speed_up,
            4: self.effectsFactory.effect_slow_down,
            5: self.effectsFactory.effect_chorus,
            6: self.effectsFactory.effect_vibrato,
            7: self.effectsFactory.effect_high_pitch,
            8: self.effectsFactory.effect_low_pitch,
            9: self.effectsFactory.effect_dance,
            10: self.effectsFactory.effect_squidward,
            11: self.effectsFactory.effect_invert,
            12: self.effectsFactory.effect_rainbow,
            13: self.effectsFactory.effect_flip,
            14: self.effectsFactory.effect_mirror,
            15: self.effectsFactory.effect_sus,
            16: self.effectsFactory.effect_stutter_loop,
            17: self.effectsFactory.effect_loop_frames,
            18: self.effectsFactory.effect_shuffle_frames,
            19: self.effectsFactory.effect_audio_crust,
        }
        func = effect_map.get(effect)
        if func:
            func(clip)

    def clean_up(self):
        job_dir = self.toolBox.get_temp()
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)

    def number_effects_selected(self):
        return sum(self.effects)

    def _update_progress(self, increment):
        self.doneCount += increment
        if self.progress_callback:
            self.progress_callback(min(100, self.doneCount * 100))
