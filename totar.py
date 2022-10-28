import cv2
import os
import time
from cv2 import _INPUT_ARRAY_STD_VECTOR_MAT
import numpy as np
from elements.yolo import OBJ_DETECTION
from shutil import make_archive, rmtree, move
Object_classes = ['plate']
                
Object_classes1 = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                'hair drier', 'toothbrush' ]

Object_colors = list(np.random.rand(80,3)*255)
Object_detector = OBJ_DETECTION('weights/best.pt', Object_classes)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
print(gstreamer_pipeline(flip_method=0))
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
if cap.isOpened():
    i = 0
    while 1:
        ret, frame = cap.read()
        if ret:
            # detection process
            objs = Object_detector.detect(frame)

            # plotting
            for obj in objs:
                # print(obj)
                label = obj['label']
                score = obj['score']
                [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                color = Object_colors[Object_classes.index(label)]

                img = frame[ymin-4:ymax+4, xmin:xmax+10]

                try:
                    os.mkdir("Images")
                except:
                    pass
                ImagePath = "/home/totar/Totar/Images/PlateImage-{}.jpg".format(i)
                cv2.imwrite(ImagePath, img)
                i +=1

                frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)

        cv2.imshow("TOTAR", frame)

        keyCode = cv2.waitKey(30)
        if keyCode == ord('q'):
            # <---- caching license plate images ---->
            RegisData = 'RegisData-{}-{}'.format(time.strftime('%x'),time.strftime('%X'))
            RegisDataPath = '/home/totar/Totar/{}.zip'.format(RegisData)
            make_archive(
                RegisData,
                'zip',
                root_dir='/home/totar/Totar/Images',
            )
            move(
                RegisDataPath,
                '/home/totar/Totar/CacheData'
            )
            ImagesDir = '/home/totar/Totar/Images'
            rmtree(ImagesDir)
            # <---- caching license plate images ---->
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Unable to open camera")
