
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
import threading
import psutil
from gps3.agps3threaded import AGPS3mechanism
import signal
import sys


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Exiting!!! ")
    settings.status_GPS=False
 
signal.signal(signal.SIGINT, handler)

class RoundedButton(Canvas):

    def __init__(self, master=None, text:str="", radius=10, btnforeground="white", btnbackground="black", clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked

        self.radius = radius        
        
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=str(settings.gpsSpeed) + " km/hr", tags="button", fill=btnforeground, font=("Times", 40, "bold" ), justify="center")

        self.bind("<Configure>", self.resize)
        
        text_rect = self.bbox(self.text)
        
        if int(self["width"]) < text_rect[2]-text_rect[0]:
            self["width"] = (text_rect[2]-text_rect[0]) 
        
        else:
            self["width"] = 350

        if int(self["height"]) < text_rect[3]-text_rect[1]:
            self["height"] = (text_rect[3]-text_rect[1])
        else:
            self["height"] = 200

    def round_rectangle(self, x1, y1, x2, y2, radius=10, update=False, **kwargs): # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)
        
        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2]-text_bbox[0]:
            width = text_bbox[2]-text_bbox[0] + 5 
        
        if event.height < text_bbox[3]-text_bbox[1]:  
            height = text_bbox[3]-text_bbox[1] + 5
        
        self.round_rectangle(5, 5, width-50, height-100, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2]-bbox[0])/2) - ((text_bbox[2]-text_bbox[0])/2)
        y = ((bbox[3]-bbox[1])/2) - ((text_bbox[3]-text_bbox[1])/2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill="white")
            if self.clicked is not None:
                self.clicked()

        else:
            self.itemconfig(self.rect, fill=self.btnbackground)



def updateMap(gpsWin, mainWin, destTxt, mylbl, map_wdg, WIDTH, HEIGHT):
    if settings.showMap:
        print( " Here ")
        dest_address = settings.destTxt.get("1.0",END)
        if len(dest_address) > 15:
            settings.marker_1 = map_wdg.set_marker(settings.gpsLat, settings.gpsLong)
            marker_2 = map_wdg.set_address(dest_address, marker=True)
            settings.marker_2 = map_wdg.set_marker(marker_2.position[0], marker_2.position[1])
            if settings.prev_gpsLat != settings.gpsLat and settings.prev_gpsLong != settings.gpsLong :
                settings.prev_gpsLat = settings.gpsLat
                settings.prev_gpsLong = settings.gpsLong
                if settings.path_1 is not None:
                    settings.path_1.remove_position(position)
                    settings.path_1.delete()
            else:
                settings.path_1 = map_wdg.set_path([settings.marker_2.position, settings.marker_1.position,( marker_2.position[0],marker_2.position[1] ) ,(settings.gpsLat, settings.gpsLong)])
                #settings.path_1.set_position_list(new_position_list)
                #settings.path_1.add_position(position)
        else:
            settings.marker_1 = map_wdg.set_position(settings.gpsLat, settings.gpsLong)
            if settings.marker_2 is not None:
                settings.marker_2.delete()
                #settings.path_1.remove_position(position)
                settings.path_1.delete()

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
    map_wdg.set_zoom(40)
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


def checkStatus(mainWin,process):
    if checkIfProcessRunning(process):
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
    checkStatus(mainWin, 'chrome')
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

def optionVideo(value):
    settings.enablebackVideo=value
    return

def playbackVid():
    ### Put here path of the file / script to be launched
    command_list = "/usr/bin/python3 " 
    command_list += OBJECT_DETECT_BIN_PATH
    command_list +="collison_warning.py &"
    if settings.enablebackVideo:
        p = subprocess.Popen(command_list)
    

def checkOptions(optionVideo ,newWindow, mainWin):
    if optionVideo is True:
        playbackVid()
        on_closing(newWindow, mainWin)


