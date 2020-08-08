import numpy as np
from math import *
from mayavi import mlab


radius = 75
length = 750


u = np.linspace(0, 2 * np.pi, 50)  # divide the circle into 50 equal parts
h = np.linspace(0, 1, 20)  # divide the height 1 into 20 parts
x = np.outer(radius*np.sin(u), np.ones(len(h)))  # x value repeated 20 times
y = np.outer(radius*np.cos(u), np.ones(len(h)))  # y value repeated 20 times
z = length*np.outer(np.ones(len(u)), h)  # x,y corresponding height

turns = 10
thickness = 6
theta = np.linspace(0,5*pi,100)

# radius = radius*1.05
# Zh = radius*np.cos(theta)
# Xh = radius*np.sin(theta)
# Yh = theta*(length/(turns*2*pi))

radius = radius*1.01
w = 0.5
t = np.arange(0, 100, 0.01)
Zh = radius*np.cos(w*t)
Xh = radius*np.sin(w*t)
Yh = np.loadtxt('z_position.csv', delimiter=',')


Y = np.column_stack((Yh-thickness/2, Yh+thickness/2)).T
X = np.column_stack((Xh, Xh)).T
Z = np.column_stack((Zh, Zh)).T

fig = mlab.figure(figure='Py Filament Winder', size=(900, 420))

CYLINDER_COLOR = (0,94,120)
STRAND_COLOR = (35,43,43)

tuple(map(lambda x: x/255, CYLINDER_COLOR))

filament = mlab.mesh(X, Y,Z ,color = tuple(map(lambda x: x/255, STRAND_COLOR)))
cylinder = mlab.mesh(x, z, y,color = tuple(map(lambda x: x/255, CYLINDER_COLOR)))
mlab.view(azimuth=0,distance=720)

fig.scene.scene_editor._tool_bar.setVisible(False)

mlab.show()