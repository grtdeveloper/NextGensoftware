
from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from time import sleep
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
import PIL.Image as Image

import tkintermapview
import settings
import tkinterweb
import webview
import os.path
import webbrowser
import multiprocessing as mp
import threading
import psutil


def updateMap(gpsWin, mainWin, destTxt, mylbl, map_wdg, WIDTH, HEIGHT):
    if settings.showMap:
        print( " Here ")
        dest_address = settings.destTxt.get("1.0",END)
        if len(dest_address) > 15:
            marker_1 = map_wdg.set_marker(settings.gpsLat, settings.gpsLong, marker=True)
            marker_2 = map_wdg.set_marker(settings.destTxt.get("1.0",END), marker= True)
            #map_wdg.set_position(settings.gpsLat,settings.gpsLong, marker=True)
            if settings.prev_gpsLat != settings.gpsLat and settings.prev_gpsLong != settings.gpsLong :
                settings.prev_gpsLat = settings.gpsLat
                settings.prev_gpsLong = settings.gpsLong
                path_1.remove_position(position)
                path_1.delete()
            else:
                path_1 = map_wdg.set_path([marker_2.position, marker_1.position])
                path_1.set_position_list(new_position_list)
                path_1.add_position(position)
        else:
            marker_1= map_wdg.set_position(settings.gpsLat, settings.gpsLong, marker=True)

        gpsWin.after(3000,lambda: updateMap(gpsWin, mainWin, destTxt, mylbl, map_wdg, WIDTH, HEIGHT))
    else:
        print( "Performing window operations ")
        gpsWin.destroy()
        mainWin.deiconify()


def showLocation(mainWin, val_Map):
    mainWin.withdraw()
    print( " Launching  GPS ..... ")
    settings.showMap=val_Map
    gpsWin = Toplevel()
    gpsWin.resizable(0,0)
    gpsWin.title(" ----  Location Finder  ---- ")
    WIDTH, HEIGHT = gpsWin.winfo_screenwidth(),gpsWin.winfo_screenheight()

    mylbl = LabelFrame(gpsWin,)
    mylbl.pack(pady=20)
    
    destLbl=Label(gpsWin, text="Destination: ", width=15,height =2, font=('Helvetica 10 bold'), highlightthickness=0, bd=0)
    destLbl.place(x=85,y=50)

    settings.destTxt = Text(gpsWin, width=40, height= 2, font= settings.myFont, bd=0)
    settings.destTxt.place(x=175, y=50)
    
    map_wdg = tkintermapview.TkinterMapView(mylbl,width=WIDTH-200, height=HEIGHT-100, corner_radius=0)
    map_wdg.set_zoom(35)
    map_wdg.pack()
    try:
        updateMap(gpsWin, mainWin, settings.destTxt, mylbl, map_wdg, WIDTH, HEIGHT)
    except Exception as err:
        pass
    gpsWin.protocol("WM_DELETE_WINDOW", lambda: on_closing(gpsWin, mainWin))
    gpsWin.mainloop()

def on_closing(prevWin, mainWin):
    print(" Closing Active Window ")
    prevWin.destroy()
    print(" Falling Back to Original ")
    mainWin.deiconify()

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def checkStatus(mainWin):
    if checkIfProcessRunning('chrome'):
        threading.Timer(2, lambda: checkStatus(mainWin)).start()
        print( "Running ")
        return True
    else:
        print("Closed / Stopped ")
        mainWin.deiconify()
        return False


def launchPlayer(mainWin, link):
    mainWin.withdraw()
    #playWin = Toplevel()
    from selenium import webdriver
    
    driver = webdriver.Chrome (executable_path="/usr/lib/chromium-browser/chromium-browser")
    # maximize with maximize_window()
    driver.maximize_window()
    driver.get(link)
    driver.quit()
    #webbrowser.open_new(link,fullscreen=True)
    checkStatus(mainWin)
    #playWin.mainloop()


def open_file(videoplayer, window ,dirName):
    if settings.play_Options.lower() == "recorded" :
        file = askopenfile(mode='r', initialdir= dirName, parent= window ,filetypes=[('Video Files', ["*.*"])])
        if file is not None:
            filename = file.name
            videoplayer.load(r"{}".format(filename))
            videoplayer.play()
    else:
        from tkinter import messagebox
        messagebox.showerror('Player Error', 'Error: Please Choose Recorded Option First!',parent=window)
    return


def playAgain(videoplayer):
    print(" Playing File Again ")
    videoplayer.play()

def StopVideo(videoplayer):
    print(" Stopping File Again ")
    videoplayer.stop()

def PauseVideo(videoplayer):
    print(" Pausing File Again ")
    videoplayer.pause()


def showVideo(dir_Video,mainWin):
    window = Toplevel()
    window.resizable(0,0)

    window.title("Tkinter Play Videos in Video Player")
    WIDTH, HEIGHT = window.winfo_screenwidth(),window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (WIDTH, HEIGHT-100))
    window.configure(bg="light blue")
    videoplayer = TkinterVideo(master=window, scaled=True)
    videoplayer.pack(expand=True, fill="both")

    lbl1 = Label(window, text="Tkinter Video Player", bg="light blue", fg="white", font="none 28 bold")
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    dirIcon = os.path.join(settings.BASE_DIR, settings.DIR_MEDIA_ICONS)
    IMG_OPEN = os.path.join(dirIcon,settings.FILE_OPEN)
    IMG_PLAY = os.path.join(dirIcon,settings.FILE_PLAY)
    IMG_PAUSE = os.path.join(dirIcon,settings.FILE_PAUSE)
    IMG_STOP = os.path.join(dirIcon,settings.FILE_STOP)

    print(" Image open : ", IMG_OPEN)

    imgOpen = ImageTk.PhotoImage(Image.open(IMG_OPEN).resize((150,150), Image.ANTIALIAS))
    imgPlay = ImageTk.PhotoImage(Image.open(IMG_PLAY).resize((150,150), Image.ANTIALIAS))
    imgPause = ImageTk.PhotoImage(Image.open(IMG_PAUSE).resize((150,150), Image.ANTIALIAS))
    imgStop = ImageTk.PhotoImage(Image.open(IMG_STOP).resize((150,150), Image.ANTIALIAS))
    

    def get_value(event):
        settings.play_Options = ply_choice.get()
        print(" You have choosen to play " + settings.play_Options + " video")


    ply_choice = StringVar()
    cbox_video = ttk.Combobox(window, textvariable=ply_choice, font= settings.myFont)
    cbox_video.pack(side=LEFT,padx=50)

    cbox_video['values'] = [ 'live', 'recorded' ]
    cbox_video['state'] = 'readonly'
    cbox_video.bind('<<ComboboxSelected>>', get_value)

    openbtn = Button(window, text='Open', image=imgOpen, command=lambda: open_file(videoplayer, window, dir_Video))
    openbtn.pack(side=LEFT, padx=50)

    playbtn = Button(window, text='Play Video', image=imgPlay, command=lambda: playAgain(videoplayer))
    playbtn.pack(side=LEFT, padx=50)

    pausebtn = Button(window, text='Pause Video', image=imgPause, command=lambda: PauseVideo(videoplayer))
    pausebtn.pack(side=LEFT, padx=50)

    stopbtn = Button(window, text='Stop Video', image=imgStop ,command=lambda: StopVideo(videoplayer))
    stopbtn.pack(side=LEFT, padx=50)

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing( window, mainWin))
    window.mainloop()
    return
