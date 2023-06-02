import customtkinter as ctk
from pytube import YouTube, exceptions
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("500x200")
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.create_label("self.label", "YTDownloader", 24)
        self.textbox = ctk.CTkEntry(master=self.frame, placeholder_text="Enter a YouTube Video URL", width=500, font=("Lucida Sans", 18))
        self.textbox.pack(padx=8, pady=12)
        self.create_button("self.button", "Download", 18, self.process)
        self.root.mainloop()

    def clearframe(self):
        for widget in self.frame.pack_slaves(): widget.destroy()

    def create_label(self, name, text, size):
        globals()[name] = ctk.CTkLabel(master=self.frame, text=text, font=("Lucida Sans", size))
        globals()[name].pack(padx=8, pady=12)

    def create_button(self, name, text, size, command):
        globals()[name] = ctk.CTkButton(master=self.frame, text=text, command=command, font=("Lucida Sans", size))
        globals()[name].pack(padx=8, pady=12)

    def rerun(self):
        self.root.destroy()
        self.__init__()

    def done(self):
        self.clearframe()
        self.create_label("self.label", "Finished Downloading! Would you like to download another video?", 14)
        self.create_button("self.button3", "Yes", 18, self.rerun)
        self.create_button("self.button4", "No", 18, self.root.quit)

    def process(self):
        self.yt = None
        try: self.yt = YouTube(self.textbox.get())
        except exceptions.RegexMatchError:
            self.clearframe()
            self.create_label("self.label", "No such video exists", 18)
            return
        self.ask_type(self.yt)

    def b1_action(self):
        yd = self.yt.streams.get_highest_resolution()
        self.download(yd, "video")
    
    def b2_action(self):
        yd = self.yt.streams.get_audio_only()
        self.download(yd, "audio")

    def download(self, stream, stream_type):
            folder_path = filedialog.askdirectory(title="Select Folder")
            folder_path = folder_path.replace("\\", "/")
            if stream_type == "audio":
                audio_file_name = f"{self.yt.title}.mp3"
                stream.download(output_path=folder_path, filename=audio_file_name)
            else: stream.download(output_path=folder_path)
            self.done()        

    def ask_type(self, yt):
        for widget in self.frame.winfo_children(): widget.destroy()
        self.create_label("self.label", "Would you like to save it as a video or audio file?", 14)
        self.create_button("self.button1", "Video", 18, self.b1_action)
        self.create_button("self.button2", "Audio", 18, self.b2_action)

App()
