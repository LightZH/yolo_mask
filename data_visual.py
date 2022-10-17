# 实现数据集的可视化
import cv2
import os
from tqdm import tqdm


def split(src):
    imges = []  # 存储所有图片的路径
    annotation = []  # 存储所有标注文件的路径
    # 第一步：遍历需要分离的文件夹
    for f in os.listdir(src):
        imges.append(f)
        # f = os.path.join(src, f)
        # if f.endswith(".jpg"):  # 可以是.jpg,.png,.jpeg等等
        #     imges.append(f)
        # if f.endswith(".txt"):  # 可以是json文件或者xml文件
        #     annotation.append(f)
    return imges, annotation


def read_txt(inputpath):
    SaveList = []
    with open(inputpath, "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n').split()  # 删除换行符
            SaveList.append(line)
        file.close()
    return SaveList


if __name__ == "__main__":
    # input_path = 'H:/mask_data/no_mask/txt/PartB_00056.txt'
    # input_img = 'H:/mask_data/no_mask/txt/PartB_00056.jpg'
    src_image = 'H:/mask_data/images'
    src_label = 'H:/mask_data/labels'
    srcv = 'H:/mask_data/visual'
    if not os.path.isdir(srcv):  # 如果文件夹不存在
        os.mkdir(srcv)
    # image和annotation返回是一个长度为2的元组？？
    images = split(src_image)[0]
    annotations = split(src_label)[0]
    for i in tqdm(range(len(images))):
        visual_path = os.path.join(srcv, images[i])
        image = cv2.imread(os.path.join(src_image, images[i]))
        height, width, _ = image.shape
        data_list = read_txt(os.path.join(src_label, annotations[i]))
        for boxnum in range(len(data_list)):
            box = data_list[boxnum]
            name = "face" if box[0] == '0' else "mask"
            cx = float(box[1]) * width
            cy = float(box[2]) * height
            w = float(box[3]) * width
            h = float(box[4]) * height
            xmin = int(cx - w / 2)
            ymin = int(cy - h / 2)
            xmax = int(cx + w / 2)
            ymax = int(cy + h / 2)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
            cv2.putText(image, name, (xmin - 5, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imwrite(visual_path, image)



