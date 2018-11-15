# NOTE. Create a line of points to a
# lign the screen with the projector, making sure they're parallel


from psychopy import visual, core, event, monitors
import math

'USER INPUT HERE'
distance =  1     #cm, distance between the screen and larvae's head
radius = 1           #degree, size of visual stimulus in terms of visual angle
x_halfangle = 70     #degree
moving_y_angle = 0    #degree



'SET MONITOR PARAMETETRS'
monitor_width = 31                            # cm
monitor_size = [1280,720]                     # pixel
myMonitor = monitors.Monitor('X1_carbon',width = 31 ,distance = distance)
myMonitor.setSizePix(monitor_size)
myMonitor.saveMon()

'CREATE A WINDOW'
myWin = visual.Window(monitor_size, monitor=myMonitor, units='degFlat', color = (-1,-1,-1), fullscr=True)

color = [1,0,1]

'CREATE VISUAL STIMULUS'
myCentre = visual.Polygon(win=myWin, edges=100, radius = radius, units='degFlat', lineColor=color , fillColor=color , pos=[0,0])
leftmidEnd = visual.Polygon(win=myWin, edges=100, radius=radius, units='degFlat', lineColor=color , fillColor=color , pos=[-x_halfangle/2,-moving_y_angle])
rightmidEnd = visual.Polygon(win=myWin, edges=100, radius=radius, units='degFlat', lineColor=color , fillColor=color , pos=[x_halfangle/2,-moving_y_angle])
leftEnd = visual.Polygon(win=myWin, edges=100, radius=radius, units='degFlat', lineColor=color , fillColor=color , pos=[-x_halfangle,-moving_y_angle])
rightEnd = visual.Polygon(win=myWin, edges=100, radius=radius, units='degFlat', lineColor=color , fillColor=color , pos=[x_halfangle,-moving_y_angle])

'DISPLAY THE STIMULUS'
timer = core.Clock()  # create a clock to record the moving duration
myCentre.draw()
leftmidEnd.draw()
rightmidEnd.draw()
leftEnd.draw()
rightEnd.draw()
myWin.update()

k_1 = event.waitKeys()

'QUIT THE PROGRAM'
myWin.close()
core.quit()


