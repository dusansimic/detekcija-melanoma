import cv2 as cv
import numpy as np
import preprocessing as prep
import util as util

def getColorDeviation(img, out):
	imgFinal, contourFinal, _ = cv.findContours(out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	contourFinal, imgFinal = prep.removeHoles(contourFinal, imgFinal)
	largestFinalContour = util.findLargestContour(contourFinal)
	maskHeight, maskWidth = out.shape
	mask = np.zeros((maskHeight, maskWidth, 3), np.uint8)
	mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
	mask = cv.drawContours(mask, [largestFinalContour], -1, (255), 1)
	mask = np.dstack((mask, mask, mask))
	cv.fillPoly(mask, pts = [largestFinalContour], color = (1, 1, 1)) # Fill with circle
	tempImg = img * mask
	kernel = np.ones((5,5), np.uint8)
	tempImg = cv.erode(tempImg, kernel, iterations = 1)
	tempImgArr = tempImg[
		(tempImg[:,:,1] != 0) |
		(tempImg[:,:,0] != 0) |
		(tempImg[:,:,2] != 0)]

	stddevs = np.std(tempImgArr, axis=0)

	return (stddevs, tempImg)
