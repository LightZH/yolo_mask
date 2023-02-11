import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.plots import Annotator, colors, save_one_box
from tqdm import tqdm


def loadtxt(height, width, srclabel):
    f = open(srclabel)
    data = f.readlines()  # 逐行读取txt并存成list。每行是list的一个元素，数据类型为str
    dataset = []
    for row in range(len(data)):  # len(data)为数据行数
        temp = data[row].strip('\n').split(' ')
        dataset.append(temp)
    faces = []
    if len(dataset) >= 1:
        for d in range(len(dataset)):
            cn = float(dataset[d][0])
            cx = float(dataset[d][1]) * width
            cy = float(dataset[d][2]) * height
            w = float(dataset[d][3]) * width
            h = float(dataset[d][4]) * height
            faces.append([cn, cx - w / 2, cy - h / 2, w, h])
    return faces


def split_pic(src):
    imges = []  # 存储所有图片的路径
    # 第一步：遍历需要分离的文件夹
    for f in os.listdir(src):
        if f.endswith(".jpg"):  # 可以是.jpg,.png,.jpeg等等
            imges.append(f)
    return imges


def img_nose_detector(img_path, srclabel, nose_cascade_file):
    image = cv2.imread(img_path)
    height, width, _ = image.shape
    nose_cascade = cv2.CascadeClassifier(nose_cascade_file)
    if nose_cascade.empty():
        raise IOError('Unable to load the nose cascade classifier xml file!')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = loadtxt(height, width, srclabel)
    face_rect = np.array(faces, dtype=int)
    names = ["no_mask", "mask_nor", "mask_unnor"]
    annotator = Annotator(image, line_width=3, example=str(names))
    # 在检测到的脸部周围画矩形框
    for (cn, x, y, w, h) in face_rect:
        face_list = [x, y, x + w, y + h]
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
        if cn == 1:
            yz = (y + h + h / 5) if (y + h + h / 5) < height else height
            xz = (x + w + w / 5) if (x + w + w / 5) < width else width
            roi = gray[y:int(yz), x:int(xz)]
            nose_rects = nose_cascade.detectMultiScale(roi, 1.3, 5)
            if len(nose_rects) != 0:
                for (x_nose, y_nose, w_nose, h_nose) in nose_rects:
                    cv2.rectangle(image, (x + x_nose, y + y_nose), (x + x_nose + w_nose, y + y_nose + h_nose),
                                  (0, 255, 0), 3)
                    break  # 一张脸上只能有一个鼻子，故而此处break
                annotator.box_label(face_list, names[2], color=colors(2, True))
                # cv2.putText(image, "mask_unnor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
            else:
                # cv2.putText(image, "mask_nor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
                annotator.box_label(face_list, names[1], color=colors(1, True))
        else:
            annotator.box_label(face_list, names[0], color=colors(0, True))
            # cv2.putText(image, "no_mask", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
    im0 = annotator.result()
    return im0


def main_nose(pic_path, res_path):
    pic_names = split_pic(pic_path)
    for pic_name in tqdm(pic_names):
        img_path = os.path.join(pic_path, pic_name)
        srclabel = os.path.join((res_path + '/labels/'), pic_name[0:-4]) + '.txt'
        nose_cascade_file = './weights/haarcascade_mcs_nose.xml'
        save_path = os.path.join(res_path, "mask_face")
        if not os.path.isdir(save_path):  # 如果目标图片文件夹不存在
            os.mkdir(save_path)
        save_name = os.path.join(save_path, pic_name)
        if os.path.exists(srclabel):
            # image1, flag_nose = img_nose_detector(img_path, srclabel, nose_cascade_file, True)
            image1 = img_nose_detector(img_path, srclabel, nose_cascade_file)
        else:
            image1 = cv2.imread(img_path)
        cv2.imwrite(save_name, image1)
        # image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        # plt.imshow(image1)
        # plt.show()


if __name__ == '__main__':
    pic_path = './data/testimages'
    res_path = './runs/detect/exp'
    main_nose(pic_path, res_path)
