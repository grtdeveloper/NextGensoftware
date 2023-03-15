from PIL import ImageTk
from tkinter import *
import tkinter as tk
import settings
import os
import os.path
import PIL.Image as Image
from ui import *
from customFunctions import showLocation, on_closing, launchPlayer, showVideo, adasGui, getSpeed, RoundedButton, server_program, wifiStatus, bluetoothStatus
import threading
import signal
import time
import sys
 
def handler(signum, frame):
    res = input("Ctrl-c was pressed. Exiting!!! ")
    settings.status_GPS=False
    ### Close Sockets if not
    print( " ----  Closing All Sockets ---- ")
    if settings.sock_Server is not None:
        settings.sock_Server.close()  # close the connection
    if settings.sock_Client is not None:
        settings.sock_Client.close()  # close the connection
    sys.exit()
 
def closePgm():
    settings.status_GPS=False
    print( " Exiting Completely ")
    sys.exit()

def updateIcons(mainScreen, btn_Animal,btn_Bike,btn_Car,btn_Pedestrian,btn_Speed, red_dirIcon, yellow_dirIcon, blue_dirIcon):
    imgFile = ""
    print( " checked.. :" , (settings.collision_object.lower()) )
    if settings.speed_Limit <= settings.gpsSpeed :
        print(" Not Updating Screen As speed is under Threhold ") 
        
    elif settings.enablebackVideo is True and len(settings.selected_Option) > 0:
        print( " Update Icons ")
        if "Animal" in settings.selected_Option :
            if "animal" in settings.collision_object.lower() and settings.collision_object_color.lower() == "red":
                imgFile = os.path.join(red_dirIcon, settings.FILE_ANIMAL)
            elif "animal" in settings.collision_object.lower() and settings.collision_object_color.lower() == "yellow":
                imgFile = os.path.join(yellow_dirIcon, settings.FILE_ANIMAL)
            else:
                imgFile = os.path.join(blue_dirIcon, settings.FILE_ANIMAL)
            settings.imgAnimal = ImageTk.PhotoImage(Image.open(imgFile).resize((100,100), Image.ANTIALIAS))
            btn_Animal.configure(image=settings.imgAnimal)

        if "Bike" in settings.selected_Option:
            if "motorcycle" in settings.collision_object.lower() and settings.collision_object_color.lower() == "red":
                imgFile = os.path.join(red_dirIcon, settings.FILE_BIKE)
            if "motorcycle" in settings.collision_object.lower() and settings.collision_object_color.lower() == "yellow":
                imgFile = os.path.join(yellow_dirIcon, settings.FILE_BIKE)
            else:
                imgFile = os.path.join(blue_dirIcon, settings.FILE_BIKE)
            settings.imgBike = ImageTk.PhotoImage(Image.open(imgFile).resize((100,100), Image.ANTIALIAS))
            btn_Bike.configure(image=settings.imgBike)
        
        if "Car" in settings.selected_Option:
            if "car" in settings.collision_object.lower() and settings.collision_object_color.lower() == "red":
                imgFile = os.path.join(red_dirIcon, settings.FILE_CAR)
            elif "car" in settings.collision_object.lower() and settings.collision_object_color.lower() == "yellow":
                imgFile = os.path.join(yellow_dirIcon, settings.FILE_CAR)
            else:
                imgFile = os.path.join(blue_dirIcon, settings.FILE_CAR)
            settings.imgCar = ImageTk.PhotoImage(Image.open(imgFile).resize((100,100), Image.ANTIALIAS))
            btn_Car.configure(image=settings.imgCar)
        
        if "Pedestrian" in settings.selected_Option:
            if "pedestrian" in settings.collision_object.lower() and settings.collision_object_color.lower() == "red":
                imgFile = os.path.join(red_dirIcon, settings.FILE_PEDESTRIAN)
            elif "pedestrian" in settings.collision_object.lower() and settings.collision_object_color.lower() == "yellow":
                imgFile = os.path.join(yellow_dirIcon, settings.FILE_PEDESTRIAN)
            else:
                imgFile = os.path.join(blue_dirIcon, settings.FILE_PEDESTRIAN)
            settings.imgPedestrian = ImageTk.PhotoImage(Image.open(imgFile).resize((100,100), Image.ANTIALIAS))
            btn_Pedestrian.configure(image=settings.imgPedestrian)

        if "Speed" in settings.selected_Option:
            if int(settings.max_vehicle_speed) > int(settings.gpsSpeed) :
                imgFile = os.path.join(blue_dirIcon, settings.FILE_SPEED)
                print( " Speed Limit Under with the Maximum speed ")
            elif int(settings.speed_Limit) == int(settings.gpsSpeed) :
                imgFile = os.path.join(yellow_dirIcon, settings.FILE_SPEED)
                print( " Speed Limit Matched the Maximum speed ")
            else:
                imgFile = os.path.join(red_dirIcon, settings.FILE_SPEED)
            print(" Vehicle speed is Above threshold ")
            settings.imgSpeed = ImageTk.PhotoImage(Image.open(imgFile).resize((100,100), Image.ANTIALIAS))
            btn_Speed.configure(image=settings.imgSpeed)
        mainScreen.update()
    mainScreen.after(250, lambda: updateIcons(mainScreen, btn_Animal,btn_Bike,btn_Car,btn_Pedestrian,btn_Speed, red_dirIcon, yellow_dirIcon, blue_dirIcon))
    return

