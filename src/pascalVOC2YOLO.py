import xml.etree.ElementTree as ET
import pickle
import os
import shutil
from os.path import join
from operator import itemgetter

classes = ['bus', 'car'] # Add your classes
image_sets = ['train', 'val']
VOC_DIR = '/home/alx/dataset-VOC' # Path to the input PascalVOC dataset 
YOLO_DIR = '/home/alx/dataset-YOLO' # Path to where to save the YOLO dataset

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('%s/Annotations/%s.xml'%(VOC_DIR, image_id))
    out_file = open('%s/data/obj/%s.txt'%(YOLO_DIR, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def create_train_val_files(train, val):
    for image_set in image_sets:
        if image_set == 'train':
            with open('%s/data/%s.txt'%(YOLO_DIR, image_set), 'w') as list_file:
                list_file.write('\n'.join(list(set(train))))
        elif image_set == 'val':
            with open('%s/data/%s.txt'%(YOLO_DIR, image_set), 'w') as list_file:
                list_file.write('\n'.join(list(set(val))))

def create_obj_files():
    with open('%s/data/obj.names'%(YOLO_DIR), 'w') as f:
        f.write('\n'.join(classes))

    with open('%s/data/obj.data'%(YOLO_DIR), 'w') as f:
        f.write('classes = %s\n'%(len(classes)))
        for image_set in image_sets:
            if image_set == 'val':
                f.write('valid = data/%s.txt\n'%(image_set))
            else:
                f.write('%s = data/%s.txt\n'%(image_set, image_set))
        f.write('names = data/obj.names\n')
        f.write('backup = backup/')


def main():
    if not os.path.exists('%s/data/obj/'%(YOLO_DIR)):
            os.makedirs('%s/data/obj/'%(YOLO_DIR), exist_ok=True)

    train = []
    val = []
    sets = sorted(list(zip(classes, image_sets)) + list(zip(classes, image_sets[::-1])), key=itemgetter(0))
    for class_id, image_set in sets:
        image_ids = open('%s/ImageSets/Main/%s_%s.txt'%(VOC_DIR, class_id, image_set)).read().strip().split()
        image_ids = list(filter(lambda x: x not in ['-1', '1'], image_ids))
        for image_id in image_ids:
            if image_set == 'train':
                train.append(image_id)
            elif image_set == 'val':
                val.append(image_id)
            #print("Processing image: %s for %s set\n"%(image_id, image_set))
            image_id = os.path.splitext(image_id)[0]
            convert_annotation(image_id)
            if not os.path.isfile('%s/data/obj/%s.jpg'%(YOLO_DIR, image_id)):
                shutil.copy('%s/JPEGImages/%s.jpg'%(VOC_DIR, image_id), '%s/data/obj/%s.jpg'%(YOLO_DIR, image_id))

    create_train_val_files(train, val)
    create_obj_files()

if __name__ == "__main__":
    main()

