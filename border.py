import cv2 as cv
import numpy as np
import preprocessing as prep
import util as util

def findDefects(contours, drawDefects, img):
	cnt = contours[0]
	hull = cv.convexHull(cnt, returnPoints = False)
	defects = cv.convexityDefects(cnt, hull)
	if not drawDefects:
		return defects
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		cv.line(img,start,end,[0,255,0],2)
		cv.circle(img,far,5,[0,0,255],-1)
	return (defects, img)

def compareContours(contour1, contour2):
	ret = cv.matchShapes(contour1, contour2, 1, 0.0)
	return ret

def getFittedEllipse(contour):
	ellipse = cv.fitEllipse(contour)
	return ellipse

def getEquivalentCircle(contour):
	area = cv.contourArea(contour)
	radius = np.sqrt(area/np.pi)
	M = cv.moments(contour)
	x = int(M['m10'] / M['m00'])
	y = int(M['m01'] / M['m00'])

	return (x, y, radius)

def getArrayOfRadiusMelanoma(contour):
	contourTemp = util.findLargestContour(contour) # Find largest contour
	x, y = getCenterOfCircle(contourTemp) # Get center of circle
	arrOfRadius = []
	for i in range(0, len(contourTemp)):
		arrOfRadius.append(np.sqrt(np.power(contourTemp[i][0][0] - x, 2) + np.power(contourTemp[i][0][1] - y, 2)))

	return arrOfRadius

def getMelanomaWithoutCircle(out, contours):
	blankImageHeight, blankImageWidth = out.shape
	blankImage = np.zeros((blankImageHeight, blankImageWidth, 3), np.uint8)

	# Create a circle contour
	contourNew = util.findLargestContour(contours)
	x, y, radius = getEquivalentCircle(contourNew)
	# cv.circle(img, (x, y), int(radius), (0, 255, 0), 2)
	cv.circle(blankImage, (x, y), int(radius), (255, 255, 255), 2)
	blankImageBW = cv.cvtColor(blankImage, cv.COLOR_BGR2GRAY)
	imgBlankImage, contourBlankImage, _ = cv.findContours(blankImageBW, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	contourBlankImage, imgBlankImage = prep.removeHoles(contourBlankImage, imgBlankImage)

	# Prepare melanoma contour
	imgFinal, contourFinal, _ = cv.findContours(out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	contourFinal, imgFinal = prep.removeHoles(contourFinal, imgFinal)
	largestFinalContour = util.findLargestContour(contourFinal)

	# Insert circle into melanoma
	finalBlankImageHeight, finalBlankImageWidth = imgFinal.shape # Make a new blank image
	finalBlankImage = np.zeros((blankImageHeight, blankImageWidth, 3), np.uint8)
	finalBlankImage = cv.cvtColor(finalBlankImage, cv.COLOR_BGR2GRAY)
	finalBlankImage = cv.drawContours(finalBlankImage, [largestFinalContour], 0, 255) # Draw melanoma contour
	finalBlankImage, finalBlankContour, _ = cv.findContours(finalBlankImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Find contour
	finalBlankContour, finalBlankImage = prep.removeHoles(finalBlankContour, finalBlankImage) # Fill contour
	cv.fillPoly(finalBlankImage, pts = [util.findLargestContour(contourBlankImage)], color = (0, 0, 0)) # Fill with circle

	return (finalBlankImage, contourBlankImage)

def getMelanomaWithoutCircleSurface(finalBlankImage, contourBlankImage):
	s = np.count_nonzero(finalBlankImage)/3
	return s
