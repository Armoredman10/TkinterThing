# Output Stuff
import sys
import os
import threading
import queue
import time
#Subprocess
import subprocess
#Install needed stuff
subprocess.run(['pip', 'install', 'gallery-dl'])
subprocess.run(['pip', 'install', 'customtkinter'])
subprocess.run(['pip', 'install', 'yt-dlp'])
import yt_dlp
import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
#Gallery-DL
from gallery_dl import config
extr="Twitter"
dirt=""
destiny = "n"
appear = "system"
extract = "Chosen Website: Twitter"
cookies = False
#Gallery-Dl cookies
config.load()
config.set((), "cookies", ["firefox", "edge", "chrome"])


# Change Destiny and Dirt to Main class variables with self instead of global

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
        self.ent=ctk.CTkEntry(self.f,width=250, placeholder_text="")
        self.lbl=ctk.CTkLabel(self.f, text="")
        self.but=ctk.CTkButton(self.f, text="Download", command=self.download, width=25)
        self.but2=ctk.CTkButton(self.f, text="\N{FILE FOLDER}", command=self.direct, width=15)
        self.but3=ctk.CTkButton(self.f, text="\N{GEAR}", command=self.SettingsWindow, width=15)
        self.f.grid(column=0, row=0, sticky="NSEW")
        self.ent.grid(column=0, row=0, sticky="EW", padx=3)
        self.lbl.grid(column=0, row=1, sticky="EW", padx=6)
        self.but.grid(column=1, row=0, sticky="E", padx=(3,0))
        self.but2.grid(column=2, row=0, sticky="E", padx=3)
        self.but3.grid(column=3, row=0, sticky="E", padx=(0,3))
        self.newWindow = None
        self.dj = ""
        dirname = os.path.dirname(__file__)
        cooks = os.path.join(dirname, 'cookies.txt')
        self.cook = "--cookies " + cooks + " "
    # Running Gallery-DL
    def download(self):
        if extr == "Twitter" or "Instagram":
            download_thread = threading.Thread(target=self.download_gdl)
            download_thread.start()
        elif extr=="Youtube":
            if self.ent.get() == "" or self.ent.get() == "input a youtube link":
                self.ent.delete(0, tk.END)
                self.ent.insert(0, "input a youtube link")
            else:
                download_thread = threading.Thread(target=self.download_video)
                download_thread.start()
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
            result_window.focus()
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
    def download_gdl(self):
        global destiny
        global dirt
        global cookies
        temp = self.ent.get()
        print(temp)
        self.ent.delete(0, tk.END)
        if destiny == "y" and cookies == True:
            self.dj = "gallery-dl " + self.cook + temp + " --dest " + dirt
            print("1")
        elif destiny == "y" and cookies == False:
            self.dj = "gallery-dl " + temp + " --dest " + dirt
            print("2")
        elif destiny == "n" and cookies == True:
            self.dj = "gallery-dl " + self.cook + temp
            print("3")
        elif destiny == "n" and cookies == False:
            self.dj = "gallery-dl " + temp
            print("4")
        print(self.dj)
        def create_toplevel():
            # Create a new Toplevel window for displaying the output
            result_window = ctk.CTkToplevel(self.master)
            result_window.title("Download Result")
            # Create a Text widget to display the output
            output_text = ctk.CTkTextbox(result_window, wrap=tk.WORD, height=300, width=500)
            output_text.pack()
            result_window.focus()
            return result_window, output_text
        result_window, output_text = create_toplevel()
        # def Function that creates dj, has the if statements for directory and cookies here
        def download_gdl2():
    # Redirect stdout to the Text widget using the custom redirector
            sys.stdout = StdoutRedirector(output_text)
    # Use Popen to capture the output
            process = subprocess.Popen(self.dj, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # Read the output line by line and update the text widget
            for line in process.stdout:
                sys.stdout.write(line)
                time.sleep(0.1)
    # Wait for the process to finish
            process.wait()
    # Restore stdout to its original value
            sys.stdout = sys.__stdout__
            self.queue.put("Download finished")
        threading.Thread(target=download_gdl2).start()
    # Changing download directory, probably will need to update when more extractors are added
    def direct(self):
        global destiny
        global dirt
        dir = askdirectory()
        print(dir)
        dirt=dir+"/"+ extr
        destiny = "y"
        print(destiny)
        print(dirt)
        dirty="Downloading at: " + dirt 
        print(dirty)
        self.lbl.configure(text=dirty)
    # Creates setting window
    def SettingsWindow(self):
        if self.newWindow is None or not self.newWindow.winfo_exists():
            self.newWindow = ctk.CTkToplevel(self.master)  # create window if its None or destroyed
            self.app = Settings(self.newWindow)
        else:
            self.newWindow.deiconify() # Unminimizes hopefully
            self.newWindow.focus()  # if window exists focus it



class Settings:
    def __init__(self, master):
# put settings inside frame with border, save button outside of frame
        #Move these around to look better
        global cookies
        self.cookies = False
        self.master = master
        self.master.title("Settings")
        self.master.focus()
        self.f2 = ctk.CTkFrame(self.master)
        self.list=ctk.CTkComboBox(self.f2, state="readonly", command=self.listcall, values=["Twitter","Instagram","Youtube"])
        self.list.grid(column=0, row=1, sticky="EW")
        self.list.set(extr)
        self.list=ctk.CTkComboBox(self.f2, state="readonly", command=self.appearence, values=["system","dark","light"])
        self.list.grid(column=0, row=2, sticky="EW")
        self.list.set(appear)
        self.cookie = tk.BooleanVar()
        self.cookbtn =ctk.CTkCheckBox(self.f2, text="use cookies.txt", variable=self.cookie, command=self.chkbx) 
        self.quitButton = ctk.CTkButton(self.f2, text = 'Save Settings', width = 25, command = self.close_windows)
        self.quitButton.grid(column=1, row=1)
        self.lbl = ctk.CTkLabel(self.f2, text=extract)
        self.lbl.grid(column=0, row=0, sticky="W", padx=3)
        self.cookbtn.grid(column=0, row=3)
        self.f2.grid(column=0, row=0, sticky="NSEW")
        if cookies == True:
            self.cookbtn.select()
    def chkbx(self):
        global cookies
        if self.cookie.get():
            cookies = True
        else:
            cookies = False
    def close_windows(self):
        self.master.destroy()
    def listcall(self,choice):
        global extr
        global extract
        extr=choice
        extract= "Chosen Website: " + extr
        self.lbl.configure(text=extract)
        #Change entrys placeholder text, may need to move this, still haven't done this
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
