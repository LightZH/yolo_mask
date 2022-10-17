import random
import os
import shutil
from tqdm import tqdm


# 区分后以txt格式存储
def split(src):
    imges = []  # 存储所有图片的路径
    annotation = []  # 存储所有xml的路径
    # 第一步：遍历需要分离的文件夹
    for f in os.listdir(src):
        f = os.path.join(src, f)
        if f.endswith(".jpg"):  # 可以是.jpg,.png,.jpeg等等
            imges.append(f)
        if f.endswith(".txt"):  # 可以是json文件或者xml文件
            annotation.append(f)
    return imges, annotation


# # 第二步：创建目标图片文件夹和xml文件夹
# if not os.path.isdir(img):  # 如果目标图片文件夹不存在
#     os.mkdir(img)
# if not os.path.isdir(annota):  # 如果目标xml文件夹不存在
#     os.mkdir(annota)
# # 第三步：转移到目标文件夹中
# for im in imges:  # 遍历所有的图片，将图片文件转移到目标文件夹中
#     new_path = os.path.join(src, im)
#     # print(new_path)
#     shutil.copy(new_path, img)
# for ann in annotation:  # 遍历所有的xml,将xml文件转移到目标文件夹中
#     new_path = os.path.join(src, ann)
#     # print(new_path)
#     shutil.copy(new_path, annota)
# return imges, annotation
# if __name__ == '__main__':
#     img = "F:/APP/Pycharm/FILE/yolo/yolov5_mask/data/images"
#     annota = "F:/APP/Pycharm/FILE/yolo/yolov5_mask/data/labels"
#     src = 'H:/labels'
#     image,  annotation = split(src)  # 存放的图片路径
#     # for i in range(len(image)):
#     #     name = str(i)
#     #     while len(name) < 3:
#     #         name = "0" + name
#     #     new_name_img = os.path.join(src1, name) + ".jpg"
#     #     new_name_ann = os.path.join(src1, name) + ".txt"
#     #     shutil.move(image[i], new_name_img)
#     #     shutil.move(annotation[i], new_name_ann)
#     if not os.path.isdir(img):  # 如果目标图片文件夹不存在
#         os.mkdir(img)
#     if not os.path.isdir(annota):  # 如果目标txt文件夹不存在
#         os.mkdir(annota)
#     # 第三步：转移到目标文件夹中
#     for im in image:  # 遍历所有的图片，将图片文件转移到目标文件夹中
#         # new_path = os.path.join(src, im)
#         # print(new_path)
#         shutil.copy(im, img)
#     for ann in annotation:  # 遍历所有的xml,将xml文件转移到目标文件夹中
#         # new_path = os.path.join(src, ann)
#         # print(new_path)
#         shutil.copy(ann, annota)
def write_txt(path, flod, data_list):
    f = open(os.path.join(path, (flod + ".txt")), 'w')
    for fp in data_list:
        f.write(str(fp))
        f.write("\n")
    f.close()


if __name__ == "__main__":
    src = "F:/APP/Pycharm/FILE/yolo/yolov5_mask/data/images"
    dis = "F:/APP/Pycharm/FILE/yolo/yolov5_mask/data"
    images = []
    for f in os.listdir(src):
        name = "data/images/" + f
        images.append(name)
    random.shuffle(images)
    train = []
    test = []
    val = []
    for i in range(len(images)):
        if i < 360:
            train.append(images[i])
        elif i < 396:
            test.append(images[i])
        else:
            val.append(images[i])
    write_txt(dis, "train", train)
    write_txt(dis, "test", test)
    write_txt(dis, "val", val)

