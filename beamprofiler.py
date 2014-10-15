# -*- coding: utf-8 -*-
"""
This example demonstrates the use of pyqtgraph's dock widget system.

The dockarea system allows the design of user interfaces which can be rearranged by
the user at runtime. Docks can be moved, resized, stacked, and torn out of the main
window. This is similar in principle to the docking system built into Qt, but 
offers a more deterministic dock placement API (in Qt it is very difficult to 
programatically generate complex dock arrangements). Additionally, Qt's docks are 
designed to be used as small panels around the outer edge of a window. Pyqtgraph's 
docks were created with the notion that the entire window (or any portion of it) 
would consist of dockable components.

"""



#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np

from pyqtgraph.dockarea import *

app = QtGui.QApplication([])
win = QtGui.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1600,700)
win.setWindowTitle('Beam Profiler')

## Create docks, place them into the window one at a time.
d1 = Dock("Image", size=(1200, 900))    
dx = Dock("x slice", size=(1,100))
dy = Dock("y slice", size=(100,1))
d3 = Dock("params", size=(450,1))
dp2 = Dock("params2", size=(450,1))
dc = Dock("console", size=(250,1))

area.addDock(d1, 'left')     
area.addDock(dx, 'bottom')    
area.addDock(dy, 'right')  
area.addDock(d3, 'right')
area.addDock(dp2, 'right')
area.addDock(dc, 'bottom')

dn = Dock("numbers", size=(250,1))
area.addDock(dn, 'right')

area.moveDock(dp2, 'top', d3)

dtime = Dock("time", size=(250,250))
area.addDock(dtime, 'bottom')

##
#wc = pg.console.ConsoleWidget()
#dc.addWidget(wc)
##

ptime = pg.PlotWidget(title="time")
dtime.addWidget(ptime)
ctime=ptime.plot([1], pen=(255,0,0))
ctime2=ptime.plot([2], pen=(0,255,0))

yslice = pg.PlotWidget(title="y slice")
dy.addWidget(yslice)
ycurve=yslice.plot(np.random.normal(size=100), pen=(255,0,0))
ycurve.rotate(-90)

xslice = pg.PlotWidget(title="x slice")
dx.addWidget(xslice)
xcurve=xslice.plot(np.random.normal(size=100), pen=(255,0,0))

##############################################################################
##vid

import numpy as np
import cv2

CV_CAP_DSHOW=700
CV_CAP_PROP_SETTINGS=37
cap = cv2.VideoCapture(CV_CAP_DSHOW+0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1024)
#cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, -10)
#cap.set(cv2.cv.CV_CAP_PROP_FPS, 60)
#cap.set(CV_CAP_PROP_SETTINGS,1)
#print cap.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)
#print cap.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
#print cap.get(cv2.cv.CV_CAP_PROP_CONTRAST)
#CV_CAP_PROP_DIALOG_DISPLAY= 8
#CV_CAP_PROP_DIALOG_FORMAT= 9
#CV_CAP_PROP_DIALOG_SOURCE= 10
#CV_CAP_PROP_DIALOG_COMPRESSION= 11
#CV_CAP_PROP_FRAME_WIDTH_HEIGHT= 12
#cap.set(CV_CAP_PROP_DIALOG_FORMAT, 1)

##############################################################################
##params


import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType


params = [
{'name': 'Infos', 'type': 'group', 'children': [
    {'name': 'x', 'type': 'float', 'value': 0},
    {'name': 'y', 'type': 'float', 'value': 0},
    {'name': 'db', 'type': 'float', 'value': 0},
    {'name': 'width', 'type': 'float', 'value': 0},
    {'name': 'height', 'type': 'float', 'value': 0}
    ]},
{'name': 'Camera', 'type': 'group', 'children': [
    {'name': 'exp', 'type': 'float', 'value': -0.04},
    {'name': 'fps', 'type': 'float', 'value': 25},
    {'name': 'bright', 'type': 'float', 'value': 25}
    ]},
{'name': 'Options', 'type': 'group', 'children': [
    {'name': 'autocross', 'type': 'bool', 'value': True},
    {'name': 'timesize', 'type': 'int', 'value': 1000},
    {'name': 'minSize', 'type': 'float', 'value': 0.5},
    {'name': 'maxSize', 'type': 'float', 'value': 3},
    {'name': 'Camera Type', 'type': 'list', 'values':['Monchrome Camera','Color Camera']}
    ]},    
]


## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)

## If anything changes in the tree, print a message
def cchange(param, changes):
    print("tree changes:")
#    print param.param("bright").value()
#    cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, param.param("exp").value())
#    cap.set(cv2.cv.CV_CAP_PROP_FPS, param.param("fps").value())    
#    cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, param.param("bright").value())      
#    print cap.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)        
#    print cap.get(cv2.cv.CV_CAP_PROP_FPS)       
#    cap.set(CV_CAP_PROP_SETTINGS,1)
#    for param, change, data in changes:
#        path = p.childPath(param)
#        if path is not None:
#            childName = '.'.join(path)
#        else:
#            childName = param.name()
#        print('  parameter: %s'% childName)
#        print('  change:    %s'% change)
#        print('  data:      %s'% str(data))
#        print('  ----------')
    
p.param("Camera").sigTreeStateChanged.connect(cchange)

wParams = ParameterTree()
wParams.setParameters(p, showTop=False)

d3.addWidget(wParams)

##############################################################################
## data tree
d = {}
tree = pg.DataTreeWidget(data=d)
dp2.addWidget(tree)

##############################################################################
##image
imv = pg.ImageView()
d1.addWidget(imv)
import scipy
vsize=(1280, 1024)
data = rdata= np.random.normal(size=vsize)/25
imv.setImage(data)

##############################################################################
##movable lines

vLine = pg.InfiniteLine(angle=90, movable=True)
hLine = pg.InfiniteLine(angle=0, movable=True)
imv.addItem(vLine, ignoreBounds=True)
imv.addItem(hLine, ignoreBounds=True)
vLine.setPos(vsize[0]/2)
hLine.setPos(vsize[1]/2)

#print data.shape

def positionChanged(evt):
    global data
    #pos = evt[0]  ## using signal proxy turns original arguments into a tuple
#    if p1.sceneBoundingRect().contains(pos):
#        mousePoint = vb.mapSceneToView(pos)
#        index = int(mousePoint.x())
#        if index > 0 and index < len(data1):
#            label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
#        vLine.setPos(mousePoint.x())
    #hLine.setPos(vLine.getPos()[1])
    p.param("Infos","x").setValue(vLine.getPos()[0])         
    xcurve.setData(data[...,round(hLine.getPos()[1])])
    ycurve.setData(data[round(vLine.getPos()[0])])
    
def positionChanged2(evt):   
    positionChanged(evt)
        
proxy = pg.SignalProxy(vLine.sigPositionChanged, rateLimit=60, slot=positionChanged)
proxy2 = pg.SignalProxy(hLine.sigPositionChanged, rateLimit=60, slot=positionChanged2)



##############################################################################
##timing

xcurve2=xslice.plot()
ycurve2=yslice.plot()
ycurve2.rotate(-90)


font=QtGui.QFont('Sans-Serif', 27, QtGui.QFont.Light)
#p.param("Infos","width").setValue(1)
#p.param("Infos","width").setFont(font)


layout = pg.LayoutWidget()
dn.addWidget(layout)

wlabel= QtGui.QLabel(u"width[µm]")
layout.addWidget(wlabel, row=0, col=0)
ww = pg.SpinBox()
layout.addWidget(ww, row=1,col=0)
hlabel= QtGui.QLabel(u"height[µm]")
layout.addWidget(hlabel, row=2, col=0)
wh = pg.SpinBox()
layout.addWidget(wh, row=3, col=0)

ww.setFont(font)
ww.setFixedSize(200,90)

wh.setFont(font)
wh.setFixedSize(200,90)
#ob=p.param("Infos","width")
#print [method for method in dir(ob) if callable(getattr(ob, method))]
#print [method for method in dir(ob)]
#print ob
#print ob.widget

xi=np.arange(data.shape[0])
yi=np.arange(data.shape[1])
import math

from misc import *
opt=lambda x: p.param("Options").param(x).value()

