
import os
from tkinter import *
#### Folders ####
import getpass


OBJECT_DETECT_BIN_PATH=os.getcwd()

FILE_PATH = os.path.join("/home/" ,getpass.getuser())
FILE_GPS_SPEED = os.path.join(FILE_PATH, "tflite1/GPS_speed.txt")

FILE_PATH_OPTION = os.path.join(FILE_PATH, "Option.txt")

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
ADAS_DIR="adas/"


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
FILE_ADAS_LIVE="live.png"
FILE_ADAS_SETTING="setting.png"


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
speed_Limit=0
col_warn_Animal="OFF"
col_warn_Car="OFF"
col_warn_Bike="OFF"
col_warn_Pedestrian="OFF"
col_warn_Speed="OFF"

play_Options=""
adas_Choice=""
enablebackVideo=False
selected_Option=[]
mls = []
lat_lons={}
gpsLat=18.6229
gpsLong=73.7108
gpsSpeed=0
dest_address="" 
prev_gpsLat=18.229
prev_gpsLong=73.108
max_vehicle_speed=80
marker_1=None
marker_2=None
path_1=None
sock_Server=None
sock_Client=None
int_Bluetooth="bluetooth"
int_Wifi="wlan0"
addComplete=False
Finaladd=""
collision_object=""
collision_object_color="blue"
start_stop_back_detection=False
RAPID_API="15b148a9efmsh9434c399fd51e9ep1ad383jsn88c8ba54cf06"
MAP_URL="https://route-and-directions.p.rapidapi.com/v1/routing"
GEOCODE_URL="https://google-maps-geocoding.p.rapidapi.com/geocode/json"

screen_Scalar=1.0

LINK_YOUTUBE="https://www.youtube.com/"
LINK_NETFLIX="https://www.netflix.com/"
LINK_SPOTIFY="https://accounts.spotify.com"

myFont= ('Helvetica 15 bold')
optionFont= ('Helvetica 25 bold')
adasFont= ('Helvetica 45 bold')
