import os
import cv2

root = './'
images_path = os.path.join(root, "images")

# label: info
def add_info():
	return {
    	"description": "RPi Card Image",
    	"url": "",
    	"version": "1.0",
    	"year": 2021,
    	"contributor": "AIMLab",
    	"date_created": "2021/02/23",
	}

# label: licenses
def add_licenses():
	return [
		{
			"url": "",
			"id": 1,
			"name": "AIMLab, Mahidol U.",
		}
	]

# label: categories
def add_categories():
	categories = []
	count = 1
	for superfolder in os.listdir(images_path):
		folders = os.listdir(os.path.join(images_path, superfolder))
		for folder in folders:
			d = {
				"supercategory": superfolder[:-3],
				"id": count,
				"name": folder,
			}
			categories.append(d)
			count += 1
	return categories

# label: images
def add_images():
	images = []
	count = 1
	for superfolder in os.listdir(images_path):
		folders = os.listdir(os.path.join(images_path, superfolder))
		for folder in folders:
			files = os.listdir(os.path.join(images_path, superfolder, folder))
			for file in files:
				d = {
					"license": 1,
					"file_name": "images/" + superfolder + "/" + folder + "/" + file,
					"height": 480,
					"width": 640,
					"id": count,
				}
				images.append(d)
				count += 1
	return images

# label: annotations (default bbox= 0 0 0 0)
def add_annotations():
	annotations = []
	image_id = 1
	category_id = 1
	for superfolder in os.listdir(images_path):
		folders = os.listdir(os.path.join(images_path, superfolder))
		for folder in folders:
			files = os.listdir(os.path.join(images_path, superfolder, folder))
			for file in files:
				d = {
					"area": 0,
					"iscrowd": 0,
					"image_id": image_id,
					"bbox": [0, 0, 0, 0],
					"category_id": category_id,
					"id": image_id,
				}
				annotations.append(d)
				image_id += 1
			category_id += 1
	return annotations
