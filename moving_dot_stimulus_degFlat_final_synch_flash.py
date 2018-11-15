# Bi-directional moving trace from left to right and then come back

from psychopy import visual, core, event, monitors
import math
from win32api import GetSystemMetrics
# for labjack
import u3
import time
from time import sleep
import numpy as np

'USER INPUT HERE'
distance = 1         #cm, distance between the screen and larvae's head
diameter =  0.000000000005    # degree, size of visual stimulus in terms of visual angle
rect_position = [-40,0] #center of the retangle
width_rect = 80
height_rect = 5
freq = 4 #higher the freq, less frequency

h_ratio = 0.8
w_ratio = 1.6
speed = 40  # degrees per second
x_halfangle = 80        # degrees, moving distance from left to centre in terms of visual angle, which takes 1/4 of total time
moving_y_angle = 0       # degree, correction for moving trace in terms of vertical direction
ntimes = 1
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
myStim = visual.Polygon(win=myWin, edges=100, size = [diameter/w_ratio, diameter/h_ratio], units='degFlat', lineColor=[1.0,0,1], fillColor=[1.0,0,1], pos=position)
rect = visual.Rect(win=myWin, width=width_rect, height=height_rect, units='degFlat', lineColor=[1.0,0,1], fillColor=[1.0,0,1], pos=rect_position)


'DISPLAY THE STIMULUS'
timer = core.Clock()  # create a clock to record the moving duration
#myCentre.draw()
myStim.draw()
#leftEnd.draw()
#rightEnd.draw()
myWin.update()


# # for labjack
# # ----------------------- START SYNCHRONIZATION RECEIVE TTL w/ LAB JACK ---------------------------------
# d = u3.U3()  # Open LJU3
# d.getCalibrationData()
#
# #d.debug = True
# d.configIO(EnableCounter1 = True, TimerCounterPinOffset = 6) # set the counter to pin 4
# #d.setDOState(ioNum=5, state=0)
# print 'READING..'
# print d.getFeedback(u3.BitStateRead(IONumber =6))
# #print d.getFeedback(u3.BitStateRead(IONumber =4))
#
# print d.getFeedback(u3.Counter(counter = 1))
# t0 = time.time()
#
# while True:
#     trigger = int(np.array(d.getFeedback(u3.Counter(counter = 1))))
# #    print(trigger)
#     if trigger > 0:
#         t1 = time.time()
#         break
# print d.getFeedback(u3.Counter(counter = 1))
# print 'Total time'
# print t1-t0
# # ----------------------- ----------------------------------------------------------------------------------
# '''
#
# d = u3.U3()  # Open LJU3
# d.getCalibrationData()
# k_1 = event.waitKeys()
# '''
#
# timer.reset()
# dt = 100
# d.setDOState(ioNum=4, state=0) # Set DAC0 to 4.5V
# d.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
# d.setDOState(ioNum=4,state=1)
# d.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
# d.setDOState(ioNum=4, state=0)

# --------------------- STIMULUS ------------------------------------
for loop in range(0,ntimes):

    time.sleep(1)  # delay for 5 s  ###DT-tag

    count = 0
    while position[0]<= x_halfangle:
        if count < freq:
            position[0] += deg_per_frame
            position[1] += y_deg_per_frame #for correct the moving trace
            myStim. setPos(position)
            myStim.draw()
            myWin.update()
            count += 1
        else:
            position[0] += deg_per_frame
            position[1] += y_deg_per_frame #for correct the moving trace
            myStim. setPos(position)
            myStim.draw()
            rect.draw()
            myWin.update()
            count = 0

time.sleep(0.5)  # delay for 0.5 s
d.setDOState(ioNum=4, state=0) # Set DAC0 to 4.5V
d.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
d.setDOState(ioNum=4, state=1)
d.getFeedback(u3.WaitShort(dt))  # time delay is a multiple of 128 us
d.setDOState(ioNum=4, state=0)

timeUse = timer.getTime() # unit (s)

k_1 = event.waitKeys()
timer.reset()

'QUIT THE PROGRAM'
myWin.close()
core.quit()


