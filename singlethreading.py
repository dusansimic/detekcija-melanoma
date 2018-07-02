#!/usr/bin/env python3
from main import analyze
from os import listdir
from os.path import isfile, join
import sys

imagesPath = ''
imagePath = ''

for i in range(len(sys.argv)):
	if sys.argv[i] == '--images-path':
		i += 1
		imagesPath = sys.argv[i]
	if sys.argv[i] == '--image-path':
		i += 1
		imagePath = sys.argv[i]

if imagesPath == '' and imagePath == '':
	print('Error: no images path specified')
	exit()

if imagesPath != '':
	filesList = [[join(imagesPath, f), f] for f in listdir(imagesPath) if (isfile(join(imagesPath, f)) and f.endswith('.jpg'))]

	for file in filesList:
		analyze(file)
else:
	analyze([imagePath, imagePath])
