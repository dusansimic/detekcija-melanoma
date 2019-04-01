import cv2 as cv
import numpy as np
import preprocessing as prep
import util as util
from matplotlib import pyplot as plt

def getColorDeviation(img, out):
	# Apply mask on the image
	res = cv.bitwise_and(img, img, mask = out)
	# Leave out black pixels (those which are removed by mask)
	# TODO: Should remove those outside the mask, not all black ones
	tempImgArr = res[
		(res[:,:,0] != 0) |
		(res[:,:,1] != 0) |
		(res[:,:,2] != 0)]

	# Calculate standard deviations and means (just for later analysis)
	stddevs = np.std(tempImgArr, axis=0)
	means = np.mean(tempImgArr, axis=0)

	return (stddevs, means)
