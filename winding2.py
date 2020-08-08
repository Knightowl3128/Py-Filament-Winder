import numpy as np
from numpy import pi
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mayavi import mlab

class Winding:
    def __init__(self):

        self.alpha_i = np.deg2rad(45)
        self.radius = 75
        self.w = 0.5
        self.length = 750
        self.phi_dwell = 10*pi / 2
        self.turnaround_l = 225
        self.turnaround_r = 525
        self.thickness = 6
        self.initial_position = 0.3

        self.alpha = self.alpha_i
        self.dwell_angle = 0

        self.dwell_state = False
        self.angle_start = 0

        self.dz = 1

        self.total_time = 500

    def get_alpha(self,z,dz,t):
        if np.round(z, 2) == 0 or np.round(z, 2) == self.length or self.dwell_state:
            print('asdfasdfasdfasdf')
            if self.phi_dwell == 0:
                if np.round(z, 1) == 0:
                    alpha = pi / 2 - pi / 2000
                else:
                    alpha = pi / 2 + pi / 2000
                return alpha

            if not self.dwell_state:
                self.dwell_state = True
                self.angle_start = self.w * t
                return pi / 2

            if self.dwell_state and self.w * t - self.angle_start >= self.phi_dwell / 2:

                if np.round(z, 1) == 0:
                    alpha = pi / 2 - pi / 2000
                else:
                    alpha = pi / 2 + pi / 2000
                self.dwell_state = False
                self.angle_start = 0
                return alpha

            return pi / 2

        elif (0 <= z) and (z < self.turnaround_l):
            # print(z)
            h = self.turnaround_l
            k = pi / 2
            b = self.turnaround_l
            a = k - self.alpha_i

            if dz >= 0:

                alpha = -(a) * (1 - ((z - h) / b) ** 2) ** (.5) + k


                return alpha

            elif dz < 0:
                alpha = (a) * (1 - ((z - h) / (b)) ** 2) ** (.5) + k
                return alpha

        elif (self.turnaround_l < z) and (z < self.turnaround_r) > 0:
            if dz > 0:
                alpha = self.alpha_i
                return alpha
            else:
                alpha = pi - self.alpha_i
                return alpha

        elif (z >= self.turnaround_r) and (z < self.length):

            h = self.turnaround_r
            k = pi / 2
            b = self.length - self.turnaround_r
            a = k - self.alpha_i

            if dz > 0:
                alpha = -(a) * (1 - ((z - h) / b) ** 2) ** (.5) + k
                return alpha

            elif dz <= 0:
                alpha = (a) * (1 - ((z - h) / (b)) ** 2) ** (.5) + k
                return alpha

        else:
            return pi / 2

    def integrate(self):

        def model(z, t):
            alpha = self.get_alpha(z, self.dz, t)
            try:
                print(z, self.dz, np.rad2deg(alpha))
            except:
                print(z, self.dz, alpha)

            dzdt = self.radius * self.w / np.tan(alpha)
            self.dz = dzdt
            return dzdt

        y0 = self.initial_position

        # time points
        t = np.arange(0, self.total_time , 0.01)

        # solve ODE
        y = odeint(model, y0, t, hmax=0.01)

        np.savetxt('z_position.csv', y, delimiter=',')
        self.animate()
        # plt.plot(t, y)
        # plt.xlabel('time')
        # plt.ylabel('y(t)')
        # plt.show()

    def animate(self):
        u = np.linspace(0, 2 * np.pi, 50)  # divide the circle into 50 equal parts
        h = np.linspace(0, 1, 20)  # divide the height 1 into 20 parts
        x = np.outer(self.radius * np.sin(u), np.ones(len(h)))  # x value repeated 20 times
        y = np.outer(self.radius * np.cos(u), np.ones(len(h)))  # y value repeated 20 times
        z = self.length * np.outer(np.ones(len(u)), h)  # x,y corresponding height


        radius = self.radius * 1.01

        t = np.arange(0, self.total_time , 0.01)
        Zh = radius * np.cos(self.w * t)
        Xh = radius * np.sin(self.w * t)
        Yh = np.loadtxt('z_position.csv', delimiter=',')

        Y = np.column_stack((Yh - self.thickness / 2, Yh + self.thickness / 2)).T
        X = np.column_stack((Xh, Xh)).T
        Z = np.column_stack((Zh, Zh)).T

        fig = mlab.figure(figure='Py Filament Winder', size=(900, 420))

        CYLINDER_COLOR = (0, 94, 120)
        STRAND_COLOR = (35, 43, 43)

        tuple(map(lambda x: x / 255, CYLINDER_COLOR))

        filament = mlab.mesh(X, Y, Z, color=tuple(map(lambda x: x / 255, STRAND_COLOR)))
        cylinder = mlab.mesh(x, z, y, color=tuple(map(lambda x: x / 255, CYLINDER_COLOR)))

        deg = 0
        mlab.view(azimuth=0, distance=720)
        import time

        # while True:
        #     if deg == 360: deg = 0
        #     print(deg)
        #     mlab.view(azimuth=deg, distance=720)
        #     deg += 1
        #     time.sleep(1/60)
        #     fig.scene.render()
        #     # mlab.show()

        @mlab.animate(delay=10, ui=False)
        def anim():
            while 1:

                fig.scene.camera.azimuth(.1)
                fig.scene.render()
                yield

        a = anim()
        mlab.show()

if __name__ == '__main__':

    a = Winding()

    a.animate()