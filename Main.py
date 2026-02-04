import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from Utilities import ToolBox, YTPSettings
from YTPGenerator import YTPGenerator


class YTPDeluxeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YTP Deluxe Edition (Tkinter)")
        self.geometry("1080x720")
        self.minsize(980, 640)

        self.tool_box = ToolBox()
        self.settings = YTPSettings()
        self.sources = []
        self.image_sources = []
        self.audio_sources = []
        self.url_sources = []

        self._build_ui()
        self.tool_box.ensure_project_structure()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew")

        self.sources_tab = ttk.Frame(notebook, padding=12)
        self.effects_tab = ttk.Frame(notebook, padding=12)
        self.output_tab = ttk.Frame(notebook, padding=12)
        self.advanced_tab = ttk.Frame(notebook, padding=12)

        notebook.add(self.sources_tab, text="Sources")
        notebook.add(self.effects_tab, text="Effects")
        notebook.add(self.output_tab, text="Output")
        notebook.add(self.advanced_tab, text="Advanced")

        self._build_sources_tab()
        self._build_effects_tab()
        self._build_output_tab()
        self._build_advanced_tab()

    def _build_sources_tab(self):
        self.sources_tab.columnconfigure(1, weight=1)

        sources_frame = ttk.LabelFrame(self.sources_tab, text="Local Video Sources", padding=8)
        sources_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        sources_frame.columnconfigure(0, weight=1)

        self.source_list = tk.Listbox(sources_frame, height=8)
        self.source_list.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        buttons_frame = ttk.Frame(sources_frame)
        buttons_frame.grid(row=0, column=1, sticky="ns", padx=4, pady=4)

        ttk.Button(buttons_frame, text="Add Videos", command=self._add_videos).grid(
            row=0, column=0, sticky="ew", pady=2
        )
        ttk.Button(buttons_frame, text="Remove Selected", command=self._remove_selected_source).grid(
            row=1, column=0, sticky="ew", pady=2
        )

        image_frame = ttk.LabelFrame(self.sources_tab, text="Images / GIFs", padding=8)
        image_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        image_frame.columnconfigure(0, weight=1)

        self.image_list = tk.Listbox(image_frame, height=6)
        self.image_list.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        ttk.Button(image_frame, text="Add Images", command=self._add_images).grid(
            row=0, column=1, sticky="ns", padx=4
        )

        audio_frame = ttk.LabelFrame(self.sources_tab, text="Audio Sources", padding=8)
        audio_frame.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)
        audio_frame.columnconfigure(0, weight=1)

        self.audio_list = tk.Listbox(audio_frame, height=6)
        self.audio_list.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        ttk.Button(audio_frame, text="Add Audio", command=self._add_audio).grid(
            row=0, column=1, sticky="ns", padx=4
        )

        urls_frame = ttk.LabelFrame(self.sources_tab, text="Online URLs", padding=8)
        urls_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        urls_frame.columnconfigure(0, weight=1)

        self.url_entry = ttk.Entry(urls_frame)
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        ttk.Button(urls_frame, text="Register URL", command=self._add_url).grid(
            row=0, column=1, sticky="ew", padx=4, pady=4
        )

        self.url_list = tk.Listbox(urls_frame, height=5)
        self.url_list.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

    def _build_effects_tab(self):
        effects_frame = ttk.LabelFrame(self.effects_tab, text="Toggleable Effects", padding=8)
        effects_frame.pack(fill="both", expand=True)

        self.effect_vars = []
        effect_names = self.settings.effect_names()
        for idx, name in enumerate(effect_names):
            var = tk.BooleanVar(value=self.settings.effects_enabled[idx])
            self.effect_vars.append(var)
            ttk.Checkbutton(effects_frame, text=name, variable=var).grid(
                row=idx // 2, column=idx % 2, sticky="w", padx=8, pady=2
            )

        probabilities_frame = ttk.LabelFrame(self.effects_tab, text="Effect Probability", padding=8)
        probabilities_frame.pack(fill="x", pady=8)

        ttk.Label(probabilities_frame, text="Effect Probability (%)").grid(row=0, column=0, sticky="w")
        self.effect_probability = tk.IntVar(value=self.settings.effect_probability)
        ttk.Scale(probabilities_frame, from_=0, to=100, variable=self.effect_probability, orient="horizontal").grid(
            row=0, column=1, sticky="ew", padx=6
        )
        probabilities_frame.columnconfigure(1, weight=1)

        ttk.Label(probabilities_frame, text="Max Effect Stack Level").grid(row=1, column=0, sticky="w")
        self.max_stack = tk.IntVar(value=self.settings.max_stack_level)
        ttk.Spinbox(probabilities_frame, from_=1, to=10, textvariable=self.max_stack, width=6).grid(
            row=1, column=1, sticky="w", padx=6
        )

    def _build_output_tab(self):
        output_frame = ttk.LabelFrame(self.output_tab, text="Output Settings", padding=8)
        output_frame.pack(fill="x", pady=4)

        ttk.Label(output_frame, text="Output File").grid(row=0, column=0, sticky="w")
        self.output_entry = ttk.Entry(output_frame)
        self.output_entry.insert(0, "output/ytp_deluxe.mp4")
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(output_frame, text="Browse", command=self._browse_output).grid(row=0, column=2, padx=4)

        output_frame.columnconfigure(1, weight=1)

        clip_frame = ttk.LabelFrame(self.output_tab, text="Clip Controls", padding=8)
        clip_frame.pack(fill="x", pady=4)

        self.min_duration = tk.DoubleVar(value=self.settings.min_clip_duration)
        self.max_duration = tk.DoubleVar(value=self.settings.max_clip_duration)
        self.clip_count = tk.IntVar(value=self.settings.max_clips)

        ttk.Label(clip_frame, text="Min Clip Duration (s)").grid(row=0, column=0, sticky="w")
        ttk.Entry(clip_frame, textvariable=self.min_duration, width=8).grid(row=0, column=1, sticky="w")

        ttk.Label(clip_frame, text="Max Clip Duration (s)").grid(row=0, column=2, sticky="w", padx=(16, 0))
        ttk.Entry(clip_frame, textvariable=self.max_duration, width=8).grid(row=0, column=3, sticky="w")

        ttk.Label(clip_frame, text="Clip Count").grid(row=1, column=0, sticky="w")
        ttk.Spinbox(clip_frame, from_=1, to=70000, textvariable=self.clip_count, width=8).grid(
            row=1, column=1, sticky="w"
        )

        self.progress = ttk.Progressbar(self.output_tab, mode="determinate")
        self.progress.pack(fill="x", pady=6)

        action_frame = ttk.Frame(self.output_tab)
        action_frame.pack(fill="x", pady=4)

        ttk.Button(action_frame, text="Preview (FFplay)", command=self._preview).pack(
            side="left", padx=4
        )
        ttk.Button(action_frame, text="Generate YTP", command=self._generate).pack(
            side="right", padx=4
        )

    def _build_advanced_tab(self):
        advanced_frame = ttk.LabelFrame(self.advanced_tab, text="Advanced Options", padding=8)
        advanced_frame.pack(fill="both", expand=True)

        self.insert_transition = tk.BooleanVar(value=self.settings.insert_transition_clips)
        self.allow_stacking = tk.BooleanVar(value=self.settings.allow_effect_stacking)
        self.preserve_audio = tk.BooleanVar(value=self.settings.preserve_original_audio)

        ttk.Checkbutton(
            advanced_frame,
            text="Insert Transition Clips from sources/ (probability-based)",
            variable=self.insert_transition,
        ).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Checkbutton(
            advanced_frame,
            text="Allow Effect Stacking",
            variable=self.allow_stacking,
        ).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Checkbutton(
            advanced_frame,
            text="Preserve Original Audio Under Overlays",
            variable=self.preserve_audio,
        ).grid(row=2, column=0, sticky="w", pady=2)

        ttk.Label(advanced_frame, text="Transition Probability (1-100)").grid(row=3, column=0, sticky="w", pady=2)
        self.transition_probability = tk.IntVar(value=self.settings.transition_probability)
        ttk.Spinbox(advanced_frame, from_=1, to=100, textvariable=self.transition_probability, width=8).grid(
            row=3, column=1, sticky="w", padx=4
        )

        ttk.Label(advanced_frame, text="Preset Label").grid(row=4, column=0, sticky="w", pady=2)
        self.preset_label = ttk.Entry(advanced_frame)
        self.preset_label.insert(0, self.settings.ytp_effects_name)
        self.preset_label.grid(row=4, column=1, sticky="w", padx=4)

    def _add_videos(self):
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[("Video Files", "*.mp4 *.wmv *.avi *.mkv")],
        )
        for file in files:
            self.sources.append(file)
            self.source_list.insert(tk.END, file)

    def _add_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.gif")],
        )
        for file in files:
            self.image_sources.append(file)
            self.image_list.insert(tk.END, file)

    def _add_audio(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[("Audio", "*.mp3 *.wav *.ogg")],
        )
        for file in files:
            self.audio_sources.append(file)
            self.audio_list.insert(tk.END, file)

    def _add_url(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        self.url_sources.append(url)
        self.url_list.insert(tk.END, url)
        self.url_entry.delete(0, tk.END)

    def _remove_selected_source(self):
        selection = list(self.source_list.curselection())
        for index in reversed(selection):
            self.sources.pop(index)
            self.source_list.delete(index)

    def _browse_output(self):
        file = filedialog.asksaveasfilename(
            title="Output File",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")],
        )
        if file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file)

    def _preview(self):
        output_file = self.output_entry.get().strip()
        if not output_file:
            messagebox.showwarning("Output Missing", "Please choose an output file.")
            return
        try:
            self.tool_box.preview(output_file)
        except FileNotFoundError:
            messagebox.showerror("FFplay Missing", "FFplay not found. Please install FFmpeg.")

    def _generate(self):
        if not self.sources:
            messagebox.showwarning("No Sources", "Please add at least one source video.")
            return

        output_file = self.output_entry.get().strip()
        self._sync_settings()

        generator = YTPGenerator(
            util=self.tool_box,
            output=output_file,
            min_dur=self.settings.min_clip_duration,
            max_dur=self.settings.max_clip_duration,
            max_clips=self.settings.max_clips,
            insert_transition_clips=self.settings.insert_transition_clips,
            transition_probability=self.settings.transition_probability,
            effect_probability=self.settings.effect_probability,
            allow_effect_stacking=self.settings.allow_effect_stacking,
            max_stack_level=self.settings.max_stack_level,
            effects=self.settings.effects_enabled,
        )
        for source in self.sources:
            generator.add_source(source)

        self.progress["value"] = 0
        try:
            generator.go(progress_callback=self._update_progress)
            messagebox.showinfo("YTP Deluxe", "Generation complete.")
        except Exception as exc:
            messagebox.showerror("YTP Deluxe", f"Generation failed: {exc}")

    def _update_progress(self, value):
        self.progress["value"] = value
        self.update_idletasks()

    def _sync_settings(self):
        self.settings.min_clip_duration = float(self.min_duration.get())
        self.settings.max_clip_duration = float(self.max_duration.get())
        self.settings.max_clips = int(self.clip_count.get())
        self.settings.effect_probability = int(self.effect_probability.get())
        self.settings.max_stack_level = int(self.max_stack.get())
        self.settings.insert_transition_clips = self.insert_transition.get()
        self.settings.allow_effect_stacking = self.allow_stacking.get()
        self.settings.transition_probability = int(self.transition_probability.get())
        self.settings.preserve_original_audio = self.preserve_audio.get()
        self.settings.ytp_effects_name = self.preset_label.get().strip() or "Default"
        self.settings.effects_enabled = [var.get() for var in self.effect_vars]


if __name__ == "__main__":
    app = YTPDeluxeApp()
    app.mainloop()
