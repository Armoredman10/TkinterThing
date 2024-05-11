from __future__ import unicode_literals
import yt_dlp
# Output Stuff
import sys
import threading
import queue
#Subprocess
import subprocess
#Install needed stuff
subprocess.run("pip install -U gallery_dl")
subprocess.run("pip install -U customtkinter")
subprocess.run("pip install -U yt_dlp")
#Tkinter stuff
import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
#Gallery-DL
from gallery_dl.job import DownloadJob 
from gallery_dl import config

# change with extractor choice, twitter for now
# Put inside the class?
extr="twitter"
dirty=""
appear = "system"
extract = "Chosen Website: Twitter"

#Gallery-Dl cookies, change later
config.load()
config.set((), "cookies", ["firefox"])

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Scroll to the bottom
    def flush(self):
        pass


class Main:
    def __init__(self, master):
        self.queue = queue.Queue()
        self.master=master
        self.master.title("Internet Archive Tool")
        self.f=ctk.CTkFrame(self.master)
        self.ent=ctk.CTkEntry(self.f,width=250,placeholder_text="")
        self.lbl=ctk.CTkLabel(self.f,text=dirty)
        self.but=ctk.CTkButton(self.f,text="Download",command=self.download,width=25)
        self.but2=ctk.CTkButton(self.f,text="\N{FILE FOLDER}",command=self.direct,width=15)
        self.but3=ctk.CTkButton(self.f,text="\N{GEAR}",command=self.SettingsWindow,width=15)
        self.f.grid(column=0,row=0,sticky="NSEW")
        self.ent.grid(column=0,row=0,sticky="EW",padx=3)
        self.lbl.grid(column=0,row=1,sticky="EW")
        self.but.grid(column=1,row=0,sticky="E",padx=(3,0))
        self.but2.grid(column=2,row=0,sticky="E",padx=3)
        self.but3.grid(column=3,row=0,sticky="E",padx=(0,3))
        self.newWindow = None
    # Running Gallery-DL
    def download(self):
        temp = self.ent.get()
        self.ent.delete(0,tk.END)
        if extr=="twitter":
            print("Twitter")
            subprocess.run(DownloadJob(temp).run())
        elif extr=="Instagram":
            #Instagram Download stuff here
            print("Insta")
        elif extr=="Youtube":
            #Youtube-dl stuff here
            download_thread = threading.Thread(target=self.download_video)
            download_thread.start()
            print("Youtube")
    # Changing download directory, probably will need to update when more extractors are added
    def direct(self):
        ext="twitter"
        dir = askdirectory()
        dirt=dir+"/"+ extr
        dirty="Downloading at:"+" "+ dirt
        config.set(("extractor",), "base-directory", dirt)
        self.lbl.configure(text=dirty)
    # Creates setting window (WIP)
    def SettingsWindow(self):
        if self.newWindow is None or not self.newWindow.winfo_exists():
            self.newWindow = ctk.CTkToplevel(self.master)  # create window if its None or destroyed
            self.app = Settings(self.newWindow)
        else:
            self.newWindow.deiconify() # Unminimizes hopefully
            self.newWindow.focus()  # if window exists focus it
    def download_video(self):
        temp = self.ent.get()
        self.ent.delete(0, tk.END)
        def create_toplevel():
            # Create a new Toplevel window for displaying the output
            result_window = ctk.CTkToplevel(self.master)
            result_window.title("Download Result")
            # Create a Text widget to display the output
            output_text = ctk.CTkTextbox(result_window, wrap=tk.WORD, height=300, width=500)
            output_text.pack()
            return result_window, output_text
        result_window, output_text = create_toplevel()
        def download():
            # Redirect stdout to the Text widget using the custom redirector
            sys.stdout = StdoutRedirector(output_text)
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([temp])
            # Restore stdout to its original value
            sys.stdout = sys.__stdout__
            self.queue.put("Download finished")
        threading.Thread(target=download).start()



class Settings:
    def __init__(self, master):
        self.master=master
        self.master.title("Settings")
        self.master.focus()
        self.f2 = ctk.CTkFrame(self.master)
        self.list=ctk.CTkComboBox(self.f2,state="readonly",command=self.listcall,values=["Twitter","Instagram","Youtube"])
        self.list.grid(row=1,column=0,sticky="EW")
        self.list.set(extr)
        self.list=ctk.CTkComboBox(self.f2,state="readonly",command=self.appearence,values=["system","dark","light"])
        self.list.grid(row=2,column=0,sticky="EW")
        self.list.set(appear)
        self.quitButton = ctk.CTkButton(self.f2, text = 'Save Settings', width = 25, command = self.close_windows)
        self.quitButton.grid(row=1,column=1)
        self.lbl = ctk.CTkLabel(self.f2,text=extract)
        self.lbl.grid(row=0,column=0,sticky="W",padx=3)
        self.f2.grid(column=0,row=0,sticky="NSEW")
    def close_windows(self):
        self.master.destroy()
    def listcall(self,choice):
        global extr
        global extract
        extr=choice
        extract="Chosen Website: "+extr
        self.lbl.configure(text=extract)
        # print(extr)
        #Change entrys placeholder text, may need to move this
    def appearence(self,choice):
        ctk.set_appearance_mode(choice)
        global appear
        appear = choice

def main(): 
    root = ctk.CTk()
    app = Main(root)
    root.mainloop()

if __name__ == '__main__':
    main()


