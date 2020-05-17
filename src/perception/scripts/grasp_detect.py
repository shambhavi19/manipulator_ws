#!/usr/bin/env python

import rospy 
import sys
import cv2
from perception.msg import array
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np 
import ros_numpy
import message_filters

import matplotlib.pyplot as plt

import argparse

# Helper Script to take BGR and Depth Images abd convert them to RGD Image


def image_callback(ros_rgb, ros_depth):
    bridge = CvBridge()
    try:
        rgb = bridge.imgmsg_to_cv2(ros_rgb, "bgr8")
        depth = bridge.imgmsg_to_cv2(ros_depth,"passthrough")
    except CvBridgeError, e:
        print e


    kernel = np.ones((2,2),np.uint8)


    cv2.imwrite('/home/avitra/manipulator_ws/src/perception/scripts/color_'+path+'.png',rgb)
    cv2.imwrite('/home/avitra/manipulator_ws/src/perception/scripts/depth_'+path+'.png',depth)
    color = cv2.imread('/home/avitra/manipulator_ws/src/perception/scripts/color_'+path+'.png')
    depth = cv2.imread('/home/avitra/manipulator_ws/src/perception/scripts/depth_'+path+'.png',0)
    color[:,:,0] = depth
    print("writing")
    cv2.imwrite('/home/avitra/manipulator_ws/src/perception/scripts/rgd_'+path+'.png',color)
    
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Data prep')
    parser.add_argument('--path', default='0')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    print("writing")
    args = parse_args()
    path = args.path
    print path
    rospy.init_node('rgb')

    rgb_sub = message_filters.Subscriber('/camera/color/image_rect_color', Image)
    depth_sub = message_filters.Subscriber('/camera/aligned_depth_to_color/image_raw', Image)

    ts = message_filters.TimeSynchronizer([rgb_sub, depth_sub], 10)
    ts.registerCallback(image_callback)
    rospy.spin()

