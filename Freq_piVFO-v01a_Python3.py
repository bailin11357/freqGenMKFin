# Freq_piVFO-v01a.py(w) (05-05-2017) VFO for freq_pi
# For Python version 3
# Created by Onno Hoekstra (pa2ohh)
import math
import subprocess
import time

from tkinter import *
from tkinter import font

# Values that can be modified
CANVASwidth = 800           # Width of the canvas
CANVASheight = 200          # Height of the canvas

FREQppm = 0.0               # Frequency correction in parts per million (ppm), positive or negative

FREQstp = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000] # Frequency step array in Hz
FREQptr = 3                 # index 3 from FREQstp as initial value

TIMEstp = [1, 3, 10, 30, 100, 300, 1000] # Sweep time array in ms
TIMEptr = 4                 # index 5 from TIMEstp as initial value


# Colors that can be modified
COLORframes = "#000080"     # Color = "#rrggbb" rr=red gg=green bb=blue, Hexadecimal values 00 - ff 
COLORcanvas = "#404040"
COLORtext = "#ffffff"


# Fontsizes that can be modified
FREQfontsize = 48           # Size of frequency text (Small=6, Large=48)
INFOfontsize = 8            # Size of info (Small=6, Large=24)

# Button sizes that can be modified
Buttonwidth1 = 8
Buttonwidth2 = 12            # (not used yet)

# Various global variables
TXfreq = 10000000           # The Frequency
STARTfreq = 9995000         # Startfrequency for sweep
STOPfreq = 10005000         # Stopfrequency for sweep
MINfreq = 245000            # Minimum Frequency
MAXfreq = 500000000         # Maximum Frequency

# Subprocess
Subname = "freq_pi_oh1"     # The name of the subprocess
RUNmode = 0                 # 0=OFF; 1=ON; 2=SWEEP ACTIVE; 3=RF BURST

# =================================== Start widgets routines ========================================
def Bnot():
    print ("Routine not made yet")


def BOn():
    global RUNmode

    RUNmode = 1
    SetFrequency()              # Set the frequency and activate the RF generator


def BOff():

    StopGen()


def BSweepStart():

    StartSweep()


def BFMn():
    global STARTfreq
    global STOPfreq
    global TXfreq

    STARTfreq = TXfreq + 2000   # 2 kHz deviation
    STOPfreq = TXfreq - 2000
    StartSweep()

    
def BFMw():
    global STARTfreq
    global STOPfreq
    global TXfreq

    STARTfreq = TXfreq + 20000   # 20 kHz deviation
    STOPfreq = TXfreq - 20000
    StartSweep()


def BAM():
    global STARTfreq
    global STOPfreq
    global TXfreq
    global MAXfreq

    STARTfreq = MAXfreq
    STOPfreq = TXfreq
    StartSweep()


def BTime1():
    global TIMEptr
    
    if (TIMEptr >= 1):
        TIMEptr = TIMEptr - 1

    UpdateScreen()          # UpdateScreen() call
    
    
def BTime2():
    global TIMEstp
    global TIMEptr
    
    if (TIMEptr < len(TIMEstp) - 1):
        TIMEptr = TIMEptr + 1

    UpdateScreen()          # UpdateScreen() call


def BFreq1():
    global FREQptr
    global FREQstp
    global MINfreq
    global TXfreq

    TXfreq = TXfreq - FREQstp[FREQptr]
    
    if (TXfreq < MINfreq ):
        TXfreq = MINfreq

    SetFrequency()

    UpdateScreen()          # UpdateScreen() call


def BFreq2():
    global FREQptr
    global FREQstp
    global MAXfreq
    global TXfreq

    TXfreq = TXfreq + FREQstp[FREQptr]
    
    if (TXfreq > MAXfreq ):
        TXfreq = MAXfreq
        
    SetFrequency()

    UpdateScreen()          # UpdateScreen() call
 

def BFreqStep1():
    global FREQptr

    if (FREQptr >= 1):
        FREQptr = FREQptr - 1

    UpdateScreen()          # UpdateScreen() call
    
    
def BFreqStep2():
    global FREQstp
    global FREQptr
    
    if (FREQptr < len(FREQstp) - 1):
        FREQptr = FREQptr + 1

    UpdateScreen()          # UpdateScreen() call

    
def BSetStartF():
    global STARTfreq
    global TXfreq

    STARTfreq = TXfreq

    UpdateScreen()          # UpdateScreen() call

    
def BSetStopF():
    global STOPfreq
    global TXfreq

    STOPfreq = TXfreq

    UpdateScreen()          # UpdateScreen() call


# ============================================ Main routine ====================================================


def UpdateScreen():         # Update screen with text
    MakeScreen()            # Update the text
    root.update()           # Activate updated screens    


def SetFrequency():       # Set the frequency
    global Subname
    global TXfreq
    global FREQppm
    global RUNmode

    if RUNmode == 1:
        rc = 0
        try:
            rc = subprocess.call(["sudo", Subname, "-f", str(TXfreq), "-y", str(FREQppm)])     # Set the frequency of the RF generator
        except:
            showwarning("ERROR!", "No subprocess: " + Subname)
            
        if rc != 0:
            showwarning("ERROR!", "Error in: " + Subname)

    UpdateScreen()          # UpdateScreen() call 


