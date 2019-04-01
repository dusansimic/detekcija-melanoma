#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import util as util
import preprocessing as prep
import border as border
import diameter as diameter
import newColor as color
import asymmetry as asymmetry
from statistics import mean

def analyze(paramArr):
	# Read image path, filename and output file from params
	imagePath, fileName, outputFile = paramArr
	#print(imagePath)
	proportions = 0
	# Read the image first
	img = cv.imread(imagePath) # Reading image
	hsvimg = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	_, contours = util.getContourContrast(img) # Method for getting threshold and contours
	contour = util.findLargestContour(contours)
	threshShapeHeight, threshSHapeWidth, _ = img.shape
	thresh = np.zeros((threshShapeHeight, threshSHapeWidth, 1), dtype=np.uint8)
	thresh = cv.drawContours(thresh, [contour], 0, 255)
	([contour], thresh) = prep.fillEmpty([contour], thresh)

	# ================
	# Get rid of holestours
	#
	# There are some holes in the contour so this gets rid of them
	# ================
	closing = prep.removeHoles(thresh)

	# =====================
	# Get rid of noise dots
	#
	# This gets rid of noise dots that are around the contour
	# =====================
	out = prep.removeNoise(closing)

	# =================
	# B Rule
	#
	# Border rule implementation
	# =================
	finalBlankImage, contourBlankImage = border.getMelanomaWithoutCircle(out, thresh, contours)
	# for cont in contourBlankImage:
	# 	print(len(cont))
	# cv.imshow('Final blank image', finalBlankImage)
	# cv.waitKey()
	# cv.destroyAllWindows()
	# exit()


	sCnt = border.getMelanomaWithoutCircleSurface(finalBlankImage, contourBlankImage)
	borderDeviation = (sCnt*2)/cv.contourArea(util.findLargestContour(contourBlankImage))

	# =============
	# D Rule
	#
	# If diameter of lesion is bigger than 6mm
	# =============
	calculatedDiameter = diameter.getMinEnclosingCircleRadius(util.findLargestContour(contours)) * 2
	# realDiameter = diameter / proportions
	realDiameter = 0

	# =============
	# C Rule
	#
	# Color detecion
	# =============
	# Prepare melanoma contour
	stddevs, means = color.getColorDeviation(img, out)
	hstddevs, sstddevs, vstddevs = stddevs
	hmeans, smeans, vmeans = means

	# =============
	# A Rule
	#
	# Asymmetry rule
	# =============
	asymmetryResult = min([res for _, res in asymmetry.getAsymmetryRotationResults(thresh).items()])
	# asymmetryResult = asymmetry.getAsymmetryRotationResults(thresh)
	# meanAsymmetryResult = mean([res for _, res in asymmetryResult.items()]) * 100
	# asymmetryDeviation = asymmetry.getNewXOR(img)

	csvLine = str(fileName) + ',' + str(asymmetryResult) + ',' + str(borderDeviation) + ',' + str(hstddevs) + ',' + str(hmeans) + ',' + str(sstddevs) + ',' + str(smeans) + ',' + str(vstddevs) + ',' + str(vmeans) + ',' + str(realDiameter) + '\n'
	file = open(outputFile, 'a')
	file.write(csvLine)
	file.close()
