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

radius = radius*1.05
w = 0.5
t = np.arange(0, 100, 0.01)
Zh = radius*np.cos(w*t)
Xh = radius*np.sin(w*t)
Yh = np.loadtxt('z_position.csv', delimiter=',')


Y = np.column_stack((Yh-thickness/2, Yh+thickness/2)).T
X = np.column_stack((Xh, Xh)).T
Z = np.column_stack((Zh, Zh)).T


s = mlab.mesh(X, Y,Z ,color = (155/255,196/255,197/255))
t = mlab.mesh(x, z, y)


mlab.show()