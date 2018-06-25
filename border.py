import cv2 as cv

def findDefects(contours, drawDefects, img):
	cnt = contours[0]
	hull = cv.convexHull(cnt, returnPoints = False)
	defects = cv.convexityDefects(cnt, hull)
	if not drawDefects:
		return defects
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		cv.line(img,start,end,[0,255,0],2)
		cv.circle(img,far,5,[0,0,255],-1)
	return (defects, img)

def compareContours(contour1, contour2):
	ret = cv.matchShapes(contour1, contour2, 1, 0.0)
	return ret

def getFittedEllipse(contour):
	ellipse = cv.fitEllipse(contour)
	return ellipse
