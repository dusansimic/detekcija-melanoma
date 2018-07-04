import cv2 as cv
import numpy as np
import preprocessing as prep
import util as util

def getXOR(out):
	imgFinal, contourFinal, _ = cv.findContours(out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	imgFinal = prep.removeHoles(imgFinal)
	largestFinalContour = util.findLargestContour(contourFinal)
	maskHeight, maskWidth = out.shape
	mask = np.zeros((maskHeight, maskWidth, 3), np.uint8)
	mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
	mask = cv.drawContours(mask, [largestFinalContour], -1, (255), 1)
	mask = np.dstack((mask, mask, mask))
	cv.fillPoly(mask, pts = [largestFinalContour], color = (255, 255, 255)) # Fill with circle

	maskCenter = tuple(np.array(mask.shape[1::-1]) / 2)
	rotationMatrix = cv.getRotationMatrix2D(maskCenter, 180, 1.0)
	maskRotated = cv.warpAffine(mask, rotationMatrix, mask.shape[1::-1], flags = cv.INTER_LINEAR)

	maskXORed = cv.bitwise_xor(mask, maskRotated)

	deviation = (np.count_nonzero(maskXORed)/np.count_nonzero(mask))*100

	return deviation

def getNewXOR(img):
	thresh, contours = util.getContourHSV(img)
	largestContour = util.findLargestContour(contours)
	maskHeight, maskWidth, _ = img.shape

	mask = np.zeros((maskHeight, maskWidth, 3), np.uint8)
	mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
	mask = cv.drawContours(mask, [largestContour], -1, (255), 1)
	mask = np.dstack((mask, mask, mask))
	cv.fillPoly(mask, pts = [largestContour], color = (255, 255, 255)) # Fill with circle

	maskCenter = tuple(np.array(mask.shape[1::-1])/2)
	rotationMatrix = cv.getRotationMatrix2D(maskCenter, 180, 1.0)
	maskRotated = cv.warpAffine(mask, rotationMatrix, mask.shape[1::-1], flags = cv.INTER_LINEAR)

	maskXORed = cv.bitwise_xor(mask, maskRotated)

	devitaion = (np.count_nonzero(maskXORed)/np.count_nonzero(mask))*100

	return devitaion
