import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import math
import numpy as np


class animateClass:
    def __init__(self, egoPosition, car_position_pred, obstacleNum, obstaclePosition, obst_position_pred):
        self.obstacle_y_pred = None
        self.obstacle_x_pred = None
        self.plot_xaxis_limits = [0, 0]
        self.plot_yaxis_limits = [0, 0]
        self.ax = None
        self.fig = None
        self.egoPosition = egoPosition
        self.egoPositionPred = car_position_pred
        self.obstacleNum = obstacleNum
        self.obstPosition = obstaclePosition
        self.obstPositionPred = obst_position_pred
        self.frame_num = 0
        self.frame_interval = 0
        self.anim = None
        self.prediction_horizon = 0

        self.ego_x = []
        self.ego_y = []
        self.ego_x_pred = []
        self.ego_y_pred = []
        self.obstacle_x = []
        self.obstacle_y = []

    def open_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

    # Animation settings
    def animate(self, frame):
        if frame == self.frame_num:
            print(f'{frame} == {self.frame_num}; closing!')
            plt.close(self.fig)
        else:
            # print(f'frame: {frame}')  # Debug: May be useful to stop
            self.ego_x_pred = []
            self.ego_y_pred = []
            self.obstacle_x_pred = []
            self.obstacle_y_pred = []

            for i in range(0, frame):
                self.ego_x.append(self.egoPosition[i][0])
                self.ego_y.append(self.egoPosition[i][1])

            # For EGO vehicle Prediction Visualization
            if (frame - self.prediction_horizon) > 0:
                for j in range((frame - self.prediction_horizon), frame):
                    self.ego_x_pred.append(self.egoPositionPred[j][0])
                    self.ego_y_pred.append(self.egoPositionPred[j][1])

            # For Obstacle Prediction Visualization
            if (frame - self.prediction_horizon) > 0:
                for j in range((frame - self.prediction_horizon), frame):
                    self.obstacle_x_pred.append(self.obstPositionPred[j][0])
                    self.obstacle_y_pred.append(self.obstPositionPred[j][1])

            for i in range(0, frame):
                self.obstacle_x.append(self.obstPosition[i][0])
                self.obstacle_y.append(self.obstPosition[i][1])

            self.ax.clear()
            # self.ax.plot(self.ego_x, self.ego_y, 'gs')
            self.ax.plot(self.ego_x, self.ego_y, 'g')
            # self.ax.plot(self.egoPosition[frame-1][0], self.egoPosition[frame-1][1], 'gs')

            y_del = self.egoPosition[frame][1] - self.egoPosition[frame - 1][1]
            x_del = self.egoPosition[frame][0] - self.egoPosition[frame - 1][0]
            org_angle = math.degrees(np.arctan2(y_del, x_del))

            wid = 2
            hei = 6
            l = (wid / 2)
            # b = (wid/2)*math.cos(90 - org_angle)
            x_ = self.egoPosition[frame - 1][0] + (l * math.sin(org_angle))
            y_ = self.egoPosition[frame - 1][1] - (l * math.cos(org_angle))
            # print(self.egoPosition[frame - 1][0], self.egoPosition[frame - 1][1])
            # print(x_, y_)
            self.ax.add_patch(Rectangle((x_, y_), wid, hei, angle=(180 - org_angle), color='g'))
            self.ax.plot(self.ego_x_pred, self.ego_y_pred, 'b*')

            self.ax.plot(self.obstacle_x, self.obstacle_y, 'rs')
            self.ax.plot(self.obstacle_x, self.obstacle_y, 'r')
            self.ax.plot(self.obstacle_x_pred, self.obstacle_y_pred, 'b+')
            self.ax.set_xlim(self.plot_xaxis_limits)
            self.ax.set_ylim(self.plot_yaxis_limits)

    def animate_function(self):
        self.open_figure()
        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=self.frame_interval,
                                            frames=self.frame_num + 1, repeat=False)
        plt.show()
