import cv2 as cv
import numpy as np

def findLargestContour(contours):
	largestContour = max(contours, key = cv.contourArea)
	return largestContour

def getCenterOfCircle(contour):
	M = cv.moments(contour)
	x = int(M['m10'] / M['m00'])
	y = int(M['m01'] / M['m00'])

	return (x, y)

def getThreshAndContour(img):
	imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Converting to BW
	blur = cv.GaussianBlur(imggray, (5,5), 0) # Blur image
	_, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) # Getting threshold
	img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

	return (thresh, contours)

def __increaseContrast(img, brightness, contrast):
	imgInceasedContrast = cv.addWeighted(img, 1.0 + contrast / 127, img, 0, brightness - contrast)
	return imgInceasedContrast

def getContourHSV(img):
	imgInceasedContrast = __increaseContrast(img, 64.0, 0.0)
	imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Convert to BW
	blur = cv.GaussianBlur(imggray, (5,5), 0)
	_, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) # Getting threshold
	img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

	return (thresh, contours)
