import tkinter as tk
from tkinter import ttk
import settings

def press(num):
    settings.entry_gpsText = str(num)
    print("Got Key as :", settings.entry_gpsText)
    settings.Finaladd += str(settings.entry_gpsText)

# function clear button

def cleanup():
    settings.entry_gpsText="clear"
    settings.Finaladd = ""
    settings.addComplete=False

# end 


# Enter Button Work Next line Function

def action(win):
  settings.addComplete=True
  win.destroy()

# end function coding

def initKey(event=None):
    key = tk.Tk()  # key window name
    key.title('--- Keypad  ---')  # title Name
    # get screen width and height
    
    ws = key.winfo_screenwidth() # width of the screen
    hs = key.winfo_screenheight() # height of the screen

    w = 1350
    h= 200
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    key.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Size window size
    #key.geometry('1350x200')         # normal size
    key.maxsize(width=1350, height=190)      # maximum size
    key.minsize(width= 1350 , height = 190)     # minimum size
    # end window size

    key.configure(bg = 'white')    #  add background color

    # entry box
    #settings.entry_gpsText = tk.StringVar()
    #Dis_entry = ttk.Entry(key,state= 'readonly',textvariable = settings.entry_gpsText)
    #Dis_entry.grid(rowspan= 1 , columnspan = 100, ipadx = 999 , ipady = 20)
    # end entry box

    # add all button line wise 

    # First Line Button

    keyWidth=6
    Style = ttk.Style ()
    Style.configure("TButton", font = ('Helvetica 15 bold'))

    q = ttk.Button(key,text = 'Q' , width = keyWidth, command = lambda : press('Q'))
    q.grid(row = 1 , column = 0, ipadx = keyWidth , ipady = 10)

    w = ttk.Button(key,text = 'W' , width = keyWidth, command = lambda : press('W'))
    w.grid(row = 1 , column = 1, ipadx = keyWidth , ipady = 10)

    E = ttk.Button(key,text = 'E' , width = keyWidth, command = lambda : press('E'))
    E.grid(row = 1 , column = 2, ipadx = keyWidth , ipady = 10)

    R = ttk.Button(key,text = 'R' , width = keyWidth, command = lambda : press('R'))
    R.grid(row = 1 , column = 3, ipadx = keyWidth , ipady = 10)

    T = ttk.Button(key,text = 'T' , width = keyWidth, command = lambda : press('T'))
    T.grid(row = 1 , column = 4, ipadx = keyWidth, ipady = 10)

    Y = ttk.Button(key,text = 'Y' , width = keyWidth, command = lambda : press('Y'))
    Y.grid(row = 1 , column = 5, ipadx = keyWidth , ipady = 10)

    U = ttk.Button(key,text = 'U' , width = keyWidth, command = lambda : press('U'))
    U.grid(row = 1 , column = 6, ipadx = keyWidth , ipady = 10)

    I = ttk.Button(key,text = 'I' , width = keyWidth, command = lambda : press('I'))
    I.grid(row = 1 , column = 7, ipadx = keyWidth , ipady = 10)

    O = ttk.Button(key,text = 'O' , width = keyWidth, command = lambda : press('O'))
    O.grid(row = 1 , column = 8, ipadx = keyWidth , ipady = 10)

    P = ttk.Button(key,text = 'P' , width = keyWidth, command = lambda : press('P'))
    P.grid(row = 1 , column = 9, ipadx = keyWidth , ipady = 10)

    cur = ttk.Button(key,text = '-' , width = keyWidth+2, command = lambda : press('--'))
    cur.grid(row = 1 , column = 10 , ipadx = keyWidth , ipady = 10)

    cur_c = ttk.Button(key,text = '=' , width = keyWidth +2, command = lambda : press('='))
    cur_c.grid(row = 1 , column = 11, ipadx = keyWidth , ipady = 10)

    num_7 = ttk.Button(key,text = '7' , width = keyWidth, command = lambda : press('7'))
    num_7.grid(row = 1 , column = 12, ipadx = keyWidth , ipady = 10)

    num_8 = ttk.Button(key,text = '8' , width = keyWidth, command = lambda : press('8'))
    num_8.grid(row = 1 , column = 13, ipadx = keyWidth , ipady = 10)

    num_9 = ttk.Button(key,text = '9' , width = keyWidth, command = lambda : press('9'))
    num_9.grid(row = 1 , column = 14, ipadx = keyWidth , ipady = 10)

    num_4 = ttk.Button(key,text = '4' , width = keyWidth, command = lambda : press('7'))
    num_4.grid(row = 2 , column = 12, ipadx = keyWidth , ipady = 10)

    num_5 = ttk.Button(key,text = '5' , width = keyWidth, command = lambda : press('5'))
    num_5.grid(row = 2 , column = 13, ipadx = keyWidth , ipady = 10)

    num_6 = ttk.Button(key,text = '6' , width = keyWidth, command = lambda : press('6'))
    num_6.grid(row = 2 , column = 14, ipadx = keyWidth , ipady = 10)

    num_3 = ttk.Button(key,text = '3' , width = keyWidth, command = lambda : press('3'))
    num_3.grid(row = 3 , column = 12, ipadx = keyWidth , ipady = 10)

    num_2 = ttk.Button(key,text = '2' , width = keyWidth, command = lambda : press('2'))
    num_2.grid(row = 3 , column = 13, ipadx = keyWidth , ipady = 10)

    num_1 = ttk.Button(key,text = '1' , width = keyWidth, command = lambda : press('1'))
    num_1.grid(row = 3 , column = 14, ipadx = keyWidth , ipady = 10)

    num_0 = ttk.Button(key,text = '0' , width = keyWidth, command = lambda : press('0'))
    num_0.grid(row = 4 , column = 13, ipadx = keyWidth , ipady = 10)

    key_underscore = ttk.Button(key,text = '_' , width = keyWidth, command = lambda : press('_'))
    key_underscore.grid(row = 4 , column = 12, ipadx = keyWidth , ipady = 10)

    clear = ttk.Button(key,text = 'Clear' , width = 5, command = cleanup())
    clear.grid(row =4 , columnspan = 11 , ipadx = 37, ipady = 10)

    #close_b = ttk.Button(key,text = ')' , width = keyWidth, command = lambda : press(')'))
    #close_b.grid(row = 4 , column = 12 , ipadx = keyWidth , ipady = 10)


    # Second Line Button



    A = ttk.Button(key,text = 'A' , width = keyWidth, command = lambda : press('A'))
    A.grid(row = 2 , column = 0, ipadx = keyWidth , ipady = 10)



    S = ttk.Button(key,text = 'S' , width = keyWidth, command = lambda : press('S'))
    S.grid(row = 2 , column = 1, ipadx = keyWidth , ipady = 10)

    D = ttk.Button(key,text = 'D' , width = keyWidth, command = lambda : press('D'))
    D.grid(row = 2 , column = 2, ipadx = keyWidth , ipady = 10)

    F = ttk.Button(key,text = 'F' , width = keyWidth, command = lambda : press('F'))
    F.grid(row = 2 , column = 3, ipadx = keyWidth , ipady = 10)


    G = ttk.Button(key,text = 'G' , width = keyWidth, command = lambda : press('G'))
    G.grid(row = 2 , column = 4, ipadx = keyWidth , ipady = 10)


    H = ttk.Button(key,text = 'H' , width = keyWidth, command = lambda : press('H'))
    H.grid(row = 2 , column = 5, ipadx = keyWidth , ipady = 10)


    J = ttk.Button(key,text = 'J' , width = keyWidth, command = lambda : press('J'))
    J.grid(row = 2 , column = 6, ipadx = keyWidth , ipady = 10)


    K = ttk.Button(key,text = 'K' , width = keyWidth, command = lambda : press('K'))
    K.grid(row = 2 , column = 7, ipadx = keyWidth , ipady = 10)

    L = ttk.Button(key,text = 'L' , width = keyWidth, command = lambda : press('L'))
    L.grid(row = 2 , column = 8, ipadx = keyWidth , ipady = 10)


    semi_co = ttk.Button(key,text = ';' , width = keyWidth, command = lambda : press(';'))
    semi_co.grid(row = 2 , column = 9, ipadx = keyWidth , ipady = 10)


    d_colon = ttk.Button(key,text = '"' , width = keyWidth +2, command = lambda : press('"'))
    d_colon.grid(row = 2 , column = 10, ipadx = keyWidth , ipady = 10)


    enter = ttk.Button(key,text = 'Enter' , width =5, command = lambda: action(key))
    enter.grid(row = 2 , column = 11, ipadx = 20 , ipady = 10)

    # third line Button

    Z = ttk.Button(key,text = 'Z' , width = keyWidth, command = lambda : press('Z'))
    Z.grid(row = 3 , column = 0, ipadx = keyWidth , ipady = 10)


    X = ttk.Button(key,text = 'X' , width = keyWidth, command = lambda : press('X'))
    X.grid(row = 3 , column = 1, ipadx = keyWidth , ipady = 10)


    C = ttk.Button(key,text = 'C' , width = keyWidth, command = lambda : press('C'))
    C.grid(row = 3 , column = 2, ipadx = keyWidth , ipady = 10)


    V = ttk.Button(key,text = 'V' , width = keyWidth, command = lambda : press('V'))
    V.grid(row = 3 , column = 3, ipadx = keyWidth , ipady = 10)

    B = ttk.Button(key, text= 'B' , width = keyWidth , command = lambda : press('B'))
    B.grid(row = 3 , column = 4 , ipadx = keyWidth ,ipady = 10)


    N = ttk.Button(key,text = 'N' , width = keyWidth, command = lambda : press('N'))
    N.grid(row = 3 , column = 5, ipadx = keyWidth , ipady = 10)


    M = ttk.Button(key,text = 'M' , width = keyWidth, command = lambda : press('M'))
    M.grid(row = 3 , column = 6, ipadx = keyWidth , ipady = 10)


    left = ttk.Button(key,text = '<' , width = keyWidth, command = lambda : press('<'))
    left.grid(row = 3 , column = 7, ipadx = keyWidth , ipady = 10)


    right = ttk.Button(key,text = '>' , width = keyWidth, command = lambda : press('>'))
    right.grid(row = 3 , column = 8, ipadx = keyWidth , ipady = 10)


    slas = ttk.Button(key,text = '/' , width = keyWidth, command = lambda : press('/'))
    slas.grid(row = 3 , column = 9, ipadx = keyWidth , ipady = 10)


    q_mark = ttk.Button(key,text = '?' , width = keyWidth+2, command = lambda : press('?'))
    q_mark.grid(row = 3 , column = 10, ipadx = keyWidth , ipady = 10)


    coma = ttk.Button(key,text = ',' , width = keyWidth+2, command = lambda : press(','))
    coma.grid(row = 3 , column = 11, ipadx = keyWidth , ipady = 10)

    shift = ttk.Button(key,text = 'Shift' , width = keyWidth , command = lambda : press('Shift'))
    shift.grid(row = 4 , column = 4 , ipadx =keyWidth , ipady = 10)

    #Fourth Line Button


    ctrl = ttk.Button(key,text = 'Ctrl' , width = keyWidth, command = lambda : press('Ctrl'))
    ctrl.grid(row = 4 , column = 0, ipadx = keyWidth , ipady = 10)


    Esc = ttk.Button(key,text = 'Esc' , width = keyWidth, command = lambda : press('Esc'))
    Esc.grid(row = 4 , column = 1, ipadx = keyWidth , ipady = 10)


    window = ttk.Button(key,text = 'Window' , width = keyWidth, command = lambda : press('Window'))
    window.grid(row = 4 , column = 2 , ipadx = keyWidth , ipady = 10)

    Alt = ttk.Button(key,text = 'Alt' , width = keyWidth, command = lambda : press('Alt'))
    Alt.grid(row = 4 , column = 3 , ipadx = keyWidth , ipady = 10)

    space = ttk.Button(key,text = 'Space' , width = keyWidth + 24, command = lambda : press(' '))
    space.grid(row = 4 , columnspan = 25, ipadx = 0 , ipady = 10)

    conn_amper = ttk.Button(key,text = '&' , width = 7, command = lambda : press('&'))
    conn_amper.grid(row = 4 , column = 10, ipadx = 10 , ipady = 10)

    dot = ttk.Button(key,text = '.' , width = keyWidth +3, command = lambda : press('.'))
    dot.grid(row = 4 , column = 11, ipadx = 0 , ipady = 10)


    key.mainloop()  # using ending point

