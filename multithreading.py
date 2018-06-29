#!/usr/bin/env python3
from multiprocessing import Pool
from main import analyze
from os import listdir
from os.path import isfile, join

filesList = [f for f in listdir('/home/dusan/Downloads/slike/') if isfile(join('/home/dusan/Downloads/slike/', f))]
finalFilesList = []
for file in filesList:
	if file.endswith('.jpg'):
		finalFilesList.append(join('/home/dusan/Downloads/slike/', file))

with Pool(8) as p:
	p.map(analyze, finalFilesList)

# print(filesList)

# if __name__ == '__main__':
# 	with Pool(processes = 4) as pool:

