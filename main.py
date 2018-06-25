import cv2 as cv
import numpy as np
import preprocessing as prep
import border as border
import util as util

img = cv.imread('images/melanoma.jpg') # Reading image
imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Converting to BW
_, thresh = cv.threshold(imggray, 127, 255, cv.THRESH_BINARY_INV) # Getting threshold
img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

# ================
# Get rid of holes
#
# There are some holes in the contour so this gets rid of them
# ================
_, thresh = prep.removeHoles(contours, thresh)

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
blankImageHeight, blankImageWidth = out.shape
blankImage = np.zeros((blankImageHeight, blankImageWidth, 3), np.uint8)

# Draw ellipse on blank and original image
contourNew = util.findLargestContour(contours)
ellipse = border.getFittedEllipse(contourNew)
cv.ellipse(img, ellipse, (0, 255, 0), 2)
cv.ellipse(blankImage, ellipse, (255, 255, 255), 2)
blankImageBW = cv.cvtColor(blankImage, cv.COLOR_BGR2GRAY)
imgBlankImage, contourBlankImage, _ = cv.findContours(blankImageBW, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contourBlankImage, imgBlankImage = prep.removeHoles(contourBlankImage, imgBlankImage)
imgFinal, contourFinal, _ = cv.findContours(out, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(border.compareContours(util.findLargestContour(contourFinal), contourBlankImage[0]))

# cv.imshow('Image', out) # Show result
# cv.imshow('Blank image', imgBlankImage)
cv.waitKey()
cv.destroyAllWindows()
