import os
import cv2
import json
import numpy as np
from utils.make_coco import *

def create_label():
	return {
		"info": add_info(),
		"licenses": add_licenses(),
		"categories": add_categories(),
		"images": add_images(),
		"annotations": add_annotations(),
	}

def load_label():
	f = open(label_path)
	return json.load(f)

def save_label():
	with open(label_path, 'w') as outfile:
		json.dump(label, outfile)

def make_categories(label):
	d = {}
	for c in label['categories']:
		d[c["id"]] = {
			"supercategory": c["supercategory"],
			"name": c["name"],
		}
	return d

def update(label):
	label["annotations"][index]["area"] = bbox[2] * bbox[3]
	label["annotations"][index]["bbox"] = bbox
	return label

def mouse_event(event, x, y, flags, param):
	global mx, my, lx, ly, rx, ry
	
	# mouse move
	if event == cv2.EVENT_MOUSEMOVE:
		mx, my = x, y
		display()

	# left mouse click
	if event == cv2.EVENT_LBUTTONUP:
		lx, ly = x, y
		display()

	# right mouse click
	if event == cv2.EVENT_RBUTTONUP:
		rx, ry = x, y
		display()

def display():
	global mx, my, lx, ly, rx, ry, bx1, by1, clicked, bbox

	# clone original
	display = image.copy()

	# draw measure line
	if mx + my > 0:
		cv2.line(display, (0, my), (img_w, my), color, 1)
		cv2.line(display, (mx, 0), (mx, img_h), color, 1)

	# left click event
	if lx + ly > 0:
		if not clicked:
			bx1, by1, lx, ly = lx, ly, -1, -1
		elif clicked:
			x1, x2 = [x for x in sorted([bx1, lx])]
			y1, y2 = [y for y in sorted([by1, ly])]
			bbox = x1, y1, x2-x1, y2-y1
			bx1, by1, lx, ly = -1, -1, -1, -1
		clicked = not clicked

	# right click event
	if rx + ry > 0:
		if not clicked:
			bbox = 0, 0, 0, 0
		elif clicked:
			bx1, by1 = -1, -1
			clicked = False
		rx, ry = -1, -1

	# draw pre-build line
	if bx1 + by1 > 0:
		cv2.line(display, (0, by1), (img_w, by1), color, 2)
		cv2.line(display, (bx1, 0), (bx1, img_h), color, 2)

	# draw bbox
	x, y, w, h = bbox
	cv2.rectangle(display, (x, y), (x+w, y+h), color, 2)

	# display
	cv2.imshow("display", display)

root = ''
images_path = os.path.join(root, "images")
label_path = os.path.join(root, "label.json")
label = {}

index = 0
mx, my = -1, -1
lx, ly = -1, -1
rx, ry = -1, -1
bx1, by1 = -1, -1
clicked = False
color = (0, 0, 255)

if __name__ == '__main__':

	# make label data
	label = load_label() if os.path.exists(label_path) else create_label()
	cards = make_categories(label)
	total = len(label["images"])

	# main loop
	while True:

		# get image data
		img_path = label["images"][index]["file_name"]
		img_h = label["images"][index]["height"]
		img_w = label["images"][index]["width"]

		# load image
		image = cv2.imread(img_path)

		# get label data
		bbox = label["annotations"][index]["bbox"]
		area = label["annotations"][index]["area"]
		category_id = label["annotations"][index]["category_id"]
		supercategory = cards[category_id]["supercategory"]
		name = cards[category_id]["name"]

		# show progress & meta data
		print('-----------------------------------------')
		print(index+1, 'of', total)
		print('supercategory', supercategory)
		print('name', name)
		print('bbox', bbox)
		print('area', area)
		print('-----------------------------------------')

		# draw display
		display()

		# user feedback
		cv2.setMouseCallback('display', mouse_event)
		key = cv2.waitKeyEx(0)
		if key in [ord("q"), 27]: 
			break
		elif key in [ord("a")]: 
			label = update(label)
			index = np.clip(index-1, 0, total-1)
		elif key in [ord("d")]: 
			label = update(label)
			index = np.clip(index+1, 0, total-1)
		elif key in [ord(" ")]: 
			label = update(label)
			save_label()