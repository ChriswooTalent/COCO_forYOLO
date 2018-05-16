import argparse
import os
from random import shuffle
import shutil
import subprocess
import sys
import shutil

HOMEDIR = "G:"
YoloImageSets_dir = "G:/coco/yolo/data/coco"

# If true, re-create all list files.
redo = True
# The root directory which holds all information of the dataset.
data_dir = "{}/coco".format(HOMEDIR)
yolodata_dir = "{}/coco/yolo".format(HOMEDIR)
# The directory name which holds the image sets.
imgset_dir = "data/ImageSets"
# The direcotry which contains the images.
img_dir = "CocoImages"
img_ext = "jpg"
dst_img_dir = "JPEGImages"
# The directory which contains the annotations.
#anno_dir = "annotations"
#anno_ext = "json"
train_list_file = "{}/train.txt".format(YoloImageSets_dir)
minival_list_file = "{}/val.txt".format(YoloImageSets_dir)
test_list_file = "{}/test.txt".format(YoloImageSets_dir)

src_label_dir = "G:/coco/yolo/data/labels"
dst_label_dir = "G:/coco/CocoImages/labels"

def change(path, path1):
    for f in os.listdir(path):
        if os.path.isfile(path + os.path.sep + f):
            a, b = os.path.splitext(f)
            if b != '.py':
                shutil.copy(path + os.sep + f, path1)
        elif os.path.isdir(path + os.path.sep + f):
            change(path + os.sep + f, path1)

# Create training set.
# We follow Ross Girschick's split.
if redo or not os.path.exists(train_list_file):
    datasets = ["train2017", "val2017"]
    img_files = []
    anno_files = []
    for dataset in datasets:
        imgset_file = "{}/{}/{}.txt".format(yolodata_dir, imgset_dir, dataset)
        with open(imgset_file, "r") as f:
            for line in f.readlines():
                name = line.strip("\n")
#                subset = name.split("_")[0]
                subset = dataset
                img_file = "{}/{}/{}.{}".format(img_dir, subset, name, img_ext)
                assert os.path.exists("{}/{}".format(data_dir, img_file)), \
                        "{}/{} does not exist".format(data_dir, img_file)
                abs_img_file = "{}/{}/{}/{}.{}".format(data_dir, img_dir, dst_img_dir, name, img_ext)
                img_files.append(abs_img_file)
    # Shuffle the images.
    idx = [i for i in xrange(len(img_files))]
    shuffle(idx)
    with open(train_list_file, "w") as f:
        for i in idx:
            f.write("{}\n".format(img_files[i]))

if redo or not os.path.exists(minival_list_file):
    datasets = ["val2017"]
    subset = "val2017"
    img_files = []
    anno_files = []
    for dataset in datasets:
        imgset_file = "{}/{}/{}.txt".format(yolodata_dir, imgset_dir, dataset)
        with open(imgset_file, "r") as f:
            for line in f.readlines():
                name = line.strip("\n")
                img_file = "{}/{}/{}.{}".format(img_dir, subset, name, img_ext)
                assert os.path.exists("{}/{}".format(data_dir, img_file)), \
                        "{}/{} does not exist".format(data_dir, img_file)
                abs_img_file = "{}/{}/{}/{}.{}".format(data_dir, img_dir, dst_img_dir, name, img_ext)
                img_files.append(abs_img_file)
    with open(minival_list_file, "w") as f:
        for i in xrange(len(img_files)):
            f.write("{}\n".format(img_files[i]))

if redo or not os.path.exists(test_list_file):
    datasets = ["test2017"]
    subset = "test2017"
    img_files = []
    anno_files = []
    for dataset in datasets:
        imgset_file = "{}/{}/{}.txt".format(yolodata_dir, imgset_dir, dataset)
        with open(imgset_file, "r") as f:
            for line in f.readlines():
                name = line.strip("\n")
                img_file = "{}/{}/{}.{}".format(img_dir, subset, name, img_ext)
                assert os.path.exists("{}/{}".format(data_dir, img_file)), \
                        "{}/{} does not exist".format(data_dir, img_file)
                abs_img_file = "{}/{}/{}/{}.{}".format(data_dir, img_dir, dst_img_dir, name, img_ext)
                img_files.append(abs_img_file)
    with open(test_list_file, "w") as f:
        for i in xrange(len(img_files)):
            f.write("{}\n".format(img_files[i]))

change(src_label_dir, dst_label_dir)

