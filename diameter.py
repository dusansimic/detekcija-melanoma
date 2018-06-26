import cv2 as cv

def getMinEnclosingCircleRadius(contour):
	(x, y), radius = cv.minEnclosingCircle(contour)
	# cv.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
	# cv.imshow('image', image)

	return radius
