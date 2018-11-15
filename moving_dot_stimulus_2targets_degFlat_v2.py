# Bi-directional moving trace from left to right and then come back

from psychopy import visual, core, event, monitors
import math
from win32api import GetSystemMetrics
import u3
import time
import numpy as np

i = 0
n = 0   # loops
t0 = time.time()

'USER INPUT HERE'
distance = 1        #cm, distance between the screen and larvae's head
diameter = 5       # degree, size of visual stimulus in terms of visual angle
h_ratio = 0.8
w_ratio = 1.6
speed = 20  # degrees per second
x_halfangle = 80        # degrees, moving distance from left to centre in terms of visual angle, which takes 1/4 of total time
moving_y_angle = 0       # degree, correction for moving trace in terms of vertical direction

# elevation = 0            # degrees
# direction = 1            # TODO modify the direction of moving stimulus

'PARAMETERS SPECIFICALLY FOR MOVING TRACE CORRECTION'
monitor_width = 31                            # cm
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
monitor_size = [width, height]                     # pixel
moving_time = x_halfangle*2/float(speed)             # second
print moving_time
moving_y_speed = float(moving_y_angle*2/moving_time)     # degree per second
position = [-x_halfangle,-moving_y_angle]           # degree, initial position
position2 = [x_halfangle,-moving_y_angle]

'SET MONITOR PARAMETETRS'
myMonitor = monitors.Monitor('X1_carbon',width = 31 ,distance = distance)
myMonitor.setSizePix(monitor_size)
myMonitor.saveMon()

'CREATE A WINDOW'
myWin = visual.Window(monitor_size, monitor=myMonitor, units='degFlat', color = (-1,-1,-1), fullscr=True)
# units when setting the Window actually means nothing, I think.

'''get the the average time per frame'''
frametime = myWin.getMsPerFrame(nFrames=60, showVisual=False, msg='', msDelay=0.0)[0]
# return the the average time per frame, with unit of ms
deg_per_frame = frametime*speed/1000
y_deg_per_frame = frametime*moving_y_speed/1000

'CREATE A STIMULUS'
myStim1 = visual.Polygon(win=myWin, edges=100, size = [diameter/w_ratio, diameter/h_ratio], units='degFlat', lineColor=[1,0,1], fillColor=[1,0,1], pos=position)
myStim2 = visual.Polygon(win=myWin, edges=100, size = [diameter/w_ratio, diameter/h_ratio], units='degFlat', lineColor=[1,0,1], fillColor=[1,0,1], pos=position2)


'DISPLAY THE STIMULUS'
timer = core.Clock()  # create a clock to record the moving duration
#myCentre.draw()
myStim1.draw()
myStim2.draw()
#leftEnd.draw()
#rightEnd.draw()
#myWin.update()
# ----------------------- START SYNCHRONIZATION RECEIVE TTL w/ LAB JACK ---------------------------------
dev = u3.U3()  # Open LJU3
dev.getCalibrationData()
dt = 100
dev = u3.U3()  # Open first found U3
#d.debug = True
dev.configIO(EnableCounter1 = True, TimerCounterPinOffset = 6) # set the counter to pin 4
#d.setDOState(ioNum=5, state=0)
print 'READING..'
print dev.getFeedback(u3.BitStateRead(IONumber =6))
#print d.getFeedback(u3.BitStateRead(IONumber =4))

print dev.getFeedback(u3.Counter(counter = 1))
t0 = time.time()

while True:
    trigger = int(np.array(dev.getFeedback(u3.Counter(counter = 1))))
#    print(trigger)
    if trigger > 0:
        t1 = time.time()
        break
print dev.getFeedback(u3.Counter(counter = 1))
print 'Total time'
print t1-t0

# k_1 = event.waitKeys()
timer.reset()
dev.setDOState(ioNum=4, state=0) # Set DAC0 to 4.5V
dev.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
dev.setDOState(ioNum=4, state=1)
dev.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
dev.setDOState(ioNum=4, state=0)
dev.getFeedback(u3.WaitShort(dt))

# --------------------- STIMULUS ------------------------------------


while position[0]<= x_halfangle:
    position2[0] -= deg_per_frame
    position2[1] -= y_deg_per_frame
    position[0] += deg_per_frame
    position[1] += y_deg_per_frame #for correct the moving trace
    myStim1.setPos(position)
    myStim1.draw()
    myStim2. setPos(position2)
    myStim2.draw()

    myWin.update()

timeUse = timer.getTime() # unit (s)
# print k_1, timeUse

#myWin.flip(clearBuffer=True)
time.sleep(0.5)
dev.setDOState(ioNum=4, state=0) # Set DAC0 to 4.5V
dev.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
dev.setDOState(ioNum=4, state=1)
dev.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
dev.setDOState(ioNum=4, state=0)
dev.getFeedback(u3.WaitShort(dt))

k_1 = event.waitKeys()
timer.reset()

'QUIT THE PROGRAM'
myWin.close()
core.quit()

