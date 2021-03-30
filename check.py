import os
import cv2
import json
import numpy as np
from utils.make_coco import *

def load_label():
	f = open(label_path)
	return json.load(f)

def make_categories(label):
	d = {}
	for c in label['categories']:
		d[c["id"]] = {
			"supercategory": c["supercategory"],
			"name": c["name"],
		}
	return d	

if __name__ == '__main__':

	# make label data
	root = ''
	label_path = os.path.join(root, "label.json")
	label = load_label() if os.path.exists(label_path) else create_label()
	cards = make_categories(label)
	total = len(label["images"])
	index = 0

	# main loop
	while True:

		# get image data
		img_path = label["images"][index]["file_name"]
		image = cv2.imread(img_path)

		# get label data
		bbox = label["annotations"][index]["bbox"]
		area = label["annotations"][index]["area"]
		category_id = label["annotations"][index]["category_id"]
		supercategory = cards[category_id]["supercategory"]
		name = cards[category_id]["name"]

		# show meta data
		print('-----------------------------------------')
		print('supercategory', supercategory)
		print('name', name)
		print('bbox', bbox)
		print('area', area)
		print('-----------------------------------------')

		# show bbox and image
		x, y, w, h = bbox
		color = (0, 255, 0)
		cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
		cv2.imshow('display', image)

		# user feedback
		key = cv2.waitKey(0)
		if key in [ord('q')]:
			break
		elif key in [ord("a")]: 
			index = np.clip(index-1, 0, total-1)
		elif key in [ord("d")]: 
			index = np.clip(index+1, 0, total-1)
