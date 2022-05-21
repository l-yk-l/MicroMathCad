import time
import math

import numpy as np
from collections import deque


class Sinusoid(object):
    def __init__(self, plt, ax, k=1.0, n_points=500):
        self.n_points = n_points
        self.e = 10 / n_points
        self.k = k
        npx = np.linspace(0, 0, 1)
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(np.sin(self.k * np.pi * npx), maxlen=n_points)
        self.x_history = [self.x[0]]
        self.y_history = [self.y[0]]
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.color = None
        self.plt.xlim([-0.6, 10.6])
        self.plt.ylim([-1.2, 1.2])

    def update(self, dy):
        last = self.x[-1]
        if not self.isPaused:
            self.x.append(last + self.e)  # update data
            self.y.append(dy)
            self.x_history.append(last + self.e)
            self.y_history.append(dy)

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)

            # лимиты осей (с какой по какую точку оси отображать плот)
            if last < 10:
                self.plt.xlim([-0.6, 10.6])
            else:
                self.plt.xlim([last - 10.6, last + 0.6])
            self.plt.ylim([-1.2, 1.2])
            self.ax.autoscale_view(True, True, True)
            return self.line, self.ax

    def data_gen(self):
        while True:
            yield np.sin(self.k * np.pi * self.x[-1])

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)


class Victim(object):
    def __init__(self, plt, ax, start_x, start_y, direction, speed, max_angle_of_rotation, n_points=500):
        self.n_points = n_points
        self.e = 10 / n_points
        npx = np.array([start_x])
        npy = np.array([start_y])
        self.direction = direction
        self.speed = speed
        self.max_angle_of_rotation = max_angle_of_rotation
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(npy, maxlen=n_points)
        self.x_history = [self.x[0]]
        self.y_history = [self.y[0]]
        self.hunters = []
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.color = None
        # Лимиты следует подобрать позже по стартовой точке
        self.plt.xlim([-10, 10])
        self.plt.ylim([-10, 10])

    def update(self, dy):
        # A(x1, y1)
        # a - угол в градусах
        # d - расстояние
        # B = (x1 + d*cos(a), y1 + d*sin(a))
        if not self.isPaused:
            for i in range(math.floor(self.speed * 10)):
                last_x = self.x[-1]
                last_y = self.y[-1]
                self.x.append(last_x + 0.1 * np.cos(np.radians(self.direction)))
                self.y.append(last_y + 0.1 * np.sin(np.radians(self.direction)))
                self.x_history.append(self.x[-1])
                self.y_history.append(self.y[-1])

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)

            # лимиты осей (с какой по какую точку оси отображать плот)
            # if last < 10:
            #     self.plt.xlim([-0.6, 10.6])
            # else:
            #     self.plt.xlim([last - 10.6, last + 0.6])
            # self.plt.ylim([-1.2, 1.2])
            self.ax.autoscale_view(True, True, True)

            time.sleep(0.05)

            return self.line, self.ax

    def data_gen(self):
        while True:
            yield self.y[-1]

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)

    def add_hunter(self, hunter):
        self.hunters.append(hunter)


class Hunter(object):
    def __init__(self, plt, ax, start_x, start_y, direction, speed, max_angle_of_rotation, n_points=500):
        self.n_points = n_points
        self.e = 10 / n_points
        npx = np.array([start_x])
        npy = np.array([start_y])
        self.direction = direction
        self.speed = speed
        self.max_angle_of_rotation = max_angle_of_rotation
        self.x = deque(npx, maxlen=n_points)
        self.y = deque(npy, maxlen=n_points)
        self.x_history = [self.x[0]]
        self.y_history = [self.y[0]]
        self.victim = None
        self.isPaused = True
        self.ax = ax
        self.plt = plt
        [self.line] = self.ax.step(self.x, self.y)
        self.color = None
        # Лимиты следует подобрать позже по стартовой точке
        self.plt.xlim([-10, 10])
        self.plt.ylim([-10, 10])

    def update(self, dy):
        # A(x1, y1)
        # a - угол в градусах
        # d - расстояние
        # B = (x1 + d*cos(a), y1 + d*sin(a))
        last_x = self.x[-1]
        last_y = self.y[-1]
        if not self.isPaused:
            for i in range(math.floor(self.speed * 10)):
                last_x = self.x[-1]
                last_y = self.y[-1]
                self.x.append(last_x + 0.1 * np.cos(np.radians(self.direction)))
                self.y.append(last_y + 0.1 * np.sin(np.radians(self.direction)))
                self.x_history.append(self.x[-1])
                self.y_history.append(self.y[-1])

            self.line.set_xdata(self.x)  # update plot data
            self.line.set_ydata(self.y)

            # лимиты осей (с какой по какую точку оси отображать плот)
            # if last < 10:
            #     self.plt.xlim([-0.6, 10.6])
            # else:
            #     self.plt.xlim([last - 10.6, last + 0.6])
            # self.plt.ylim([-1.2, 1.2])
            self.ax.autoscale_view(True, True, True)
            return self.line, self.ax

    def data_gen(self):
        while True:
            yield self.y[-1]

    def set_color(self, color):
        self.color = color
        self.line.set_color(self.color)

    def set_victim(self, victim):
        self.victim = victim