def StartSweep():           # Start the sweep
    global Subname
    global STARTfreq
    global STOPfreq
    global FREQstp
    global FREQptr
    global FREQppm
    global TIMEstp
    global TIMEptr
    global RUNmode

    if STARTfreq < STOPfreq:
        RUNmode = 2
    else:
        RUNmode = 3
    
    UpdateScreen()          # UpdateScreen() call 
       
    rc = 0
    try:
        rc = subprocess.call(["sudo", Subname, "-b", str(STARTfreq), "-d", str(int(1000*TIMEstp[TIMEptr])), "-e", str(STOPfreq), "-i", str(FREQstp[FREQptr]), "-y", str(FREQppm)])
    except:
        showwarning("ERROR!", "No subprocess: " + Subname)

    if rc != 0:
        showwarning("ERROR!", "Error in: " + Subname)

    StopGen()
    
    UpdateScreen()          # UpdateScreen() call 


def StopGen():              # Stop the RF generator
    global Subname
    global RUNmode
    
    rc = 0
    try:
        rc =  subprocess.call(["sudo", Subname, "-q"])     # Stop the RF generator
    except:
        showwarning("ERROR!", "No subprocess: " + Subname)
        
    if rc != 0:
        showwarning("ERROR!", "Error in: " + Subname)

    RUNmode = 0
    UpdateScreen()          # UpdateScreen() call 


def HzToMHz(fc):
    txt = str(int(fc))
    while len(txt) < 7:
        txt = "0" + txt
        
    txt = txt[:-6] + "." + txt[-6:]
    
    return(txt)


def MakeScreen():           # Update the text
    global FREQstp
    global FREQptr
    global TIMEstp
    global TIMEptr
    global TXfreq
    global STARTfreq
    global STOPfreq
    global FREQfont
    global INFOfont
    global CANVASwidth
    global CANVASheight
    global RUNmode


    # Delete all items on the screen
    de = ca.find_enclosed ( 0, 0, CANVASwidth+1000, CANVASheight+1000)   
    for n in de: 
        ca.delete(n)


    # Sweep info at top 
    txt = "Sweep: "
    txt = txt + "    Start: " + HzToMHz(STARTfreq) + " MHz" + "   Stop:" + HzToMHz(STOPfreq) + " MHz"
    txt = txt + "    Step: " + HzToMHz(FREQstp[FREQptr]) + " MHz" + "    Timestep: " + str(TIMEstp[TIMEptr]) + " ms" 
    x = 10
    y = 20
    idTXT = ca.create_text (x, y, text=txt, font=INFOfont, anchor=W, fill=COLORtext)


    # TX Frequency information and SWEEP ACTIVE
    if RUNmode < 2:
        txt = HzToMHz(TXfreq) + " MHz"
    if RUNmode == 2:
        txt = "SWEEP ACTIVE"
    if RUNmode == 3:
        txt = "RF BURST"

    x = 60
    y = CANVASheight / 2
    idTXT = ca.create_text(x, y, text=txt, font=FREQfont, anchor=W, fill=COLORtext)


    # Frequency step information and ON OFF at bottom
    if RUNmode == 0:
        txt = "OFF"
    else:
        txt = "ON"
        
    txt = txt + "     Frequency step: " + HzToMHz(FREQstp[FREQptr]) + " MHz"

    x = 10
    y = CANVASheight-20
    idTXT = ca.create_text (x, y, text=txt, font=INFOfont, anchor=W, fill=COLORtext)


# ================ Make Screen ==========================

root=Tk()
root.title("Freq_piVFO-v01a.py(w) (05-05-2017) VFO for freq_pi")

root.minsize(100, 100)

frame1 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame1.pack(side=TOP, expand=1, fill=X)

frame2 = Frame(root, background="black", borderwidth=5, relief=RIDGE)
frame2.pack(side=TOP, expand=1, fill=X)

frame3 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame3.pack(side=TOP, expand=1, fill=X)

ca = Canvas(frame2, width=CANVASwidth, height=CANVASheight, background=COLORcanvas)
ca.pack(side=TOP)

b = Button(frame1, text="ON", width=Buttonwidth1, command=BOn)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="OFF", width=Buttonwidth1, command=BOff)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="StartSweep", width=Buttonwidth1, command=BSweepStart)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="TimeStep+", width=Buttonwidth1, command=BTime2)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="TimeStep-", width=Buttonwidth1, command=BTime1)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="SetStop", width=Buttonwidth1, command=BSetStopF)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="SetStart", width=Buttonwidth1, command=BSetStartF)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="Frequency-", width=Buttonwidth1, command=BFreq1)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="Frequency+", width=Buttonwidth1, command=BFreq2)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="FreqStep-", width=Buttonwidth1, command=BFreqStep1)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="FreqStep+", width=Buttonwidth1, command=BFreqStep2)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="FM narrow", width=Buttonwidth1, command=BFMn)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="FM wide", width=Buttonwidth1, command=BFMw)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="AM", width=Buttonwidth1, command=BAM)
b.pack(side=RIGHT, padx=5, pady=5)



# Fonts, after initialisation of the tk screen! 
FREQfont = font.Font(size=FREQfontsize)
# FREQfont = font.Font(family="Helvetica", size=FREQfontsize, weight="bold")
INFOfont = font.Font(size=INFOfontsize)
# INFOfont = font.Font(family="Helvetica", size=INFOfontsize, weight="bold")


# ================ Call main routine ===============================
StopGen()                   # Stop the RF generator

root.update()               # Activate updated screens
root.mainloop()



