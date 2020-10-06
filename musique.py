import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer

root=Tk()

statusbar = ttk.Label(root, text = "Welcome to Musique", relief = SUNKEN, anchor = W)
statusbar.pack(side = BOTTOM, fill = X)

#Creating menubar
menubar=Menu(root)
root.config(menu=menubar)

# playlist contains full path of file
#playlistbox contains name of file only

playlist = []

def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)
    add_to_playlist(filename)
    
def add_to_playlist(filename):
    fname = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, fname)
    playlist.insert(index, filename)
    index += 1
    

#Create the submenu
subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Musique','This is a music player built using Python Tkinter by @ShubhneetSandhu')

subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

#root.geometry('400x500')
root.title("Musique")                                                     #title
root.iconbitmap(r'Musique_images/boombox_7Fz_icon.ico')                   #icon

#Root window - StatusBar, LeftFrame, RightFrame
#LeftFrame - The listbox(playlist)
#RightFrame - MiddleFrame and BottomFrame
 
leftframe = ttk.Frame(root)
leftframe.pack(side = LEFT, padx = 20, pady = 15)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addfile = ttk.Button(leftframe, text = "Add", command = browse_file)
addfile.pack(padx = 10, side = LEFT)

def del_file():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    del playlist[selected_song]

delfile = ttk.Button(leftframe, text = "Delete", command = del_file)
delfile.pack(side = RIGHT, padx = 10)

rightframe = ttk.Frame(root)
rightframe.pack(side = LEFT)

mixer.init()                                               #mixer initialization


playphoto = PhotoImage(file = 'Musique_images/plays.png')
pausephoto = PhotoImage(file = 'Musique_images/pause.png')
rewindphoto = PhotoImage(file = 'Musique_images/rewind.png')
mutephoto = PhotoImage(file = 'Musique_images/mute.png')
speakerphoto = PhotoImage(file = 'Musique_images/speaker.png')


def playmusic():
    global paused
    #This logic first checks whether the paused var. is initialized and if it is not initialized, then it will start the music
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Playing- " + os.path.basename(play_song)
        paused = False
    else:
        try:
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_song = playlist[selected_song]
            mixer.music.load(play_song)
            mixer.music.play()
            statusbar['text'] = "Playing- " + os.path.basename(play_song)
       
        except:
            tkinter.messagebox.showerror('File not found', 'Musique could not find the file. Please check again')
        
paused = False

def pausemusic():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music paused"
    
def rewindmusic():
    mixer.music.load(filename)
    mixer.music.play()
    statusbar['text'] = "Music rewinded"
    
def set_vol(val):
    val=float(val)/100                                       #as set_volume takes value from the range 0-1 ex.0.55
    mixer.music.set_volume(val)
    
muted = False
    
def mutemusic():
    global muted
    if muted:
        #Unmute vol.
        mixer.music.set_volume(0.6)
        volumebtn.configure(image = speakerphoto)
        scale.set(60)
        muted = False
    else:
        #Mute vol.
        mixer.music.set_volume(0)
        volumebtn.configure(image = mutephoto)
        scale.set(0)
        muted = True
    
middleFrame = Frame(rightframe)
middleFrame.pack(padx = 10, pady = 20)
 
rewindbtn=ttk.Button(middleFrame,image=rewindphoto,command=rewindmusic)
rewindbtn.grid(row = 0, column = 0, padx = 5)   
playbtn=ttk.Button(middleFrame,image=playphoto,command=playmusic)
playbtn.grid(row = 0, column = 1, padx = 5)
pausebtn=ttk.Button(middleFrame,image=pausephoto,command=pausemusic)
pausebtn.grid(row = 0, column = 2, padx = 5)

bottomFrame = ttk.Frame(rightframe)
bottomFrame.pack(pady = 15)
volumebtn=ttk.Button(bottomFrame,image=speakerphoto,command=mutemusic)
volumebtn.grid(row = 0, column = 0, padx = 5)


scale=ttk.Scale(bottomFrame,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(60)
mixer.music.set_volume(0.6)                                 #to initialize volume at start of program 
scale.grid(row = 0, column = 1)

def closing():
    mixer.music.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()
