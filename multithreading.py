#!/usr/bin/env python3
from multiprocessing import Pool
from main import analyze
from os import listdir
from os.path import isfile, join

imagesPath = '../slike/'

filesList = [f for f in listdir(imagesPath) if isfile(join(imagesPath, f))]
finalFilesList = []
for file in filesList:
	if file.endswith('.jpg'):
		finalFilesList.append([join(imagesPath, file), file])

with Pool(4) as p:
	p.map(analyze, finalFilesList)
