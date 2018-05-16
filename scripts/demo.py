from pycocotools.coco import COCO
import numpy as np
import json
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2
import caffe
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir='G:/coco'
dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)

def draw_box(img, name, box, score):
	""" draw a single bounding box on the image """
	xmin, ymin, xmax, ymax = box

	box_tag = '{} : {:.2f}'.format(name, score)
	text_x, text_y = 5, 7

	cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 255), 2)
	boxsize, _ = cv2.getTextSize(box_tag, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
	cv2.rectangle(img, (xmin, ymin - boxsize[1] - text_y),
					(xmin + boxsize[0] + text_x, ymin), (0, 225, 0), -1)
	cv2.putText(img, box_tag, (xmin + text_x, ymin - text_y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)



# initialize COCO api for instance annotations
coco=COCO(annFile)

cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['zebra']);
#imgIds = coco.getImgIds(catIds=catIds );
#imgIds = coco.getImgIds(imgIds = [26145])
#img = coco.loadImgs(imgIds[0])[0]

imgIds = coco.getImgIds(catIds=catIds)
#imgIds = coco.getImgIds(imgIds=[461632])
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]

# load and display image
I = io.imread('%s/CocoImages/%s/%s'%(dataDir,dataType,img['file_name']))
image_name = "{}/CocoImages/{}/{}".format(dataDir,dataType,img['file_name'])
image = caffe.io.load_image(image_name)
# use url to load image
#plt.axis('off')
#plt.imshow(I)
#plt.show()

# load and display instance annotations
plt.imshow(I); plt.axis('off')
annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
anno_file = "G:/Test.json"

#with open(anno_file, "w") as f:
#    json.dump(anns, f, sort_keys=True, indent=2, ensure_ascii=False)

coco.showAnns(anns)
width = img["width"]
height = img["height"]
dw = 1. / (width)
dh = 1. / (height)
if(len(anns) > 0):
                for s_anno in anns:
                    x_min = s_anno["bbox"][0]
                    y_min = s_anno["bbox"][1]
                    x_max = x_min+s_anno["bbox"][2]
                    y_max = y_min+s_anno["bbox"][3]
                    x_min = round(x_min)
                    y_min = round(y_min)
                    x_max = round(x_max)
                    y_max = round(y_max)
                    cat_id = s_anno["category_id"]
                    bb = (int(x_min), int(y_min), int(x_max), int(y_max))
                    draw_box(image, "object", bb, 0.99)
                    #cv2.imshow('object detection', image)

#plt.imshow(I); plt.axis('off'); plt.show()
plt.imshow(image); plt.axis('off'); plt.show()

# initialize COCO api for person keypoints annotations
#annFile = '{}/annotations/person_keypoints_{}.json'.format(dataDir,dataType)
#coco_kps=COCO(annFile)

# load and display keypoints annotations
#plt.imshow(I); plt.axis('off')
#ax = plt.gca()
#annIds = coco_kps.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
#anns = coco_kps.loadAnns(annIds)
#coco_kps.showAnns(anns)

# initialize COCO api for caption annotations
#annFile = '{}/annotations/captions_{}.json'.format(dataDir,dataType)
#coco_caps=COCO(annFile)

# load and display caption annotations
#annIds = coco_caps.getAnnIds(imgIds=img['id']);
#anns = coco_caps.loadAnns(annIds)
#coco_caps.showAnns(anns)
#plt.imshow(I); plt.axis('off'); plt.show()