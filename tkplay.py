"""
pygame/tkinter version of basic music player
"""
import tomllib
import tkinter as tk
import tkinter.filedialog as fd
import pygame
from pathlib import Path
from functools import partial
from os import chdir, environ


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.MUSIC_END = pygame.USEREVENT + 1
        self.track = tk.StringVar()
        self.status = tk.StringVar()
        ## gui ##
        self.load_toml()
        ### partialization ###
        self.plase_init()
        self.place_frames()
        ###!only (not)works for Win10/11 ###
        environ["SDL_WINDOWID"] = str(self.embedframe.winfo_id())
        environ["SDL_VIDEODRIVER"] = "windib"
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        pygame.display.flip()

        # buttons
        self.place_buttons()
        # songs list
        scroll_y = tk.Scrollbar(self.songsframe, orient=tk.VERTICAL)
        self.playlist = tk.Listbox(
            self.songsframe,
            yscrollcommand=scroll_y.set,
            selectbackground=self.primary_color,
            selectmode=tk.SINGLE,
            font=("Victor Mono", 10, "bold"),
            bg=self.secondary_color,
            fg=self.acsent_color,
            bd=5,
            relief=tk.GROOVE,
        )

        # set path
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=tk.BOTH, expand=True)
        path = fd.askdirectory()
        path_to_music = Path(path)
        chdir(path_to_music)
        songs = [f for f in path_to_music.iterdir() if f.is_file()]
        for track in songs:
            self.playlist.insert(tk.END, track.parts[-1])
        self.playlist.bind("<Double-Button-1>", self.playsong)

    def plase_init(self):
        self.root.title("Music Player")
        self.root.geometry("1000x300")
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.MUSIC_END)

    def load_toml(self):
        with open("settings.toml", "rb") as toml:
            data = tomllib.load(toml)
        # load GUI colors
        colors = data["colors"]
        self.text_color = colors["text"]
        self.bg_color = colors["bg"]
        self.primary_color = colors["primary"]
        self.acsent_color = colors["acsent"]
        self.secondary_color = colors["secondary"]

    def place_frames(self):
        frame = partial(
            tk.LabelFrame,
            master=self.root,
            font=("Victor Mono", 15, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            bd=5,
            relief=tk.GROOVE,
        )

        self.trackframe = frame(text="Track")
        self.buttonframe = frame(text="Control Panel")
        self.songsframe = frame(text="Playlist")
        self.embedframe = frame(text="Test")
        self.trackframe.place(x=0, y=0, width=600, height=100)
        self.buttonframe.place(x=0, y=200, width=600, height=100)
        self.embedframe.place(x=0, y=100, width=600, height=100)
        self.songsframe.place(x=600, y=0, width=400, height=300)

    def place_buttons(self):
        button = partial(
            tk.Button,
            master=self.buttonframe,
            width=2,
            height=1,
            font=("Victor Mono", 20),
            fg=self.primary_color,
            bg=self.bg_color,
            bd=0,
            activebackground=self.secondary_color,
            activeforeground=self.acsent_color,
        )
        self.playbtn = button(text="\u23F5", command=self.playsong)
        self.playbtn.grid(row=0, column=0, padx=5, pady=5)
        stopbtn = button(text="\u23F9", command=self.stopsong)
        stopbtn.grid(row=0, column=1, padx=5, pady=5)

    def place_lables(self):
        label = partial(
            tk.Label,
            master=self.trackframe,
            anchor=tk.W,
            textvariable=self.track,
            font=("Victor Mono", 24, "bold"),
            bg=self.bg_color,
            fg=self.acsent_color,
        )
        songtrack = label(width=20).grid(row=0, column=0, padx=10, pady=5)
        trackstatus = label(textvariable=self.status).grid(
            row=0, column=1, padx=10, pady=5
        )

    def playsong(self, *args):
        self.track.set(self.playlist.get(tk.ACTIVE))
        self.status.set("is playing")
        pygame.mixer.music.load(self.playlist.get(tk.ACTIVE))
        pygame.mixer.music.play()
        self.playbtn.configure(command=self.pausesong, text="\u23F8")

    def stopsong(self):
        self.status.set("")
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.playbtn.configure(command=self.playsong, text="\u23F5")

    def pausesong(self):
        self.status.set("-Paused")
        pygame.mixer.music.pause()
        self.playbtn.configure(command=self.unpausesong, text="\u23F5")

    def unpausesong(self):
        self.status.set("-Playing")
        pygame.mixer.music.unpause()
        self.playbtn.configure(command=self.pausesong, text="\u23F8")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                print("music end event")
                self.status = ""
            # for search TODO: delete after binding
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    fd.askdirectory()
            self.root.after(100, self.check_events)

    def run(self):
        self.check_events()

    def equalizer(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    app.run()
    root.mainloop()
