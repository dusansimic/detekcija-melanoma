#!/usr/bin/env python3
from multiprocessing import Pool
from main import analyze
from os import listdir
from os.path import isfile, join
import sys
import tqdm

imagesPath = ''
noProcesses = 0
outputFile = 'results.csv'

for i in range(len(sys.argv)):
	if sys.argv[i] == '--images-path':
		i += 1
		imagesPath = sys.argv[i]
	elif sys.argv[i] == '--processes':
		i += 1
		noProcesses = int(sys.argv[i])
	elif sys.argv[i] == '--output':
		i += 1
		outputFile = sys.argv[i]
		
if imagesPath == '':
	print('Error: no images path specified')
	exit()
if noProcesses == 0:
	print('Error: number of processes not specified')
	exit()

filesList = [[join(imagesPath, f), f, outputFile] for f in listdir(imagesPath) if (isfile(join(imagesPath, f)) and f.endswith('.jpg'))]

f = open(outputFile, 'a')
f.write('file name,asymmetry result,border deviation,hstddevs,hmeans,sstddevs,smeans,vstddevs,vmeans,real diameter')
f.close()

with Pool(noProcesses) as p:
	for _ in tqdm.tqdm(p.imap(analyze, filesList), total=len(filesList)):
		pass
