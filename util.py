import cv2 as cv

def findLargestContour(contours):
	largestContour = max(contours, key = cv.contourArea)
	return largestContour

def getCenterOfCircle(contour):
	M = cv.moments(contour)
	x = int(M['m10'] / M['m00'])
	y = int(M['m01'] / M['m00'])

	return (x, y)