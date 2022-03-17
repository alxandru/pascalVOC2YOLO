# Convert PascalVOC Dataset to YOLO

This scripts converts a PascalVOC dataset to YOLO format.
It has the following functionality:
* creates the directory structure needed in order to train a YOLO network
* creates the `obj.data`, `obj.names`, `train.txt` and `val.txt` files based on the given input 
* reads the xml files and converts them to YOLO txt files and saves them to `data/obj/`
* copy the image files from PascalVOC `JPEGImages/` folder to YOLO `data/obj/`

The PascalVOC dataset was generated with the [VOTT](https://github.com/microsoft/VoTT) annotation and labeling tool from a [video](https://drive.google.com/file/d/1fB_WHSA1YQJFTdtwfhpDPp4PbMZofKJm/view?usp=sharing) recorded and labeled by me and has the following directory structure:
```bash
.
├── Annotations
│   ├── test001.mp4#t=0.1.xml
│   ├── test001.mp4#t=0.2.xml
│   ...
├── ImageSets
│   └── Main
│       ├── bus_train.txt
│       ├── bus_val.txt
│       ├── car_train.txt
│       └── car_val.txt
└── JPEGImages
    ├── test001.mp4#t=0.1.jpg
    ├── test001.mp4#t=0.2.jpg
    ...
```

After running the [pascalVOC2YOLO.py](src/pascalVOC2YOLO.py) script the generated YOLO dataset should be:

```bash
.
└── data
    └── obj
    │   ├── test001.mp4#t=0.1.jpg
    │   ├── test001.mp4#t=0.1.txt
    │   ├── test001.mp4#t=0.2.jpg
    │   ├── test001.mp4#t=0.2.txt
    │   ...
    │
    ├── obj.data
    ├── obj.names
    ├── train.txt
    └── val.txt
```

Where the YOLO txt files under the `obj` folder have the format:
```bash
alx@jnano1:~/dataset-YOLO/data/obj$ cat test001.mp4#t=0.1.txt
1 0.8065568943695005 0.7365158472839091 0.050766507208635285 0.04888481655003832
1 0.08474938686836826 0.7325652625446453 0.04552266480924344 0.04590375467312116
1 0.13165040789512703 0.7152108707094267 0.0375028179792637 0.04116810055598158
1 0.1768199617900546 0.6906309648308799 0.05906558250706307 0.057836839172737686
```

If you are interested in the YOLO dataset I generated with this script you can download it from [here](https://drive.google.com/file/d/1CswmUyLhKtTSx8NT4RGMML60SWHtJG7M/view?usp=sharing). The dataset is called [Roundabout Traffic Dataset](https://github.com/alxandru/yolov4_roundabout_traffic/blob/main/data/README.md) since it is based on a recorded video with a fixed camera in a roundabout.

The script was tested on [NVIDIA Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit).

Disclaimer: This code is a modified version of Joseph Redmon's [voc_label.py](https://github.com/pjreddie/darknet/blob/master/scripts/voc_label.py).

## How to run

Before running the script you need to edit a few variables.

1. Modify the `classes` variable at line 8. Make sure to keep the order of classes correct.
```python
classes = ['bus', 'car'] # Add your classes
```

2. Point where your PascalVOC dataset is by changing `VOC_DIR` at line 10.

```python
VOC_DIR = '/home/alx/dataset-VOC' # Path to the input PascalVOC dataset 
```
3. Edit the `YOLO_DIR` at line 11 to set the output folder.

```python
YOLO_DIR = '/home/alx/dataset-YOLO' # Path to where to save the YOLO dataset
```

Finally run the script. How long it takes to run depends on your dataset and your environment.

```python
python pascalVOC2YOLO.py
```
