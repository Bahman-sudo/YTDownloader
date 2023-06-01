import customtkinter as ctk
from pytube import YouTube, exceptions
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("500x200")

        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text="YTDownloader", font=("Lucida Sans", 24))
        self.label.pack(padx=8, pady=12)

        self.textbox = ctk.CTkEntry(master=self.frame, placeholder_text="Enter a YouTube Video URL", width=500, font=("Lucida Sans", 18))
        self.textbox.pack(padx=8, pady=12)

        self.button = ctk.CTkButton(master=self.frame, text="Download", font=("Lucida Sans", 18), command=self.process)
        self.button.pack(padx=8, pady=12)

        self.root.mainloop()

    def clearframe(self):
        for widget in self.frame.pack_slaves(): widget.destroy()

    def done(self):
        self.clearframe()
        label = ctk.CTkLabel(master=self.frame, text="Finished downloading! Check your downloads folder.", font=("Lucida Sans", 14), anchor=ctk.CENTER)
        label.pack(padx=8, pady=12)

    def process(self):
        yt = None
        try: yt = YouTube(self.textbox.get())
        except exceptions.RegexMatchError:
            self.clearframe()
            label = ctk.CTkLabel(master=self.frame, text="No such video exists.", font=("Lucida Sans", 18))
            label.pack(padx=8, pady=12)
            return
        self.ask_type(yt)

    def ask_type(self, yt):
        def b1_action():
            yd = yt.streams.get_highest_resolution()
            download(yd, "video")

        def b2_action():
            yd = yt.streams.get_audio_only()
            download(yd, "audio")

        def download(stream, stream_type):
            folder_path = filedialog.askdirectory(title="Select Folder")
            if stream_type == "audio":
                audio_file_name = f"{yt.title}.mp3"
                stream.download(output_path=folder_path, filename=audio_file_name)
            else: stream.download(output_path=folder_path)
            self.done()

        for widget in self.frame.winfo_children(): widget.destroy()

        label = ctk.CTkLabel(master=self.frame, text="Would you like to save it as a video or audio file?", font=("Lucida Sans", 14))
        label.pack(padx=8, pady=12)

        button1 = ctk.CTkButton(master=self.frame, text="Video", command=b1_action, font=("Lucida Sans", 18))
        button1.pack(padx=10, pady=10, side="bottom")

        button2 = ctk.CTkButton(master=self.frame, text="Audio", command=b2_action, font=("Lucida Sans", 18))
        button2.pack(padx=10, pady=10, side="bottom")

App()
