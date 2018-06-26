import cv2 as cv
import numpy as np

def getColorDeviation(image):
	# colorArr = image[np.nonzero(image)]
	means, stddevs = cv.meanStdDev(image)
	# average = np.mean(colorArr)
	# colorSum = 0
	# for i in range(0, len(colorArr)):
	# 	colorArr += np.power(colorArr[i] - average, 2)
	# sigma = np.sqrt(colorSum / len(colorArr))

	return (means, stddevs)
