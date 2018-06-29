#!/bin/bash
for filename in ~/Downloads/complete_mednode_dataset/melanoma/*.jpg; do
	echo "$filename"
	./main.py --image-path "$filename"
done
