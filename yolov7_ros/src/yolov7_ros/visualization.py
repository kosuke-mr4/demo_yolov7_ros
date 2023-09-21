import sys
import random
import pathlib

import rospy

import numpy as np

# add yolov7 submodule to path
FILE_ABS_DIR = pathlib.Path(__file__).absolute().parent
YOLOV7_ROOT = (FILE_ABS_DIR / 'yolov7').as_posix()
if YOLOV7_ROOT not in sys.path:
    sys.path.append(YOLOV7_ROOT)

from utils.plots import plot_one_box

class Visualizer:
    def __init__(self, detector, line_thickness=1):
        self.model = detector.model
        self.__names = self.model.names
        self.__colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.__names]
        self.__line_thickness = line_thickness

    def draw_2d_bboxes(self, img, dets):
        WIDTH = 640
        HEIGHT = 480

        right_area = 1
        left_area = 1
        for det in dets:
            *xyxy, conf, cls = det
            label = f'{self.__names[int(cls)]} {conf:.2f}'
            # label person 0.94
            # print("label" , label , "cls" , cls)

            # only person
            if(int(cls) == 0):
                # [0.0, 368.0, 30.0, 479.0]
                # print(xyxy)
                x1 = xyxy[0]
                x2 = xyxy[2]
                y1 = xyxy[1]
                y2 = xyxy[3]
                
                if(x1 < WIDTH/2):
                    x2 = 320
                    right_area += (x2 - x1) * (y2 - y1)
                else:
                    left_area += (x2 - x1) * (y2 - y1)

                plot_one_box(xyxy, img, label=label, color=self.__colors[int(cls)],
                            line_thickness=self.__line_thickness)
        
        angular_velocity = 0
        if(left_area > right_area):
            angular_velocity = left_area / right_area / 10
        elif(left_area < right_area):
            angular_velocity = right_area / left_area / 10 * (-1)

        if (angular_velocity > 0.5): angular_velocity = 0.5
        elif (angular_velocity < -0.5): angular_velocity = -0.5
        print(angular_velocity)

        return angular_velocity

        # angular_velocity を publish
        # sankou : http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/Twist.html
