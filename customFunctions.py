
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
import os.path
import webbrowser
import threading
import psutil
from gps3.agps3threaded import AGPS3mechanism
import signal
import sys
import subprocess
import socket
import fcntl
import struct
import requests
import folium
import json
import pandas as pd
from geopy.geocoders import Nominatim
from keyPad import initKey
import getpass

gpsd = None #Setup global variable 

def get_lat_long_from_address(address):
    url = settings.GEOCODE_URL
    response={}
    d={}
    querystring = {"address":address,"language":"en"}

    headers = {
        "X-RapidAPI-Key": settings.RAPID_API,
        "X-RapidAPI-Host": "google-maps-geocoding.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    d = json.loads(response.text)
    return d['results'][0]['geometry']['location']

def get_directions_response(lat1, long1, lat2, long2, mode='drive'):
   url = "https://route-and-directions.p.rapidapi.com/v1/routing"
   key = settings.RAPID_API
   host = "route-and-directions.p.rapidapi.com"
   headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": host}
   querystring = {"waypoints": str(lat1) + "," + str(long1) + "|" + str(lat2) + "," +str(long2),"mode":mode}
   response = requests.request("GET", url, headers=headers, params=querystring)
   return response


'''
def get_directions_response(lat1,lng1, lat2,lng2):
    
    url =  settings.MAP_URL 

    querystring = {"waypoints": str(lat1) + "," + str(lng1) + "|" + str(lat2) + "," + str(lng2), "mode":"drive"}

    headers = {
            "X-RapidAPI-Key": settings.RAPID_API,
            "X-RapidAPI-Host": "route-and-directions.p.rapidapi.com"
}

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response
'''

def create_map(gpsWin, response):
   # use the response
   mls = response.json()['features'][0]['geometry']['coordinates']
   points = [(i[1], i[0]) for i in mls[0]]
   m = folium.Map()   # add marker for the start and ending points
   for point in [points[0], points[-1]]:
      folium.Marker(point).add_to(m)   # add the lines
   folium.PolyLine(points, weight=5, opacity=1).add_to(m)   # create optimal zoom
   df = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
   sw = df[['Lat', 'Lon']].min().values.tolist()
   ne = df[['Lat', 'Lon']].max().values.tolist()
   m.fit_bounds([sw, ne])
   m.save("map/current_route.html")
   webObject=launchPlayer(gpsWin, " GPS Route ", "map/current_route.html")
   return


def bluetoothStatus():
    process = subprocess.Popen(['hcitool', 'dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if "hci0" in str(out):
        return True
    else:
        return False

def wifiStatus(intfName):
    try:
        from netifaces import AF_INET, ifaddresses
    except ModuleNotFoundError as e:
        raise SystemExit(f"Requires {e.name} module. Run 'pip install {e.name}' "
                         f"and try again.")


    def get_ip_linux(interface: str) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packed_iface = struct.pack('256s', interface.encode('utf_8'))
        packed_addr = fcntl.ioctl(sock.fileno(), 0x8915, packed_iface)[20:24]
        return socket.inet_ntoa(packed_addr)

    if len(get_ip_linux(intfName)) > 1:
        return True
    else:
        return False

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Exiting!!! ")

#### Enable me to start gps thread
settings.status_GPS=False
 
signal.signal(signal.SIGINT, handler)


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    settings.sock_Server = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    settings.sock_Server.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    settings.sock_Server.listen(2)
    conn, address = settings.sock_Server.accept()  # accept new connection
    print("Connection from: " + str(address))
    recvByte = []
    data = ""
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(100).decode()
        if not data:
            break
        print(" Got data :", data)
        recvByte = data.split(',')
        print(" received :", recvByte)
        if len(recvByte) > 1:
            try:
                settings.collision_object = str(recvByte[0]) 
                settings.collision_object_color = str(recvByte[1])
            except Exception as e:
                print( "Got Exception s : ", e)
                pass
        else:
            settings.collision_object = str(recvByte[0]) 
        rsp = "ack"
        conn.send(rsp.encode())  # send data to the client
        recvByte.clear()
        data=""

    settings.sock_Server.close()  # close the connection


class RoundedButton(Canvas):

    def __init__(self, master=None, text:str="", radius=10, btnforeground="white", btnbackground="black", clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked

        self.radius = radius        
        
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=str(settings.gpsSpeed) + " km/hr", tags="button", fill=btnforeground, font=("Times", 35, "bold" ), justify="center")

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
        if settings.addComplete is False and settings.Finaladd != "clear":
            print( " in first loop ")
            destTxt.delete("1.0", "end") 
            destTxt.insert(END,settings.Finaladd)
            if len(settings.Finaladd) > 1:
                print(" dest_address :", settings.Finaladd)
        elif settings.addComplete is False and settings.Finaladd == "clear":
            print("Cleaning Up ")
            destTxt.delete("1.0", "end") 
            settings.Finaladd = ""
            settings.entry_gpsText = ""
            settings.lat_lons={}
        else:
            if len(settings.lat_lons) == 0 :
                settings.marker_1 = map_wdg.set_position(settings.gpsLat, settings.gpsLong, marker=True)
                settings.lat_lons = get_lat_long_from_address(settings.Finaladd) 
                rsp = get_directions_response(settings.gpsLat,settings.gpsLong, settings.lat_lons['lat'], settings.lat_lons['lng']) 
                ''' 
                settings.mls = rsp.json()['features'][0]['geometry']['coordinates']
                settings.marker_2= map_wdg.set_position(settings.lat_lons['lat'],settings.lat_lons['lng'], marker=True)
                settings.addComplete=True
                settings.path_1 = map_wdg.set_path([settings.marker_2.position, settings.marker_1.position,(settings.lat_lons['lat'], settings.lat_lons['lng'] ) ,(settings.gpsLat, settings.gpsLong)])
                '''
            if settings.prev_gpsLat != settings.gpsLat and settings.prev_gpsLong != settings.gpsLong :
                if settings.path_1 is not None:
                    settings.path_1.remove_position(settings.prev_gpsLat, settings.prev_gpsLong)
                settings.prev_gpsLat = settings.gpsLat
                settings.prev_gpsLong = settings.gpsLong
                rsp = get_directions_response(settings.gpsLat,settings.gpsLong, settings.lat_lons['lat'], settings.lat_lons['lng']) 
                #newPos =[tuple(x) for x in settings.mls[0]]
            create_map(gpsWin, rsp)
            gpsWin.update()
        gpsWin.after(1500,lambda: updateMap(gpsWin, mainWin, destTxt, mylbl, map_wdg, WIDTH, HEIGHT))
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
    settings.destTxt.bind('<Button-1>',initKey)  

    map_wdg = tkintermapview.TkinterMapView(mylbl,width=WIDTH-200, height=HEIGHT-100, corner_radius=0)
    map_wdg.set_zoom(15)
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
        threading.Timer(2, lambda: checkStatus(mainWin, process)).start()
        print( "Running ")
        return True
    else:
        print("Closed / Stopped ")
        mainWin.deiconify()
        return False


def launchPlayer(mainWin,title ,link):
    mainWin.withdraw()
    import webbrowser
    # creating root
     
    command_list = "/usr/bin/matchbox-keyboard --fontfamily times --fontptsize 8"
    try:
        p = subprocess.Popen(command_list ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print( "Got Exception as :" , str(e))
        pass
    print( " Command ", command_list)
    # call webbrowser.open() function.
    webbrowser.open(link)
    checkStatus(mainWin, 'chrome')
    return 

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
    size_Plr_Icon = 0
    cbox_Padx = 0
    if settings.screen_Scalar == 1.0:
        size_Plr_Icon = 150
        cbox_Padx = 50
    else:
        size_Plr_Icon = int(150 / settings.screen_Scalar )
        cbox_Padx = int(50 / settings.screen_Scalar )


    imgOpen = ImageTk.PhotoImage(Image.open(IMG_OPEN).resize((size_Plr_Icon , size_Plr_Icon), Image.ANTIALIAS))
    imgPlay = ImageTk.PhotoImage(Image.open(IMG_PLAY).resize((size_Plr_Icon , size_Plr_Icon), Image.ANTIALIAS))
    imgPause = ImageTk.PhotoImage(Image.open(IMG_PAUSE).resize((size_Plr_Icon , size_Plr_Icon), Image.ANTIALIAS))
    imgStop = ImageTk.PhotoImage(Image.open(IMG_STOP).resize((size_Plr_Icon , size_Plr_Icon), Image.ANTIALIAS))
    

    def get_value(event):
        settings.play_Options = ply_choice.get()
        print(" You have choosen to play " + settings.play_Options + " video")


    ply_choice = StringVar()
    cbox_video = ttk.Combobox(window, textvariable=ply_choice, font= settings.myFont)
    cbox_video.pack(side=LEFT,padx=cbox_Padx)

    cbox_video['values'] = [ 'live', 'recorded' ]
    cbox_video['state'] = 'readonly'
    cbox_video.bind('<<ComboboxSelected>>', get_value)

    openbtn = Button(window, text='Open', image=imgOpen, command=lambda: open_file(videoplayer, window, dir_Video))
    openbtn.pack(side=LEFT, padx=cbox_Padx)

    playbtn = Button(window, text='Play Video', image=imgPlay, command=lambda: playAgain(videoplayer))
    playbtn.pack(side=LEFT, padx=cbox_Padx)

    pausebtn = Button(window, text='Pause Video', image=imgPause, command=lambda: PauseVideo(videoplayer))
    pausebtn.pack(side=LEFT, padx=cbox_Padx)

    stopbtn = Button(window, text='Stop Video', image=imgStop ,command=lambda: StopVideo(videoplayer))
    stopbtn.pack(side=LEFT, padx=cbox_Padx)

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing( window, mainWin))
    window.mainloop()
    return

def optionVideo(value):
    settings.enablebackVideo=value
    return

def playbackVid(width , height):
    print(" Came heree .... ")
    username = str(getpass.getuser()) 
    ### Put here path of the file / script to be launched
    #command_list = "source /home/" 
    #command_list += username
    #command_list += "/tflite1/tflite1-env/bin/activate ;"
    command_list = "/usr/bin/python3 " 
    command_list += settings.OBJECT_DETECT_BIN_PATH
    command_list +="/playLive.py --modeldir Sample_TFLite_model/ --width "
    command_list += str(width)
    command_list += " --height "
    command_list += str(height)
    if settings.enablebackVideo is True:
        command_list += " &"

    print( " Command ", command_list)
    try:
        p = subprocess.Popen(command_list ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print( "Got Exception as :" , str(e))
        pass

def checkOptions(newWindow, mainWin):
    WIDTH, HEIGHT = newWindow.winfo_screenwidth(), newWindow.winfo_screenheight()
    on_closing(newWindow, mainWin)
    try:
        playbackVid(WIDTH, HEIGHT)
        checkStatus(mainWin, 'python3 /home/pi/NextGenDriving/NextGensoftware/playLive.py')
    except Exception as err:
        print( " Got Exception while playing ", str(err))
        pass


def adasGui(mainWin):
    #mainWin.withdraw()

    window = Toplevel()
    window.resizable(0,0)

    window.title(" ------ ADAS Options ------ ")
    WIDTH, HEIGHT = window.winfo_screenwidth(),window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (WIDTH, HEIGHT-100))
    window.configure(bg="black")
    
    rad_X=0
    rad_Y=0
    lbl_X= 0
    lbl_Y= 0 
    diffX_Pad = 0
    btnSubmit_Wd=0
    btnSubmit_Ht=0
    iconSize = 0 
    btnLive_X = 0
    if settings.screen_Scalar == 1.0:
        rad_X=100
        rad_Y=75
        lbl_X= 100
        lbl_Y= 150
        chkBox_Y =  450 
        chkBox_X =  100 
        diffX_Pad = 320
        btnSubmit_Wd=100
        btnSubmit_Ht=250
        iconSize = 300 
        btnLive_X = 450

    else:
        rad_X= int(100 / settings.screen_Scalar)
        rad_Y= int(75 / settings.screen_Scalar)
        lbl_X= int(100 / settings.screen_Scalar)
        lbl_Y= int(150 / settings.screen_Scalar)
        chkBox_Y = int(450 / settings.screen_Scalar)
        chkBox_X = int(100 / settings.screen_Scalar)
        diffX_Pad = int(320 / settings.screen_Scalar)
        btnSubmit_Wd = int(100 / settings.screen_Scalar)
        btnSubmit_Ht = int(290 / settings.screen_Scalar)
        iconSize = int(300 / settings.screen_Scalar)
        btnLive_X = int(450 / settings.screen_Scalar)

    def selection(choice, window, mainWin):
        settings.adas_Choice = choice.lower()
        print(" Selected Option for Adas : ", settings.adas_Choice)
        
        file1 = open(settings.FILE_PATH_OPTION , "w")
        file1.writelines(settings.adas_Choice)
        file1.close()

        if "live" == settings.adas_Choice :
            checkOptions(window,mainWin)

        elif "settings" == settings.adas_Choice :
            optionSel = [ 'Car', 'Bike', 'Animal', 'Speed', 'Pedestrian' ]
            newWindow = Toplevel()
            window.withdraw()
            WIDTH, HEIGHT = newWindow.winfo_screenwidth(), newWindow.winfo_screenheight()
            newWindow.geometry("%dx%d+0+0" % (WIDTH, HEIGHT-100))
            newWindow.configure(bg="black")
            settings.selected_Option.clear()
            common_bg = "blue" 

            backVideo = IntVar()
            r1 = Radiobutton(newWindow, text="ON", width= 10, bg="black", selectcolor = common_bg ,fg="white", font=settings.adasFont, highlightthickness=0, activebackground = "black", activeforeground="white", variable=backVideo, value=1, command= lambda: optionVideo(True))
            #r1.pack(side=LEFT, padx=20)
            r1.grid(row=0, column=0, padx=rad_X, pady=rad_Y)

            r2 = Radiobutton(newWindow, text="OFF", width=10, bg="black", selectcolor = common_bg, fg="white", font=settings.adasFont, highlightthickness=0, activebackground="black", activeforeground="white" ,variable=backVideo, value=0, command= lambda: optionVideo(False))
            #r2.pack(side=LEFT, padx=20)
            r2.grid(row=0, column=1, padx=rad_X, pady=rad_Y)

            def getVal(event):
                settings.speed_Limit = sp_choice.get()
                print( " Speed Limit set to : " + settings.speed_Limit + " Km/hr")

            lblSpeed = Label(newWindow,text="Speed(Km/hr) :", font=settings.optionFont, fg="white", bd=0, highlightthickness=0, activebackground="black", activeforeground = "black" , bg="black")
            #lblSpeed.pack(anchor=N, padx=20, pady=100)
            lblSpeed.grid(row=2, column=0, padx= lbl_X , pady= lbl_Y)
            sp_choice = StringVar()
            cbox_video = ttk.Combobox(newWindow, textvariable=sp_choice, font= settings.optionFont)
            #cbox_video.pack(anchor=N, padx=100, pady=100)
            cbox_video.grid(row=2, column=1, padx= lbl_X , pady= lbl_Y)

            cbox_video['values'] = ['0', '20', '40', '60' ]
            cbox_video['state'] = 'readonly'
            cbox_video.bind('<<ComboboxSelected>>', getVal)
            
            diffX=0
            for x in range(len(optionSel)):
                l = Checkbutton(newWindow, bg="black", fg="white", selectcolor="blue", bd=0, highlightthickness=0, activebackground="black", activeforeground="white", text=optionSel[x], variable=optionSel[x].lower(),command=lambda x=optionSel[x]:settings.selected_Option.append(x), font= settings.optionFont)
                #l.pack(anchor=N, pady=150 + diffY)
                #l.grid(row=3, column=0 + diffX, padx=30, pady=180)
                l.place(x= chkBox_X + diffX, y= HEIGHT-chkBox_Y)
                diffX += diffX_Pad

            Button(newWindow,text="Submit",bg="black",fg="white", activebackground = "black", activeforeground="black",font= settings.adasFont, command=lambda: [print(settings.selected_Option),newWindow.destroy(),window.destroy()]).place(x=WIDTH/2 - btnSubmit_Wd, y= HEIGHT-btnSubmit_Ht)
            #.grid(row=3,column=1, padx=300, pady=10)
            newWindow.attributes('-topmost',True)
            newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing( newWindow, window))
            newWindow.mainloop()

    
    dirAdas = os.path.join(settings.BASE_DIR, settings.ADAS_DIR)
    file_Live = os.path.join(dirAdas, settings.FILE_ADAS_LIVE)
    file_Settings = os.path.join(dirAdas, settings.FILE_ADAS_SETTING)

    imgLive = ImageTk.PhotoImage(Image.open(file_Live).resize((iconSize,iconSize), Image.ANTIALIAS))
    imgSettings = ImageTk.PhotoImage(Image.open(file_Settings).resize((iconSize,iconSize), Image.ANTIALIAS))
    
    btnLive = Button(window, image=imgLive, bg="black",highlightthickness=0,bd=0,activeforeground='white', activebackground='black', compound=CENTER, command= lambda: selection("live", window, mainWin,))
    
    btnSettings = Button(window, image=imgSettings, bg="black",highlightthickness=0,bd=0,activeforeground='white', activebackground='black', compound=CENTER, command= lambda: selection("settings", window, mainWin))
    
    btnLive.pack(side=LEFT,padx=btnLive_X, pady=30)
    btnSettings.pack(side=LEFT, padx=5,pady=30)

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
            streamer.log("Location", "{lat},{lon}".format(lat=settings.gpsLat,lon=settings.gpsLong))
            print(" Lattitude : " + str(settings.gpsLat))
            print(" Longitude : " + str(settings.gpsLong))
            print(" Speed : " + str(settings.gpsSpeed) + " km/h")
            sleep(0.15)
        except Exception as err:
            pass
    print(" Exiting GPS thread ...")
