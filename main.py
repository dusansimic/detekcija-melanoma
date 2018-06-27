#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import preprocessing as prep
import border as border
import diameter as diameter
import color as color
import asymmetry as asymmetry
import sys

proportions = 0
imagePath = ''

for i in range(1, len(sys.argv)):
	if (sys.argv[i] == '--proportions'):
		i+=1
		proportions = float(sys.argv[i])
	if (sys.argv[i] == '--image-path'):
		i+=1
		imagePath = sys.argv[i]

if imagePath == '':
	print('You need to enter an image path')
	exit()

img = cv.imread(imagePath) # Reading image
imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Converting to BW
_, thresh = cv.threshold(imggray, 127, 255, cv.THRESH_BINARY_INV) # Getting threshold
img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

# ================
# Get rid of holestours
#
# There are some holes in the contour so this gets rid of them
# ================
_, thresh = prep.removeHoles(contours, thresh)

# =====================
# Get rid of noise dots
#
# This gets rid of noise dots that are around the contour
# =====================
out = prep.removeNoiseDots(img, thresh)

# =================
# B Rule
#
# Border rule implementation
# =================
finalBlankImage, contourBlankImage = border.getMelanomaWithoutCircle(out, contours)

sCnt = border.getMelanomaWithoutCircleSurface(finalBlankImage, contourBlankImage)
print((sCnt*2)/cv.contourArea(util.findLargestContour(contourBlankImage)))

# =============
# D Rule
#
# If diameter of lesion is bigger than 6mm
# =============
diameter = diameter.getMinEnclosingCircleRadius(util.findLargestContour(contours)) * 2
print(diameter * proportions)

# =============
# C Rule
#
# Color detecion
# =============
# Prepare melanoma contour
stddevs, tempImg = color.getColorDeviation(img, out)
print(stddevs)

# =============
# A Rule
#
# Asymmetry rule
# =============
deviation = asymmetry.getXOR(out)
print(deviation)

# cv.namedWindow('Image', cv.WINDOW_NORMAL)
# cv.imshow('Image', tempImg) # Show result
# cv.resizeWindow('Image', 600,	600)
# cv.waitKey()
# cv.destroyAllWindows()
