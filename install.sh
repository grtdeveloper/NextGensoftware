#!/bin/sh

echo " Updating and Upgrading Software "
sudo apt-get update
sudo apt-get upgrade

echo " Installing python packages "

sudo apt-get install python3-dev python3-pip

echo " Installing opencv package "

sudo pip3 install -U opencv-python

echo " Installing Supporing Camera libraries "

sudo apt install -y libgl1-mesa-glx

sudo pip3 install picamera

sudo apt-get install -y matchbox-keyboard

echo "Installing correct keyboard layout"

sudo cp keyboard.xml /usr/share/matchbox-keyboard
