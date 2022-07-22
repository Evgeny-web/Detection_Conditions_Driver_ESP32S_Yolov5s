import cv2
import numpy as np
import uuid
import os
import time

IMAGES_PATH = os.path.join('data', 'images')
labels = ['awake', 'drowsy', 'sleep']
number_imgs = 10

cap = cv2.VideoCapture(0)

# for label in labels:
label = labels[2]
print(label)
print('Collecting images for {}'.format(label))
time.sleep(5)

for img_num in range(number_imgs):
    print('Collecting images for {}, image number{}'.format(label, img_num))

    # webcam Feed
    ret, frame = cap.read()

    # Naming out image path
    imgname = os.path.join(IMAGES_PATH, label + '.' + str(uuid.uuid1()) + '.jpg')

    # Writes out image to file
    cv2.imwrite(imgname, frame)
    # Render to the screen
    cv2.imshow('Image Collection', frame)

    time.sleep(3)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
