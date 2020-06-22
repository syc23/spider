#!usr/bin/env python
#-*- coding:utf-8 -*-
import cv2 as cv

# # 2. 读取视频
# video = cv.VideoCapture("test.mp4")
#
# while 1:
#     ret, frame = video.read()
#     frame = cv.resize(frame, (300, 200))
#     cv.imshow("video", frame)
#     key = cv.waitKey(20)
#     if key == 27:  # esc==27
#         break
# video.release()  # 释放资源
# cv.destroyAllWindows()  # 关闭窗口

# 3. 读取摄像头
video = cv.VideoCapture(0)

while 1:
    ret, source = video.read()
    source = cv.resize(source, (400, 300))
    cv.imshow("source", source)
    # 色彩提取首先要把原画(bgr)面转换成hsv画面
    hsv = cv.cvtColor(source, cv.COLOR_BGR2HSV)
    cv.imshow('hsv', hsv)
    # 从hsv中提取到xxx颜色的轮廓
    mask = cv.inRange(hsv, (35, 43, 46), (77, 255, 255))
    cv.imshow("mask", mask)  # 得到的结果, 除了0就是1

    result = cv.bitwise_and(source, source, mask=mask)
    cv.imshow("result", result)

    key = cv.waitKey(10)
    if key == 27:
        break

video.release()
cv.destroyAllWindows()
