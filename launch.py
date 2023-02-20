from PIL import ImageTk
from tkinter import *
import tkinter as tk
import settings
import os
import os.path
import PIL.Image as Image
from ui import *
from customFunctions import showLocation, on_closing, launchPlayer, showVideo, adasGui
import threading

def showInfotain(mainWin):
    
    settings.mainFrame = mainWin
    mainWin.withdraw()
    newWindow = Toplevel()
    WIDTH, HEIGHT = mainWin.winfo_screenwidth(),mainWin.winfo_screenheight()
        
    newWindow.resizable(0,0)
    newWindow.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    newWindow.configure(bg="black")

    lblInfotain = tk.Label(newWindow,height = 400, width = WIDTH, bg="black")
    lblInfotain.place(x=0,y=HEIGHT/2 - 200)  # Place label in center of parent.
   
    dirInfotainment = os.path.join(settings.BASE_DIR,settings.INFOTAINMENT_DIR)

    IMAGE_NETFLIX = os.path.join(dirInfotainment, settings.FILE_NETFLIX)
    IMAGE_YOUTUBE = os.path.join(dirInfotainment, settings.FILE_YOUTUBE)
    IMAGE_SPOTIFY = os.path.join(dirInfotainment, settings.FILE_SPOTIFY)

    img_Netflix = ImageTk.PhotoImage(Image.open(IMAGE_NETFLIX).resize((300,300), Image.ANTIALIAS))
    img_Youtube = ImageTk.PhotoImage(Image.open(IMAGE_YOUTUBE).resize((300,300), Image.ANTIALIAS))
    img_Spotify = ImageTk.PhotoImage(Image.open(IMAGE_SPOTIFY).resize((300,300), Image.ANTIALIAS))

    settings.btn_Netflix = Button(lblInfotain, image=img_Netflix,bg="black",highlightthickness=0,bd=0,  activeforeground='black', activebackground='black', command= lambda: launchPlayer(newWindow,settings.LINK_NETFLIX))
    settings.btn_Youtube = Button(lblInfotain, image=img_Youtube,bg="black", highlightthickness=0 ,bd=0,  activeforeground='black', activebackground='black', command=lambda: launchPlayer(newWindow,settings.LINK_YOUTUBE))
    settings.btn_Spotify = Button(lblInfotain, image=img_Spotify,bg="black", highlightthickness=0 ,bd=0,  activeforeground='black', activebackground='black', command=lambda: launchPlayer(newWindow,settings.LINK_SPOTIFY))
    
    settings.btn_Netflix.grid(row=0, column=0, padx=150)
    settings.btn_Youtube.grid(row=0, column=1, padx=150)
    settings.btn_Spotify.grid(row=0, column=2, padx=150)

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
    lbl = tk.Label(root, image=img)
    lbl.img = img  # Keep a reference in case this code put is in a function.
    lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.
    
    WIFI_PATH= os.path.join(settings.BASE_DIR, settings.FILE_WIFI_CONNECT)
    wifiImg = ImageTk.PhotoImage(Image.open(WIFI_PATH).resize((50,50), Image.ANTIALIAS))
    
    BLUETOOTH_PATH= os.path.join(settings.BASE_DIR, settings.FILE_BLUETOOTH_CONNECT)
    bluetoothImg = ImageTk.PhotoImage(Image.open(BLUETOOTH_PATH).resize((50,50), Image.ANTIALIAS))

    # Add other tkinter widgets.
    btn_Wifi = tk.Button(root, image=wifiImg, bg="black",highlightthickness=0,bd=0,activeforeground='black', activebackground='black')
    btn_Wifi.place(x=50, y=10)
    btn_Bluetoth = tk.Button(root, image=bluetoothImg, bg="black",highlightthickness=0,bd=0,activeforeground='black', activebackground='black')
    btn_Bluetoth.place(x=120,y=10)
    
    lblPlaceholder = tk.Label(root, background="#0C3744",activeforeground='#0C3744', activebackground='#0C3744', bd=0, highlightthickness=0, height = 100, width = WIDTH-250)
    lblPlaceholder.place(x=WIDTH/2 -650,y=150)  # Place label in center of parent.
    
    if settings.Impact is False:
        dirIcon = settings.BLUE_ICON_DIR
    elif settings.Impact is True:
        dirIcon = settings.RED_ICON_DIR

    
    IMG_ANIMAL = os.path.join(settings.BASE_DIR,dirIcon,settings.FILE_ANIMAL)
    IMG_BIKE = os.path.join(settings.BASE_DIR,dirIcon,settings.FILE_BIKE)
    IMG_CAR = os.path.join(settings.BASE_DIR,dirIcon,settings.FILE_CAR)
    IMG_PEDESTRIAN =os.path.join(settings.BASE_DIR,dirIcon,settings.FILE_PEDESTRIAN)
    IMG_SPEED = os.path.join(settings.BASE_DIR,dirIcon,settings.FILE_SPEED)

    settings.imgAnimal = ImageTk.PhotoImage(Image.open(IMG_ANIMAL).resize((150,150), Image.ANTIALIAS))

    settings.imgBike = ImageTk.PhotoImage(Image.open(IMG_BIKE).resize((150,150), Image.ANTIALIAS))

    settings.imgCar = ImageTk.PhotoImage(Image.open(IMG_CAR).resize((150,150), Image.ANTIALIAS))
    settings.imgPedestrian = ImageTk.PhotoImage(Image.open(IMG_PEDESTRIAN).resize((150,150), Image.ANTIALIAS))
    settings.imgSpeed = ImageTk.PhotoImage(Image.open(IMG_SPEED).resize((150,150), Image.ANTIALIAS))

    settings.btn_Animal = Button(lblPlaceholder,image=settings.imgAnimal, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Bike = Button(lblPlaceholder, image=settings.imgBike, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Car = Button(lblPlaceholder, image=settings.imgCar, bg="#0C3744",highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Pedestrian = Button(lblPlaceholder, image=settings.imgPedestrian, bg="#0C3744", highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
    settings.btn_Speed = Button(lblPlaceholder, image=settings.imgSpeed, bg= "#0C3744", highlightthickness=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744')
   
    settings.btn_Animal.grid(row=0, column=0, padx=50)
    settings.btn_Bike.grid(row=0, column=1, padx=50)
    settings.btn_Car.grid(row=0, column=2, padx=50)
    settings.btn_Pedestrian.grid(row=0, column=3, padx=50)
    settings.btn_Speed.grid(row=0, column=4, padx=50)

    dirMain = ""
    if settings.THEME.lower() == "dark":
        dirMain = os.path.join(settings.BASE_DIR,settings.MAIN_ICON_DIR, settings.THEME_DARK)

    elif settings.THEME.lower()== "light":
        dirMain = os.path.join(settings.BASE_DIR,settings.MAIN_ICON_DIR, settings.THEME_LIGHT)


    IMG_ADAS = os.path.join(dirMain,settings.FILE_ADAS)
    IMG_VIDEO = os.path.join(dirMain,settings.FILE_VIDEO)
    IMG_GPS = os.path.join(dirMain,settings.FILE_GPS)
    IMG_INFOTAINMENT = os.path.join(dirMain,settings.FILE_INFOTAINMENT)
    
    settings.imgAdas = ImageTk.PhotoImage(Image.open(IMG_ADAS).resize((250,300), Image.ANTIALIAS))
    settings.imgVideo = ImageTk.PhotoImage(Image.open(IMG_VIDEO).resize((250,300), Image.ANTIALIAS))
    settings.imgGps = ImageTk.PhotoImage(Image.open(IMG_GPS).resize((250,300), Image.ANTIALIAS))
    settings.imgEnt = ImageTk.PhotoImage(Image.open(IMG_INFOTAINMENT).resize((250,300), Image.ANTIALIAS))

    '''
    lblHolder = tk.Label(root,height = 150, width = WIDTH, bg='#545F71', borderwidth=0)
    lblHolder.corner_radius = 8
    lblHolder.place(x=0,y=int(HEIGHT/2))  # Place label in center of parent.
    '''

    settings.btn_Adas = Button(root,image=settings.imgAdas, border="0", bg="#0C3744", highlightthickness=0,borderwidth=0,bd=0,activeforeground='#0C3744', activebackground='#0C3744', text="ADAS",font= settings.myFont, command = lambda: adasGui(root,))
    settings.btn_Video = Button(root,image=settings.imgVideo,border="0" ,bg="#0C3744" , highlightthickness=0,bd=0, activeforeground='#0C3744', activebackground='#0C3744', text= "VIDEO REC", font= settings.myFont, command= lambda :showVideo(os.path.join(settings.BASE_DIR,settings.DIR_VIDEO_FILES), root))
    settings.btn_Gps = Button(root,image=settings.imgGps, border="0", bg="#0C3744" ,highlightthickness=0 ,bd=0, activeforeground='#0C3744', activebackground= '#0C3744',text = "GPS", font=settings.myFont,command=lambda: gpsFunc(root,))
    settings.btn_Infotainment = Button(root,image=settings.imgEnt,border="0", bg="#0C3744" ,highlightthickness=0 ,bd=0,activeforeground='#0C3744',activebackground='#0C3744', text= "INFOTAINMENT", font=settings.myFont, command=lambda: showInfotain(root))

    settings.btn_Adas.grid(row=3, column=0, padx=100, pady=400)
    settings.btn_Video.grid(row=3, column=1, padx=100, pady=400)
    settings.btn_Gps.grid(row=3, column=2, padx=100, pady=400)
    settings.btn_Infotainment.grid(row=3, column=3, padx=100, pady=400)
    
    root.mainloop()


if __name__ == '__main__':
    create_gui()


