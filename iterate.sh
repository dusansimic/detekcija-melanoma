#!/bin/bash
for filename in ./images/uncut/*.jpg; do
	echo "$filename"
	./main.py --image-path "$filename"
done
