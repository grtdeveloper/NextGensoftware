import tkinter as tk
from tkinter import ttk

key = tk.Tk()  # key window name
key.title('--- Keypad  ---')  # title Name

exp = " "          # global variable 
# showing all data in display 

def press(num):
    global exp
    exp=exp + str(num)
    equation.set(exp)
# end 


# function clear button

def clear():
    global exp
    exp = " "
    equation.set(exp)

# end 


# Enter Button Work Next line Function

def action():
  exp = " Next Line : "
  equation.set(exp)

# end function coding



# Size window size
key.geometry('1580x250')         # normal size
key.maxsize(width=1580, height=250)      # maximum size
key.minsize(width= 1580 , height = 250)     # minimum size
# end window size

key.configure(bg = 'white')    #  add background color

# entry box
equation = tk.StringVar()
Dis_entry = ttk.Entry(key,state= 'readonly',textvariable = equation)
Dis_entry.grid(rowspan= 1 , columnspan = 100, ipadx = 999 , ipady = 20)
# end entry box

# add all button line wise 

# First Line Button

keyWidth=8

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

cur = ttk.Button(key,text = '-' , width = keyWidth, command = lambda : press('-'))
cur.grid(row = 1 , column = 10 , ipadx = keyWidth , ipady = 10)

cur_c = ttk.Button(key,text = '=' , width = keyWidth, command = lambda : press('='))
cur_c.grid(row = 1 , column = 11, ipadx = keyWidth , ipady = 10)


clear = ttk.Button(key,text = 'Clear' , width = keyWidth, command = clear)
clear.grid(row =4 , columnspan = 12 , ipadx = keyWidth , ipady = 10)

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


d_colon = ttk.Button(key,text = '"' , width = keyWidth, command = lambda : press('"'))
d_colon.grid(row = 2 , column = 10, ipadx = keyWidth , ipady = 10)


enter = ttk.Button(key,text = 'Enter' , width =5, command = action)
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


q_mark = ttk.Button(key,text = '?' , width = keyWidth, command = lambda : press('?'))
q_mark.grid(row = 3 , column = 10, ipadx = keyWidth , ipady = 10)


coma = ttk.Button(key,text = ',' , width = keyWidth, command = lambda : press(','))
coma.grid(row = 3 , column = 11, ipadx = keyWidth , ipady = 10)

shift = ttk.Button(key,text = 'Shift' , width = keyWidth , command = lambda : press('Shift'))
shift.grid(row = 4 , column = 4 , ipadx =keyWidth , ipady = 10)

#Fourth Line Button


ctrl = ttk.Button(key,text = 'Ctrl' , width = keyWidth, command = lambda : press('Ctrl'))
ctrl.grid(row = 4 , column = 0, ipadx = keyWidth , ipady = 10)


Fn = ttk.Button(key,text = 'Fn' , width = keyWidth, command = lambda : press('Fn'))
Fn.grid(row = 4 , column = 1, ipadx = keyWidth , ipady = 10)


window = ttk.Button(key,text = 'Window' , width = keyWidth, command = lambda : press('Window'))
window.grid(row = 4 , column = 2 , ipadx = keyWidth , ipady = 10)

Alt = ttk.Button(key,text = 'Alt' , width = keyWidth, command = lambda : press('Alt'))
Alt.grid(row = 4 , column = 3 , ipadx = keyWidth , ipady = 10)

space = ttk.Button(key,text = 'Space' , width = keyWidth + 37, command = lambda : press(' '))
space.grid(row = 4 , columnspan = 33, ipadx = 7 , ipady = 10)

back_slash = ttk.Button(key,text = '\\' , width = 6, command = lambda : press('\\'))
back_slash.grid(row = 4 , columnspan = 87, ipadx = 10 , ipady = 10)

dot = ttk.Button(key,text = '.' , width = keyWidth, command = lambda : press('.'))
dot.grid(row = 4 , columnspan = 220, ipadx = 0 , ipady = 10)


key.mainloop()  # using ending point
