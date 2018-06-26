#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import preprocessing as prep
import border as border
import diameter as diameter
import color as color
import util as util
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
tempImgArr = tempImg[np.nonzero(tempImg)]
tempImgArr = tempImgArr[:int(len(tempImgArr)/3)*3]
# means, stddevs = color.getColorDeviation(tempImg)
colorArrR = []
colorArrG = []
colorArrB = []
for i in np.arange(0, len(tempImgArr), 3):
	colorArrB.append(tempImgArr[i])
	colorArrG.append(tempImgArr[i + 1])
	colorArrR.append(tempImgArr[i + 2])
meanR = np.mean(colorArrR)
meanG = np.mean(colorArrG)
meanB = np.mean(colorArrB)
colorSumR = 0
colorSumG = 0
colorSumB = 0
for i in range(0, len(colorArrR)):
	colorSumR += np.power(colorArrR[i] - meanR, 2)
	colorSumG += np.power(colorArrG[i] - meanG, 2)
	colorSumB += np.power(colorArrB[i] - meanB, 2)
sigmaR = np.sqrt(colorSumR/len(colorArrR))
sigmaB = np.sqrt(colorSumB/len(colorArrB))
sigmaG = np.sqrt(colorSumG/len(colorArrG))

print(sigmaR, sigmaG, sigmaB)

cv.namedWindow('Image', cv.WINDOW_NORMAL)
cv.imshow('Image', tempImg) # Show result
cv.resizeWindow('Image', 600,	600)
cv.waitKey()
cv.destroyAllWindows()