wsd=[]
wsd2=[]
def pupdate():    
    global data,rdata,xi,yi,wwidth,p
    ddata={}
    ret, frame = cap.read()
    if not ret or np.isnan(np.min(frame)):
        imv.setImage(rdata)    
        return    
    #image    
    data=frame[...,...,1].transpose();
    imv.setImage(data)    
    #maxmium
    maxpos=list(np.unravel_index(np.argmax(data),data.shape))
    maxv=np.amax(data)
    
#    xsum=np.sum(data,axis=1,dtype=np.float32)    
#    xsum=xsum/np.sum(xsum)    
#    maxpos[0]=np.sum(np.multiply(xi,xsum))
#    
#    xsum=np.sum(data,axis=0,dtype=np.float32)    
#    xsum=xsum/np.sum(xsum)    
#    maxpos[1]=np.sum(np.multiply(yi,xsum))    
    
    if opt("autocross"):    
        vLine.setPos(maxpos[0])
        hLine.setPos(maxpos[1])        
    #fit
    xp,pcov=fit(xi,data[...,round(hLine.getPos()[1])],(maxv,maxpos[0],50,10))  
    yp,pcov=fit(yi,data[round(vLine.getPos()[0])],(maxv,maxpos[1],50,10))  
    perr = np.sqrt(np.diag(pcov))
      
    ddata["perr"]=perr
    
    xcurve2.setData(fitFunc(xi, xp[0], xp[1], xp[2], xp[3]))
    ycurve2.setData(fitFunc(yi, yp[0], yp[1], yp[2], yp[3]))
    
    if opt('Camera Type')=='Color Camera':
        pixelsize=3.6
    else:
        pixelsize=5.2
   
    width=xp[2]*2 * math.sqrt(2)*pixelsize/10**3
    height=yp[2]*2 * math.sqrt(2)*pixelsize/10**3
    
    #debug
    ddata["x"]={"width":width,"height":height,"xp":xp, "arr":frame.shape,"d1":frame[1,1,1],"data.shape":data.shape,"xxx":np.argmax(data),"maxpos":maxpos,"max":maxv}
    #ddata["mp"]=np.sum(np.multiply(xi,xsum))
    
    positionChanged(None)
    ww.setValue(abs(width))
    wh.setValue(abs(height))
    
    smax=opt("maxSize")
    smin=opt("minSize")
    width=constrain(abs(width),smin,smax)
    height=constrain(abs(width),smin,smax)    
        
    wsd.append(width)
    cutdown(wsd,opt("timesize"))
    wsd2.append(height)
    cutdown(wsd2,opt("timesize"))   
    
    ptime.setLabel('bottom', 'Time', units='s')
    ptime.disableAutoRange(pg.ViewBox.YAxis)
    ptime.setYRange(min(wsd), max(wsd))    
    ptime.showGrid(True,True)
    ddata["lims"]=(min(wsd), max(wsd))    
    ctime.setData(np.arange(len(wsd)), wsd)
    ctime2.setData(np.arange(len(wsd2)),wsd2)
    tree.setData(ddata)

timer = QtCore.QTimer()
timer.timeout.connect(pupdate)
timer.start(50)

def cutdown(a,size):
    while np.size(a)>size:
        a.pop(0)




####fit ###################################
from scipy.optimize import curve_fit
def fitFunc(x, a, x0, d,c):
    return a*np.exp(-((x-x0)**2)/(d**2))+c

def fit(xs,ys,p0):
    global fitFunc
    fitParams, fitCovariances = curve_fit(fitFunc, xs , ys,p0)
    #print fitParams
    #print fitCovariances
    return (fitParams, fitCovariances)
### save settings

import os
programname = os.path.basename(__file__)    
programbase, ext = os.path.splitext(programname)
settings = QtCore.QSettings("company", programbase) 
#from QtCore import QSettings
settings= QtCore.QSettings(os.path.dirname(os.path.realpath(__file__)) + "\\" + "   settings.ini",  QtCore.QSettings.IniFormat)


guisave(win, settings)


#settings.setValue("x",1)

print settings.value("x").toInt();
settings.sync()


win.show()
#app.exec_()
import sys
sys.exit(app.exec_())

### Start Qt event loop unless running in interactive mode or using pyside.
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()
