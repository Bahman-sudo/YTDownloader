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
        self.create_switch()
        self.create_label("self.label", "YTDownloader", 24)
        self.textbox = ctk.CTkEntry(master=self.frame, placeholder_text="Enter a YouTube Video URL", width=500, font=("Lucida Sans", 18))
        self.textbox.pack(padx=8, pady=12)
        self.create_button("self.button", "Download", 18, self.process)
        self.root.mainloop()

    def clearframe(self):
        for widget in self.frame.pack_slaves(): widget.destroy()

    def set_mode(self):
        if self.switch_var.get() == "on": ctk.set_appearance_mode("dark")
        else: ctk.set_appearance_mode("light")
        
    def create_label(self, name, text, size):
        globals()[name] = ctk.CTkLabel(master=self.frame, text=text, font=("Lucida Sans", size))
        globals()[name].pack(padx=8, pady=12)

    def create_button(self, name, text, size, command):
        globals()[name] = ctk.CTkButton(master=self.frame, text=text, command=command, font=("Lucida Sans", size))
        globals()[name].pack(padx=8, pady=12)
    
    def create_textbox(self, name, text, width, size):
        globals()[name] = self.textbox = ctk.CTkEntry(master=self.frame, placeholder_text=text, width=width, font=("Lucida Sans", size))
        globals()[name].pack(padx=8, pady=12)

    def rerun(self):
        self.root.destroy()
        self.__init__()
        self.create_switch()

    def create_switch(self):
        self.switch_var = ctk.StringVar(value="on")
        self.switch = ctk.CTkSwitch(master=self.frame, text="Dark Mode", command=self.set_mode, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.pack(padx=12, pady=8)
        self.switch.place(x=0, y=125)

    def done(self, success):
        self.clearframe()
        if success:
            self.create_label("self.label", "Finished Downloading! Would you like to download another video?", 12)
        else:
            self.create_label("self.label", "Would you like to download another video?", 14)
        self.create_button("self.button3", "Yes", 18, self.rerun)
        self.create_button("self.button4", "No", 18, self.root.quit)

    def errortext(self, text):
        self.clearframe()
        self.create_label("self.label", text, 18)
        self.done(False)

    def process(self):
        self.yt = None
        try: self.yt = YouTube(self.textbox.get())
        except exceptions.RegexMatchError: self.errortext("No such video exists")
        except exceptions.AgeRestrictedError: self.errortext("The video you have provided is age restricted")
        except exceptions.LiveStreamError: self.errortext("The video you have provided is a live-stream")
        except exceptions.MaxRetriesExceeded: self.errortext("You are being rate-limited. Plese wait before trying again")
        except exceptions.VideoRegionBlocked: self.errortext("You are being geoblocked")
        except (exceptions.HTMLParseError, exceptions.ExtractError): self.errortext("The video could not be extracted from Youtube's website")
        except (exceptions.VideoUnavailable, exceptions.VideoPrivate): self.errortext("The video you have provided is unavailable")
        except Exception as e: 
            self.create_label("self.label", "This is likely an error on my end, please report on the issues page", 18)
            self.create_label("self.label", "Report the issue here: https://github.com/Bahman-sudo/YTDownloader-Broken-/issues")
            self.create_label("self.label", f"The exception in question is: {e}")
        self.ask_type()

    def download(self, stream_type):
        folder_path = filedialog.askdirectory(title="Select Folder")
        folder_path = folder_path.replace("\\", "/")
        if stream_type == "both":
            yd = self.yt.streams.get_highest_resolution()
            yd.download(output_path=folder_path)
        if stream_type == "video":
            yd = self.yt.streams.filter(only_video=True).first()
            yd.download(output_path=folder_path)
        else:
            yd = self.yt.streams.get_audio_only()
            audio_file_name = f"{self.yt.title}.mp3"
            yd.download(output_path=folder_path, filename=audio_file_name)
        self.done(True)

    def ask_type(self):
        self.clearframe()
        self.create_label("self.label", "Would you like to save it as a video or audio file?", 14)
        self.create_button("self.button1", "Video and Audio", 18, lambda: self.download("both"))
        self.create_button("self.button2", "Just video", 18, lambda: self.download("video"))
        self.create_button("self.button2", "Just audio", 18, lambda: self.download("audio"))

App()
