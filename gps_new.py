#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading
import sys
 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
def getSpeed():
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
 
      print
      print (' GPS reading')
      print ('----------------------------------------')
      print ('latitude    ' + str(gpsd.fix.latitude))
      print ('longitude   ' + str(gpsd.fix.longitude))
      # print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print ('altitude (m)' + str(gpsd.fix.altitude))
      # print 'eps         ' , gpsd.fix.eps
      # print 'epx         ' , gpsd.fix.epx
      # print 'epv         ' , gpsd.fix.epv
      # print 'ept         ' , gpsd.fix.ept
      print ('speed (m/s) ' + str(gpsd.fix.speed))
      # file_path = '/home/pi/python-gps-examples/GPS_speed.txt'
      # sys.stdout = open(file_path, "w")
      # print(gpsd.fix.speed)
      # file_path.close()
            
      # print 'climb       ' , gpsd.fix.climb
      # print 'track       ' , gpsd.fix.track
      # print 'mode        ' , gpsd.fix.mode
      # print
      # print 'sats        ' , gpsd.satellites
 
      time.sleep(0.01) #set to whatever
      
      speed = 0
      prev_speed = 0
      if str(gpsd.fix.speed) != 'nan':
          myFile = open("/home/pi/tflite1/NextGenDriving/NextGenDriving/GPS_speed.txt", "w")
          myFile.write(str(gpsd.fix.speed))
          myFile.close()
          speed = str(gpsd.fix.speed)
      else :
          myFile = open("/home/pi/tflite1/NextGenDriving/NextGenDriving/GPS_speed.txt", "w")
          myFile.write(str(speed))
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")
  
  return speed
  
#getSpeed()

