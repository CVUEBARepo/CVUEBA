import numpy as np
import cv2
import random
import shutil

"""
Novel augmentations proposed in the paper.
For demonstration purposes, we only apply
each augmentation once per attack encoding.
"""

IN_FOLDER = "TrainImages"
OUT_FOLDER = "AugImages"

def channel_swap(path, in_folder, out_folder):
	im = cv2.imread(path)
	channel_1 = im[:, :, 0]
	channel_2 = im[:, :, 1]
	channel_3 = im[:, :, 2]
	stack = np.stack((channel_2, channel_1, channel_3), axis=-1)

	file_name = path.split(".")[0]
	file_type = path.split(".")[1]
	write_name = f"{file_name}_swap.{file_type}"
	write_name = write_name.replace(in_folder, out_folder)
	cv2.imwrite(write_name, stack)

def get_user_from_path(path):
	file = path.split("/")[2]
	return file.split("_")[0]

def get_random_benign_from_user(user):
	folder = os.path.join(IN_FOLDER, "0")
	files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	userfiles - [f for f in files if user in f]
	choice_file = random.choice(userfiles)
	return os.path.join(folder, choice_file)

def channel_replace(path, in_folder, out_folder):
	im = cv2.imread(path)
	channel_3 = im[:, :, 2]

	im_user = get_user_from_path(path)
	rand_path = get_random_benign_from_user(im_user)
	rand_im = cv2.imread(rand_path)
	channel_1 = rand_im[:, :, 0]
	channel_2 = rand_im[:, :, 1]

	stack = np.stack((channel_1, channel_2, channel_3), axis=-1)

	file_name = path.split(".")[0]
	file_type = path.split(".")[1]
	write_name = f"{file_name}_replace.{file_type}"
	write_name = write_name.replace(in_folder, out_folder)
	cv2.imwrite(write_name, stack)

try:
	os.makedirs(f"{OUT_FOLDER}/0")
except:
	pass

try:
	os.makedirs(f"{OUT_FOLDER}/1")
except:
	pass

try:
	os.makedirs(f"{OUT_FOLDER}/2")
except:
	pass

try:
	os.makedirs(f"{OUT_FOLDER}/3")
except:
	pass

# Do not augment benign images. Just copy those over
shutil.copytree(f"{IN_FOLDER}/0", f"{OUT_FOLDER}/0")
for scenario in [1, 2, 3]:
	directory_path = os.path.join(IN_FOLDER, str(scenario))
	images = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
	for image in images:
		path = os.path.join(directory_path, images)
		channel_swap(path, IN_FOLDER, OUT_FOLDER)
		channel_replace(path, IN_FOLDER, OUT_FOLDER)