def chkInterfaces(mainScreen,intBlt,intWifi,btn_Bluetoth, btn_Wifi):
    try:
        if wifiStatus(intWifi) is False:
            btn_Wifi.config(state="disabled")
            print("Wifi : Disabled")
        else:
            btn_Wifi.config(state="active")
            print("Wifi : Active")
        if bluetoothStatus() is False :
            btn_Bluetoth.config(state="disabled")
            print("Bluetooth : Disabled ")
        else:
            btn_Bluetoth.config(state="active")
            print("Bluetooth : Active ")
    except Exception as err:
        print(err)
        pass

    mainScreen.update()
    mainScreen.after(5000, lambda: chkInterfaces(mainScreen,intBlt,intWifi,btn_Bluetoth, btn_Wifi))
    return

def updateSpeed(mainScreen, btnSpeed):
    btnSpeed.itemconfig(tagOrId='text', text=str(settings.gpsSpeed) + " Km/hr")
    mainScreen.update()
    mainScreen.after(1000, lambda: updateSpeed(mainScreen, btnSpeed))
    return

def showInfotain(mainWin):
    
    settings.mainFrame = mainWin
    mainWin.withdraw()
    newWindow = Toplevel()
    WIDTH, HEIGHT = mainWin.winfo_screenwidth(),mainWin.winfo_screenheight()
        
    newWindow.resizable(0,0)
    newWindow.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    newWindow.configure(bg="black")

    height_Win = 0
    pos_lblInfo_Y = 0
    imgSize = 0
    pad_X = 0
    if settings.screen_Scalar == 1.0:
        height_Win = 400
        pos_lblInfo_Y = 200
        imgSize = 300
        pad_X = 150
    
    else:
        height_Win = int(400 / settings.screen_Scalar)
        pos_lblInfo_Y = int(200 / settings.screen_Scalar)
        imgSize = int(300 / settings.screen_Scalar)
        pad_X = int(150 / settings.screen_Scalar)


    lblInfotain = tk.Label(newWindow,height = height_Win, width = WIDTH, bg="black")
    lblInfotain.place(x=0,y=HEIGHT/2 - pos_lblInfo_Y)  # Place label in center of parent.
   
    dirInfotainment = os.path.join(settings.BASE_DIR,settings.INFOTAINMENT_DIR)

    IMAGE_NETFLIX = os.path.join(dirInfotainment, settings.FILE_NETFLIX)
    IMAGE_YOUTUBE = os.path.join(dirInfotainment, settings.FILE_YOUTUBE)
    IMAGE_SPOTIFY = os.path.join(dirInfotainment, settings.FILE_SPOTIFY)

    img_Netflix = ImageTk.PhotoImage(Image.open(IMAGE_NETFLIX).resize((imgSize , imgSize), Image.ANTIALIAS))
    img_Youtube = ImageTk.PhotoImage(Image.open(IMAGE_YOUTUBE).resize((imgSize , imgSize), Image.ANTIALIAS))
    img_Spotify = ImageTk.PhotoImage(Image.open(IMAGE_SPOTIFY).resize((imgSize , imgSize), Image.ANTIALIAS))

    settings.btn_Netflix = Button(lblInfotain, image=img_Netflix,bg="black",highlightthickness=0,bd=0,  activeforeground='black', activebackground='black', command= lambda: launchPlayer(newWindow," Netflix " ,settings.LINK_NETFLIX))
    settings.btn_Youtube = Button(lblInfotain, image=img_Youtube,bg="black", highlightthickness=0 ,bd=0,  activeforeground='black', activebackground='black', command=lambda: launchPlayer(newWindow," Youtube " ,settings.LINK_YOUTUBE))
    settings.btn_Spotify = Button(lblInfotain, image=img_Spotify,bg="black", highlightthickness=0 ,bd=0,  activeforeground='black', activebackground='black', command=lambda: launchPlayer(newWindow," Spotify " ,settings.LINK_SPOTIFY))
    
    settings.btn_Netflix.grid(row=0, column=0, padx=pad_X)
    settings.btn_Youtube.grid(row=0, column=1, padx=pad_X)
    settings.btn_Spotify.grid(row=0, column=2, padx=pad_X)

    newWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(newWindow, mainWin))
    newWindow.mainloop()


