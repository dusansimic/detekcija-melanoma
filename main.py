import cv2 as cv
import numpy as np
import preprocessing as prep
import convexityDefects as convDef

img = cv.imread('images/melanoma.jpg') # Reading image
imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Converting to BW
ret, thresh = cv.threshold(imggray, 127, 255, cv.THRESH_BINARY_INV) # Getting threshold
img2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # Getting contour

# ================
# Get rid of holes
#
# There are some holes in the contour so this gets rid of them
# ================
contours, thresh = prep.removeHoles(contours, thresh)

# =====================
# Get rid of noise dots
#
# This gets rid of noise dots that are around the contour
# =====================
se1 = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
se2 = cv.getStructuringElement(cv.MORPH_RECT, (2,2))
mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, se1)
mask = cv.morphologyEx(mask, cv.MORPH_OPEN, se2)

mask = np.dstack([mask, mask, mask]) / 255
out = img * mask


# =================
# Convexity Defects
#
# Find convexity defects
# =================
defects, img = convDef.findDefects(contours, True, img)


cv.imshow('Image', img2) # Show result
cv.imshow('Output', out)
cv.waitKey()
cv.destroyAllWindows()
