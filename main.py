#!/usr/bin/env python3
import cv2 as cv
import util as util
import preprocessing as prep
import border as border
import diameter as diameter
import color as color
import asymmetry as asymmetry

def analyze(paramArr):
	imagePath, fileName = paramArr
	proportions = 0
	img = cv.imread(imagePath) # Reading image
	thresh, contours = util.getContourHSV(img) # Method for getting threshold and contours

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
	out = prep.removeNoise(thresh)

	# =================
	# B Rule
	#
	# Border rule implementation
	# =================
	finalBlankImage, contourBlankImage = border.getMelanomaWithoutCircle(out, contours)

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
	stddevs, means, tempImg = color.getColorDeviation(img, out)
	hstddevs, sstddevs, vstddevs = stddevs
	hmeans, smeans, vmeans = means

	# =============
	# A Rule
	#
	# Asymmetry rule
	# =============
	asymmetryDeviation = asymmetry.getNewXOR(img)

	csvLine = str(fileName) + ',' + str(asymmetryDeviation) + ',' + str(borderDeviation) + ',' + str(hstddevs) + ',' + str(hmeans) + ',' + str(sstddevs) + ',' + str(smeans) + ',' + str(vstddevs) + ',' + str(vmeans) + ',' + str(realDiameter) + '\n'
	file = open('results.csv', 'a')
	file.write(csvLine)
	file.close()
	print(imagePath)
