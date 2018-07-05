import cv2 as cv
import numpy as np

def removeHoles(thresh):
	kernel = np.ones((1,1), np.uint8)
	closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
	return closing

def fillEmpty(contours, thresh):
	for cnt in contours:
		cv.drawContours(thresh, [cnt], 0, 255, -1)
	return (contours, thresh)

def removeNoise(thresh):
	kernel = np.ones((1,1), np.uint8)
	opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
	return opening

def colorInBlack(contours, thresh):
	for cnt in contours:
		cv.drawContours(thresh, [cnt], 0, 0, -1)
	return (contours, thresh)

def removeNoiseDots(img, thresh):
	se1 = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
	se2 = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
	mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, se1)
	mask = cv.morphologyEx(mask, cv.MORPH_OPEN, se2)

	mask = np.dstack([mask, mask, mask]) / 255
	out = img * mask
	# Make it only black and white, not gray
	out = out.astype(np.uint8)
	outgray = cv.cvtColor(out, cv.COLOR_BGR2GRAY)
	for i in range(0, len(outgray)-1):
		for j in range(0, len(outgray[i])-1):
			if outgray[i][j] != 0: outgray[i][j] = 255

	return outgray
