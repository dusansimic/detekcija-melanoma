def findLargestContour(contours):
	largest = 0
	for i in range(1, len(contours) - 1):
		if len(contours[i]) > len(contours[largest]): largest = i
	return contours[largest]