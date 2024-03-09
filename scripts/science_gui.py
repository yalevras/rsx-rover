import serial as ser
import time
import tkinter as tk

BUTTONWIDTH = 20
BUTTONHEIGHT = 2

#send data over serial bus, and print incoming data
def send_data(letter):
    ser.write(letter)
    #change the bit number to 16 if you remove the print statements in the arduino code
    print(ser.read(26)) 


m=tk.Tk()  #main window
m.title('Science Team Drill Controls')  #window title

#connect to arduino
try:
    ser = ser.Serial("/dev/ttyACM0", 9600)
    time.sleep(0.5)
except ser.serialutil.SerialException:
    print("Arduino not connected")


#Drill 1 Up
drill_1_up = tk.Button(m, text='Drill Up', 
                       width=BUTTONWIDTH*2, 
                       height= BUTTONHEIGHT, 
                       bg="yellow",
                       font= ('Helvetica 20 bold'),
                       command= lambda:send_data(b's'))
#Drill 1 Down
drill_1_down = tk.Button(m, text='Drill Down', 
                         width=BUTTONWIDTH*2,
                         height= BUTTONHEIGHT, 
                         bg="yellow",
                         font= ('Helvetica 20 bold'),
                         command= lambda:send_data(b'w'))
#Drill 1 FWD
drill_1_FWD = tk.Button(m, text='Drill CW', #this is usually what we want
                        width=BUTTONWIDTH*2, 
                        height= BUTTONHEIGHT,
                        bg="lightgreen",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'p'))
#Drill 1 REV
drill_1_REV = tk.Button(m, text='Drill CCW', 
                        width=BUTTONWIDTH*2,
                        height= BUTTONHEIGHT, 
                        bg="lightgreen",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'a'))


#Clockwise speed adjustment
drill_1_FWD_fast = tk.Button(m, text='Drill CW fast', 
                        width=BUTTONWIDTH,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'd'))

drill_1_FWD_slow = tk.Button(m, text='Drill CW slow', 
                        width=BUTTONWIDTH,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'o'))

drill_l_FWD_prec = tk.Button(m, text='CW precision', 
                        width=BUTTONWIDTH*2,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'j'))

#Counter clockwise speed adjustment
drill_1_REV_fast = tk.Button(m, text='Drill CCW fast', 
                        width=BUTTONWIDTH,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'e'))

drill_1_REV_slow = tk.Button(m, text='Drill CCW slow', 
                        width=BUTTONWIDTH,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'r'))

drill_l_REV_prec = tk.Button(m, text='CCW precision', 
                        width=BUTTONWIDTH*2,
                        height= BUTTONHEIGHT, 
                        bg="lightblue",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b't'))

#attach bit
drill_1_attachbit = tk.Button(m, text='Attach Bit', 
                        width=BUTTONWIDTH*2,
                        height= BUTTONHEIGHT, 
                        bg="orange",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'm'))

#remove bit
drill_1_removebit = tk.Button(m, text='Remove Bit', 
                        width=BUTTONWIDTH*2,
                        height= BUTTONHEIGHT, 
                        bg="orange",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'n'))

#Rotate bit changer
# B1 = tk.Button(m, text='B1', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'b1'))
# B2 = tk.Button(m, text='B2', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'b2'))
# B4 = tk.Button(m, text='B4', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'b4'))
# B5 = tk.Button(m, text='B5', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'b5'))

# ##rotate changer
f = tk.Button(m, text='BC FWD', 
                        width=5,
                        height= BUTTONHEIGHT, 
                        bg="pink",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'f'))
# i = tk.Button(m, text='BC FWD small', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'i'))
g = tk.Button(m, text='BC REV', 
                        width=5,
                        height= BUTTONHEIGHT, 
                        bg="pink",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'g'))
# y = tk.Button(m, text='BC REV small', 
#                         width=5,
#                         height= BUTTONHEIGHT, 
#                         bg="pink",
#                         font= ('Helvetica 20 bold'),
#                         command= lambda:send_data(b'y'))

fastdown = tk.Button(m, text='fast/down', 
                        width=BUTTONWIDTH*4,
                        height= BUTTONHEIGHT, 
                        bg="orange",
                        font= ('Helvetica 20 bold'),
                        command= lambda:send_data(b'b'))

# Specify Grid
tk.Grid.columnconfigure(m, index = 0, weight = 1)
tk.Grid.rowconfigure(m, 0,weight = 1)
tk.Grid.columnconfigure(m, index = 1, weight = 1)
tk.Grid.rowconfigure(m, 1,weight = 1)
tk.Grid.columnconfigure(m, index = 2, weight = 1)
tk.Grid.rowconfigure(m, 2,weight = 1)
tk.Grid.columnconfigure(m, index = 3, weight = 1)
tk.Grid.rowconfigure(m, 3,weight = 1)
tk.Grid.rowconfigure(m, 4,weight = 1)
tk.Grid.rowconfigure(m, 5,weight = 1)
tk.Grid.rowconfigure(m, 6,weight = 1)

#place buttons
drill_1_up.grid(row=0,column=0,columnspan=2,sticky="NSEW")
drill_1_down.grid(row=0,column=2,columnspan=2,sticky="NSEW")
drill_1_FWD.grid(row=1,column=0,columnspan=2,sticky="NSEW")
drill_1_REV.grid(row=1,column=2,columnspan=2,sticky="NSEW")

drill_1_FWD_fast.grid(row=2,column=0,sticky="NSEW")
drill_1_FWD_slow.grid(row=2,column=1,sticky="NSEW")
drill_1_REV_fast.grid(row=2,column=2,sticky="NSEW")
drill_1_REV_slow.grid(row=2,column=3,sticky="NSEW")

drill_1_attachbit.grid(row=5,column=0,columnspan=2,sticky="NSEW")
drill_1_removebit.grid(row=5,column=2,columnspan=2,sticky="NSEW")

drill_l_FWD_prec.grid(row=4,column=0,columnspan=2,sticky="NSEW")
drill_l_REV_prec.grid(row=4,column=2,columnspan=2,sticky="NSEW")

# B1.grid(row=6,column=0,columnspan=1,sticky="NSEW")
# B2.grid(row=6,column=1,columnspan=1,sticky="NSEW")
# B4.grid(row=6,column=2,columnspan=1,sticky="NSEW")
# B5.grid(row=6,column=3,columnspan=1,sticky="NSEW")


f.grid(row=6,column=0,columnspan=1,sticky="NSEW")
# i.grid(row=7,column=1,columnspan=1,sticky="NSEW")
g.grid(row=6,column=2,columnspan=1,sticky="NSEW")
# y.grid(row=7,column=3,columnspan=1,sticky="NSEW")

fastdown.grid(row=3,column=0,columnspan=4,sticky="NSEW")

m.mainloop()