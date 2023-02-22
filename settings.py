
import os
from tkinter import *
#### Folders ####


BASE_DIR=os.getcwd() + "/gui"
THEME_DIR="background/"
BLUE_ICON_DIR="blue_images/"
YELLOW_ICON_DIR="yellow_images/"
RED_ICON_DIR="red_images/"
GRAY_ICON_DIR="gray_images/"
MAIN_ICON_DIR="main_page_icons/"
THEME_LIGHT="light_theme/"
THEME_DARK="dark_theme/"
INFOTAINMENT_DIR="infotainment/"
DIR_VIDEO_FILES="videos/"
DIR_MEDIA_ICONS="Player_icons/"

### Files ###
FILE_THEME_DARK="dark.png"
FILE_THEME_LIGHT="light.png"
FILE_ANIMAL="animal.png"
FILE_CAR="car.png"
FILE_BIKE="bike.png"
FILE_PEDESTRIAN="pedestrian.png"
FILE_SPEED="speed.png"

FILE_WIFI_CONNECT="wifi_enabled.png"
FILE_WIFI_DISCONNECT="wifi_disabled.png"

FILE_BLUETOOTH_CONNECT="bluetooth_enabled.png"
FILE_BLUETOOTH_CONNECT_DISCONNECT="bluetooth_disabled.png"

FILE_ADAS="adas.png"
FILE_GPS="gps.png"
FILE_INFOTAINMENT="infotainment.png"
FILE_VIDEO="video_record.png"

FILE_NETFLIX="netflix.png"
FILE_YOUTUBE="youtube.png"
FILE_SPOTIFY="spotify.png"

FILE_OPEN="open.png"
FILE_PLAY="play.png"
FILE_PAUSE="pause.png"
FILE_STOP="stop.png"

####### Variables / Parameters ######## 

THEME="Dark"
Impact=False

imgSpeed=""
imgPedestrian=""
imgAnimal=""
imgCar=""
imgBike=""

btn_Animal=None
btn_Car=None
btn_Bike=None
btn_Pedestrian=None
btn_Speed=None

btn_Adas=None
btn_Gps=None
btn_Infotainment=None
btn_Video=None

btn_Netflix=None
btn_Youtube=None
btn_Spotify=None
destTxt=None
mainFrame=None
showMap=False
status_GPS=True

obj_detect_vid="OFF"
speed_limit=0
col_warn_Animal="OFF"
col_warn_Car="OFF"
col_warn_Bike="OFF"
col_warn_Pedestrian="OFF"
col_warn_Speed="OFF"

play_Options=""
adas_Choice=""

gpsLat=12.9746179
gpsLong=77.691753
gpsSpeed=0
dest_address="" 
prev_gpsLat=12.9746179
prev_gpsLong=77.691753

LINK_YOUTUBE="https://www.youtube.com/watch?v=Mwrhf7TuUPw"
LINK_NETFLIX="https://www.netflix.com/in/Login"
LINK_SPOTIFY="https://accounts.spotify.com/en/login"

myFont= ('Helvetica 15 bold')
adasFont= ('Helvetica 25 bold')