def adasGui(mainWin):
    #mainWin.withdraw()

    window = Toplevel()
    window.resizable(0,0)

    window.title(" ------ ADAS Options ------ ")
    WIDTH, HEIGHT = window.winfo_screenwidth(),window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (WIDTH, HEIGHT-100))
    window.configure(bg="black")
    
    def selection(choice, window, mainWin):
        settings.adas_Choice = choice.lower()
        print(" Selected Option for Adas : ", adas_Choice)
        
        if "live" == settings.adas_Choice :
            window.destroy()
            checkStatus(mainWin, 'python3 /home/pi/NextGenDriving/NextGensoftware/collison_warning.py')

        elif "settings" == settings.adas_Choice :
            optionSel = [ 'Car', 'Bike', 'Animal', 'Speed', 'Pedestrian' ]
            newWindow = Toplevel()
            window.withdraw()
            WIDTH, HEIGHT = newWindow.winfo_screenwidth(), newWindow.winfo_screenheight()
            newWindow.geometry("%dx%d+0+0" % (WIDTH, HEIGHT-100))
            newWindow.configure(bg="black")
            settings.selected_Option.clear()

            backVideo = IntVar()
            r1 = Radiobutton(newWindow, text="ON", bg="black", fg="white", font=settings.adasFont, bd=0, highlightthickness=0, activebackground = "black", activeforeground="white", variable=radio, value=1, command= lambda: optionVideo(True))
            #r1.pack(side=LEFT, padx=20)
            r1.grid(row=0, column=0, padx=100, pady=75)

            r2 = Radiobutton(newWindow, text="OFF", bg="black", fg="white", font=settings.adasFont, bd=0, highlightthickness=0, activebackground="black", activeforeground="white" ,variable=radio, value=0, command= lambda: optionVideo(False))
            #r2.pack(side=LEFT, padx=20)
            r2.grid(row=0, column=1, padx=100, pady=75)

            def getVal(event):
                settings.speed_Limit = sp_choice.get()
                print( " Speed Limit set to : " + settings.speed_Limit + " Km/hr")

            lblSpeed = Label(newWindow,text="Speed(Km/hr) :", font=settings.optionFont, fg="white", bd=0, highlightthickness=0, activebackground="black", activeforeground = "black" , bg="black")
            #lblSpeed.pack(anchor=N, padx=20, pady=100)
            lblSpeed.grid(row=2, column=0, padx=100, pady=150)
            sp_choice = StringVar()
            cbox_video = ttk.Combobox(newWindow, textvariable=sp_choice, font= settings.optionFont)
            #cbox_video.pack(anchor=N, padx=100, pady=100)
            cbox_video.grid(row=2, column=1, padx=100, pady=150)

            cbox_video['values'] = [ '20', '40', '60' ]
            cbox_video['state'] = 'readonly'
            cbox_video.bind('<<ComboboxSelected>>', getVal)
            
            diffX=0
            for x in range(len(optionSel)):
                l = Checkbutton(newWindow, bg="black", fg="white",bd=0, highlightthickness=0, activebackground="black", activeforeground="white", text=optionSel[x], variable=optionSel[x],command=lambda x=optionSel[x]:settings.selected_Option.append(x), font= settings.optionFont)
                #l.pack(anchor=N, pady=150 + diffY)
                #l.grid(row=3, column=0 + diffX, padx=30, pady=180)
                l.place(x= 100 + diffX, y= HEIGHT-450)
                diffX += 320

            Button(newWindow,text="Submit",bg="black",fg="white", activebackground = "black", activeforeground="black",font= settings.adasFont, command=lambda: [print(settings.selected_Option),newWindow.destroy(), checkOptions( settings.enablebackVideo ,newWindow, mainWin)]).place(x=WIDTH/2 - 100, y= HEIGHT-250)
            #.grid(row=3,column=1, padx=300, pady=10)
            newWindow.attributes('-topmost',True)
            newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing( newWindow, window))
            newWindow.mainloop()

    
    dirAdas = os.path.join(settings.BASE_DIR, settings.ADAS_DIR)
    file_Live = os.path.join(dirAdas, settings.FILE_ADAS_LIVE)
    file_Settings = os.path.join(dirAdas, settings.FILE_ADAS_SETTING)

    
    imgLive = ImageTk.PhotoImage(Image.open(file_Live).resize((300,300), Image.ANTIALIAS))
    imgSettings = ImageTk.PhotoImage(Image.open(file_Settings).resize((300,300), Image.ANTIALIAS))
    
    btnLive = Button(window, image=imgLive, bg="black",highlightthickness=0,bd=0,activeforeground='white', activebackground='black', compound=CENTER, command= lambda: selection("live", window, mainWin))
    
    btnSettings = Button(window, image=imgSettings, bg="black",highlightthickness=0,bd=0,activeforeground='white', activebackground='black', compound=CENTER, command= lambda: selection("settings", window, mainWin))
    
    btnLive.pack(side=LEFT,padx=450, pady=30)
    btnSettings.pack(side=LEFT, padx=5,pady=30)

    '''
    radio = IntVar()
     
    r1 = Radiobutton(window, text="Live Adas", bg="white", font=settings.adasFont, bd=0, highlightthickness=0, activebackground = "black",activeforeground="white", variable=radio, value=1, command= lambda: selection(window, mainWin))
    r1.pack(anchor=N,pady=250)

    r2 = Radiobutton(window, text="Settings", bg="white", font=settings.adasFont, bd=0, highlightthickness=0, activebackground="black" , activeforeground="white", variable=radio, value=2, command= lambda: selection(window, mainWin))
    r2.pack(anchor=N, pady=450)
    '''

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing( window, mainWin))
    window.mainloop()
    return

def getSpeed():
    agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
    agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
    agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default 0.2 second, default daemon=True

    while settings.status_GPS: 
        try:
            settings.gpsLat = round(float(agps_thread.data_stream.lat),4)
            settings.gpsLong = round(float(agps_thread.data_stream.lon),4)
            settings.gpsSpeed = int(agps_thread.data_stream.speed)
            #print(" Lattitude : " + str(settings.gpsLat))
            #print(" Longitude : " + str(settings.gpsLong))
            #print(" Speed : " + str(settings.gpsSpeed) + " km/h")
            sleep(0.15)
        except Exception as err:
            pass
    print(" Exiting GPS thread ...")
