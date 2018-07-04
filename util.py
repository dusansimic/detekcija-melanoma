import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

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

def getContourHSV(img):
	imghsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) # Convert to HSV
	imghsv2means = imghsv.reshape((-1, 3))
	imghsv2means = np.float32(imghsv2means) # Prepare image for kmeans()
	coords = cv.KMEANS_RANDOM_CENTERS
	criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	_, label, center = cv.kmeans(imghsv2means, 2, None, criteria, 10, coords) # Do kmeans
	center = np.uint8(center)
	res = center[label.flatten()]
	imghsv2means = res.reshape((img.shape)) # Convert to usable image with 2 colors
	imggray = cv.cvtColor(imghsv2means, cv.COLOR_BGR2GRAY) # Convert to BW
	blur = cv.GaussianBlur(imggray, (5,5), 0)
	_, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) # Getting threshold
	img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

	return (thresh, contours)