def gpsFunc(mainWin):
    settings.showMap=True
    gpsThr = threading.Thread(target=showLocation, args=(mainWin,settings.showMap,))
    gpsThr.start()


def create_gui():
    IMAGE_PATH = ""
    if settings.THEME.lower() == "dark": 
        IMAGE_PATH = os.path.join(settings.BASE_DIR, settings.THEME_DIR, settings.FILE_THEME_DARK)
    else:
        IMAGE_PATH = os.path.join(settings.BASE_DIR, settings.THEME_DIR, settings.FILE_THEME_LIGHT)

    root = tk.Tk()
    
    WIDTH, HEIGHT = root.winfo_screenwidth(),root.winfo_screenheight()
        
    print("Width and height :", (WIDTH, HEIGHT))
    root.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    

    # Display image on a Label widget.
    img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGHT), Image.ANTIALIAS))
    lbl = tk.Label(root, image=img )
    lbl.img = img  # Keep a reference in case this code put is in a function.
    lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.
    
    WIFI_PATH= os.path.join(settings.BASE_DIR, settings.FILE_WIFI_CONNECT)
    wifiImg = ImageTk.PhotoImage(Image.open(WIFI_PATH).resize((50,50), Image.ANTIALIAS))
    
    BLUETOOTH_PATH= os.path.join(settings.BASE_DIR, settings.FILE_BLUETOOTH_CONNECT)
    bluetoothImg = ImageTk.PhotoImage(Image.open(BLUETOOTH_PATH).resize((50,50), Image.ANTIALIAS))

    # Add other tkinter widgets.
    btn_Wifi = tk.Button(root, image=wifiImg, bg="black",highlightthickness=0,bd=0,activeforeground='black', activebackground='black')
    btn_Wifi.place(x=25, y=10)
    btn_Bluetoth = tk.Button(root, image=bluetoothImg, bg="black",highlightthickness=0,bd=0,activeforeground='black', activebackground='black')
    btn_Bluetoth.place(x=90,y=10)
    
    settings.screen_Scalar = float(1920 / WIDTH)
    
    iconSize = 0
    icons_ht_wd=0
    pd_X=0
    pd_Y=0
    btnSpeed_X=0
    btnSpeed_Y=0
    placeH_width=0
    placeH_heigth=0
    placeH_posX=0
    placeH_posY=0
    
    print( "Got settings.screen_Scalar :", settings.screen_Scalar)
    if settings.screen_Scalar == 1.0:
        iconSize = 100
        icons_ht_wd= 300
        pd_X=80
        pd_Y=400
        btnSpeed_X=310
        btnSpeed_Y=180
        placeH_posX=500
        placeH_posY=125
        placeH_heigth=400
        placeH_width=250
    else:
        iconSize = int(100 / settings.screen_Scalar)
        icons_ht_wd = int(300 / settings.screen_Scalar)
        pd_X = int(65 / settings.screen_Scalar)
        pd_Y = int(400 / settings.screen_Scalar)
        btnSpeed_X = int(475 / settings.screen_Scalar)
        btnSpeed_Y = int(315 / settings.screen_Scalar)
        placeH_posX = int(700 / settings.screen_Scalar)
        placeH_posY= int(125 / settings.screen_Scalar)
        placeH_width=int(400 / settings.screen_Scalar)
        placeH_heigth= int(250 / settings.screen_Scalar)

    lblPlaceholder = tk.Label(root, background="#0C3744",activeforeground='#0C3744', activebackground='#0C3744', bd=0, highlightthickness=0, height = placeH_heigth , width = WIDTH- placeH_width)
    lblPlaceholder.place(x=WIDTH/2 - placeH_posX ,y=  placeH_posY)  # Place label in center of parent.
    
    blue_dirIcon = os.path.join(settings.BASE_DIR, settings.BLUE_ICON_DIR)
    red_dirIcon = os.path.join(settings.BASE_DIR, settings.RED_ICON_DIR)
    yellow_dirIcon = os.path.join(settings.BASE_DIR, settings.YELLOW_ICON_DIR)
    
    IMG_ANIMAL = os.path.join(blue_dirIcon,settings.FILE_ANIMAL)
    IMG_BIKE = os.path.join(blue_dirIcon,settings.FILE_BIKE)
    IMG_CAR = os.path.join(blue_dirIcon,settings.FILE_CAR)
    IMG_PEDESTRIAN =os.path.join(blue_dirIcon,settings.FILE_PEDESTRIAN)
    IMG_SPEED = os.path.join(blue_dirIcon,settings.FILE_SPEED)

    settings.imgAnimal = ImageTk.PhotoImage(Image.open(IMG_ANIMAL).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgBike = ImageTk.PhotoImage(Image.open(IMG_BIKE).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgCar = ImageTk.PhotoImage(Image.open(IMG_CAR).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgPedestrian = ImageTk.PhotoImage(Image.open(IMG_PEDESTRIAN).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgSpeed = ImageTk.PhotoImage(Image.open(IMG_SPEED).resize((iconSize,iconSize), Image.ANTIALIAS))

    settings.btn_Animal = Button(lblPlaceholder,image=settings.imgAnimal, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744', compound=CENTER)
    settings.btn_Bike = Button(lblPlaceholder, image=settings.imgBike, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Car = Button(lblPlaceholder, image=settings.imgCar, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Pedestrian = Button(lblPlaceholder, image=settings.imgPedestrian, bg="#0C3744", highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Speed = Button(lblPlaceholder, image=settings.imgSpeed, bg= "#0C3744", highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
   
    settings.btn_Animal.grid(row=0, column=0, padx=50, pady=20)
    settings.btn_Bike.grid(row=0, column=1, padx=50, pady=20)
    settings.btn_Car.grid(row=0, column=2, padx=50, pady=20)
    settings.btn_Pedestrian.grid(row=0, column=3, padx=50, pady=20)
    settings.btn_Speed.grid(row=0, column=4, padx=50, pady=20)

    dirMain = ""
    if settings.THEME.lower() == "dark":
        dirMain = os.path.join(settings.BASE_DIR,settings.MAIN_ICON_DIR, settings.THEME_DARK)

    elif settings.THEME.lower()== "light":
        dirMain = os.path.join(settings.BASE_DIR,settings.MAIN_ICON_DIR, settings.THEME_LIGHT)


    IMG_ADAS = os.path.join(dirMain,settings.FILE_ADAS)
    IMG_VIDEO = os.path.join(dirMain,settings.FILE_VIDEO)
    IMG_GPS = os.path.join(dirMain,settings.FILE_GPS)
    IMG_INFOTAINMENT = os.path.join(dirMain,settings.FILE_INFOTAINMENT)
    
    settings.imgAdas = ImageTk.PhotoImage(Image.open(IMG_ADAS).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgVideo = ImageTk.PhotoImage(Image.open(IMG_VIDEO).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgGps = ImageTk.PhotoImage(Image.open(IMG_GPS).resize((iconSize,iconSize), Image.ANTIALIAS))
    settings.imgEnt = ImageTk.PhotoImage(Image.open(IMG_INFOTAINMENT).resize((iconSize,iconSize), Image.ANTIALIAS))

    settings.btn_Adas = Button(root,image=settings.imgAdas, border="0", bg="#0C3744",height=icons_ht_wd, width=icons_ht_wd, highlightthickness=0,borderwidth=0,bd=0,activeforeground='white', activebackground='#0C3744', text="ADAS" ,fg="white", compound=TOP,font= settings.myFont, command = lambda: adasGui(root,))
    settings.btn_Video = Button(root,image=settings.imgVideo,border="0" ,bg="#0C3744",height=icons_ht_wd, width=icons_ht_wd, highlightthickness=0,bd=0, activeforeground='white', activebackground='#0C3744', text= "VIDEO REC",fg="white",compound=TOP, font= settings.myFont, command= lambda :showVideo(os.path.join(settings.BASE_DIR,settings.DIR_VIDEO_FILES), root))
    settings.btn_Gps = Button(root,image=settings.imgGps,border="0", bg="#0C3744", height=icons_ht_wd, width=icons_ht_wd,highlightthickness=0 ,bd=0, activeforeground='white', activebackground= '#0C3744',text = "GPS", fg="white", compound=TOP, font=settings.myFont, command=lambda: gpsFunc(root,))

    settings.btn_Infotainment = Button(root,image=settings.imgEnt,border="0", bg="#0C3744", height=icons_ht_wd, width=icons_ht_wd, highlightthickness=0 ,bd=0,activeforeground='white',activebackground='#0C3744', text= "INFOTAINMENT", fg="white", compound=TOP, font=settings.myFont, command=lambda: showInfotain(root))

    settings.btn_Adas.grid(row=3, column=0, padx=pd_X, pady=pd_Y)
    settings.btn_Video.grid(row=3, column=1, padx=pd_X, pady=pd_Y)
    settings.btn_Gps.grid(row=3, column=2, padx=pd_X, pady=pd_Y)
    settings.btn_Infotainment.grid(row=3, column=3, padx=pd_X, pady=pd_Y)
    
    btn_text =str(settings.gpsSpeed) + "Km/hr"
    btnSpeed = RoundedButton(root, text= btn_text, radius=20, btnbackground="white", btnforeground="black")

    btnSpeed.place(x=WIDTH-btnSpeed_X , y=HEIGHT-btnSpeed_Y)

    root.after(250, lambda: updateIcons(root, settings.btn_Animal, settings.btn_Bike, settings.btn_Car, settings.btn_Pedestrian, settings.btn_Speed, red_dirIcon, yellow_dirIcon, blue_dirIcon))
    
    root.after(1000, lambda: updateSpeed(root, btnSpeed))

    root.after(1000, lambda: chkInterfaces(root,settings.int_Bluetooth, settings.int_Wifi, btn_Bluetoth, btn_Wifi))

    root.protocol("WM_DELETE_WINDOW", closePgm)
    root.mainloop()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    sockThr = threading.Thread(target=server_program)
    speedThr = threading.Thread(target=getSpeed)
    sockThr.daemon = True 
    speedThr.daemon = True
    sockThr.start()
    speedThr.start()
    create_gui()



