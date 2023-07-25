"""
pygame/tkinter version of basic music player
"""
import tkinter as tk
import pygame
from pathlib import Path
from functools import partial
from os import chdir


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1000x200")
        pygame.init()
        pygame.mixer.init()
        self.MUSIC_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.track = tk.StringVar()
        self.status = tk.StringVar()
        # GUI colors:
        self.text_color = "#f0f0f0"
        self.bg_color = "#050505"
        self.primary_color = "#ff602c"
        self.acsent_color = "#c3d491"
        self.secondary_color = "#1f250e"
        ## gui ##
        ### partialization ###
        frame = partial(
            tk.LabelFrame,
            master=self.root,
            font=("Victor Mono", 15, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            bd=5,
            relief=tk.GROOVE,
        )
        grid = partial
        trackframe = frame(text="Track")
        buttonframe = frame(text="Control Panel")
        songsframe = frame(text="Playlist")
        trackframe.place(x=0, y=0, width=600, height=100)
        buttonframe.place(x=0, y=100, width=600, height=100)
        songsframe.place(x=600, y=0, width=400, height=200)
        label = partial(
            tk.Label,
            master=trackframe,
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
        # buttons
        button = partial(
            tk.Button,
            master=buttonframe,
            width=2,
            height=1,
            font=("Victor Mono", 20),
            fg=self.primary_color,
            bg=self.bg_color,
            bd=0,
            activebackground=self.secondary_color,
            activeforeground=self.acsent_color,
        )
        tk.Button()
        self.playbtn = button(text="\u23F5", command=self.playsong)
        self.playbtn.grid(row=0, column=0, padx=5, pady=5)
        stopbtn = button(text="\u23F9", command=self.stopsong)
        stopbtn.grid(row=0, column=1, padx=5, pady=5)
        # songs list
        scroll_y = tk.Scrollbar(songsframe, orient=tk.VERTICAL)
        self.playlist = tk.Listbox(
            songsframe,
            yscrollcommand=scroll_y.set,
            selectbackground="#B0FC38",
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
        self.playlist.pack(fill=tk.BOTH)
        path_to_music = Path("D:\Музыка\Phone")
        chdir(path_to_music)
        songs = [f for f in path_to_music.iterdir() if f.is_file()]
        for track in songs:
            self.playlist.insert(tk.END, track.parts[-1])
        self.playlist.bind("<Double-Button-1>", self.playsong)

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
            root.after(100, self.check_events)


root = tk.Tk()
MusicPlayer(root).check_events()
root.mainloop()
