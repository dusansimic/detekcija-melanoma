import cv2 as cv
import numpy as np
import preprocessing as prep
import border as border
import util as util

img = cv.imread('images/cut3.jpg') # Reading image
imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Converting to BW
_, thresh = cv.threshold(imggray, 127, 255, cv.THRESH_BINARY_INV) # Getting threshold
img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

# ================
# Get rid of holes
#
# There are some holes in the contour so this gets rid of them
# ================
contours, thresh = prep.removeHoles(contours, thresh)

# =====================
# Get rid of noise dotselli
#
# This gets rid of noise dots that are around the contour
# =====================
out = prep.removeNoiseDots(img, thresh)

# =================
# B Rule
#
# Border rule implementation
# =================

# Draw ellipse on original image
contourNew = util.findLargestContour(contours)
ellipse = border.getFittedEllipse(contourNew)
cv.ellipse(img, ellipse, (0, 255, 0), 2)

cv.imshow('Image', img) # Show result
cv.imshow('Output', out)
cv.waitKey()
cv.destroyAllWindows()
