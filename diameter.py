import cv2 as cv

def getMinEnclosingCircleRadius(contour):
	_, radius = cv.minEnclosingCircle(contour)
	# cv.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
	# cv.imshow('image', image)
	# cv.waitKey()
	# cv.destroyAllWindows()

	return radius
