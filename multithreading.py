#!/usr/bin/env python3
from multiprocessing import Pool
from main import analyze
from os import listdir
from os.path import isfile, join
import sys

imagesPath = ''
noProcesses = 0

for i in range(len(sys.argv)):
	if sys.argv[i] == '--images-path':
		i += 1
		imagesPath = sys.argv[i]
	elif sys.argv[i] == '--processes':
		i += 1
		noProcesses = int(sys.argv[i])
if imagesPath == '':
	print('Error: no images path specified')
	exit()
if noProcesses == 0:
	print('Error: number of processes not specified')
	exit()

filesList = [[join(imagesPath, f), f] for f in listdir(imagesPath) if (isfile(join(imagesPath, f)) and f.endswith('.jpg'))]

with Pool(noProcesses) as p:
	p.map(analyze, filesList)
