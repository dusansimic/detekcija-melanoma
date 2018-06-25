import cv2 as cv
import numpy as np

def removeHoles(contours, thresh):
	for cnt in contours:
		cv.drawContours(thresh, [cnt], 0, 255, -1)
	return (contours, thresh)

def removeNoiseDots(thresh):
	se1 = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
	se2 = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
	mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, se1)
	mask = cv.morphologyEx(mask, cv.MORPH_OPEN, se2)

	mask = np.dstack([mask, mask, mask]) / 255
	out = img * mask

	return out
