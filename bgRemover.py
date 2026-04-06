import cv2
import numpy as np

cap = cv2.VideoCapture('/Users/dhiyajayadevan/Downloads/source_code/los_angeles.mp4')
backgroundObject = cv2.createBackgroundSubtractorMOG2( history = 100, detectShadows = False )

while True:
    ret, frame = cap.read()
    if not ret:
        break

#apply background object on each frame
    mask = backgroundObject.apply(frame)
    mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    real_part = cv2.bitwise_and(frame,frame,mask=mask)
    stacked = np.hstack((mask3,frame,real_part))
    cv2.imshow('All three',cv2.resize(stacked,None,fx=0.65,fy=0.65))

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()