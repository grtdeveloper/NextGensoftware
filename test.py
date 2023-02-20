# Import Module
from tkinter import *
  
# Create Object
root = Tk()
  
# Set geometry
root.geometry("400x400")
  
# Add Image
login_btn = PhotoImage(file = "/home/pi/NextGenDriving/NextGensoftware/gui/main_page_icons/dark_theme/adas.png")
  
# Create button and image
img = Button(root, image = login_btn, borderwidth = 0, bg="white")
  
img.pack()
  
# Execute Tkinter
root.mainloop()
