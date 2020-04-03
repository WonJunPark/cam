import cv2
import numpy as np

video_path = 'redVelvet.mp4'
cap = cv2.VideoCapture(video_path)

# 영상을 저장하기 위한 셋팅, 폰으로 확인
output_size = (400, 700) # 가로,세로

# initialize writing video
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)


if not cap.isOpened():
    exit()

# 첫번째 프레임을 가져옴
ret, img = cap.read()

# CSRT tracker 초기화 / 정확도와 속도 평균
tracker = cv2.TrackerCSRT_create()

cv2.namedWindow('Select Window')
cv2.imshow('Select Window',img)

# setting ROI
# ROI(Region of Interest) : 관심 영역 영상 처리
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# ROI로 tracker 셋팅
tracker.init(img, rect)

while True:
    ret, img = cap.read()

    if not ret:
        exit()

    # ROI 연속으로 따라가기
    success, box = tracker.update(img)

    left, top, w, h = [int(v) for v in box]

    # 중심 구하기
    center_x = left + w / 2
    center_y = top + h / 2

    # output으로 내보낼 박스 구하기
    result_top = int(center_y - output_size[1] / 2)
    result_bottom = int(center_y + output_size[1] / 2)
    result_left = int(center_x - output_size[0] / 2)
    result_right = int(center_x + output_size[0] / 2)

    result_img = img[result_top:result_bottom, result_left:result_right].copy()

    out.write(result_img)

    cv2.rectangle(img, pt1=(left, top), pt2=(left+w, top+h), color=(255,255,255), thickness=3)

    cv2.imshow('result_img', result_img)
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break