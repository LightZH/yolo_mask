import cv2
import numpy as np
from tqdm import tqdm
from lxml import etree
import os
from tqdm import tqdm


def split(src):
    file = []  # 存储所有图片的路径
    for f in os.listdir(src):
        file.append(f)
    return file


def parse_xml_to_dict(xml):
    if len(xml) == 0:  # 遍历到底层，直接返回tag对应的信息
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = parse_xml_to_dict(child)  # 递归遍历标签信息
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:  # 因为object可能有多个，所以需要放入列表里
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def get_box_bndbox(xml_path):
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    name = []
    # read xml
    with open(xml_path) as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    data = parse_xml_to_dict(xml)["annotation"]
    img_height = int(data["size"]["height"])
    img_width = int(data["size"]["width"])

    assert "object" in data.keys(), "file: '{}' lack of object key.".format(xml_path)
    if len(data["object"]) == 0:
        # 如果xml文件中没有目标就直接忽略该样本
        print("Warning: in '{}' xml, there are no objects.".format(xml_path))
        return

    for index, obj in enumerate(data["object"]):
        namebox = obj["name"]
        xminbox = float(obj["bndbox"]["xmin"])
        yminbox = float(obj["bndbox"]["ymin"])
        xmaxbox = float(obj["bndbox"]["xmax"])
        ymaxbox = float(obj["bndbox"]["ymax"])
        wbox = xmaxbox - xminbox
        hbox = ymaxbox - yminbox
        # 进一步检查数据，有的标注信息中可能有w或h为0的情况，这样的数据会导致计算回归loss为nan
        if wbox <= 0 or hbox <= 0:
            print("Warning: in '{}' xml, there are some bbox w/h <=0".format(xml_path))
            continue
        name.append(namebox)
        xmin.append(xminbox)
        ymin.append(yminbox)
        xmax.append(xmaxbox)
        ymax.append(ymaxbox)
    return name, xmin, ymin, xmax, ymax, img_height, img_width


def write_txt(path, flags, cx, cy, w, h):
    f = open((path + ".txt"), 'w')
    for i in range(len(flags)):
        f.write(str(flags[i]))
        f.write(" ")
        f.write(str(cx[i]))
        f.write(" ")
        f.write(str(cy[i]))
        f.write(" ")
        f.write(str(w[i]))
        f.write(" ")
        f.write(str(h[i]))
        f.write("\n")
    f.close()


def write_txt1(path, flod, data_list):
    f = open(os.path.join(path, (flod + ".txt")), 'w')
    for fp in data_list:
        f.write(str(fp))
        f.write("\n")
    f.close()


def get_box(image, label):
    flags = []
    cx = []
    cy = []
    w = []
    h = []
    wrong = []
    # 判断是否存在
    assert os.path.exists(image), "file:{} not exist...".format(image)
    assert os.path.exists(label), "file:{} not exist...".format(label)
    # 读取图片信息
    img = cv2.imread(image)
    # -----------------------------两点标注(xmin,ymin,xmax,ymax)的目标可视化--------------------------------
    name, xmin, ymin, xmax, ymax, img_height, img_width = get_box_bndbox(label)
    height, width, _ = img.shape
    assert height == img_height, "height error"
    assert width == img_width, "width error"
    boxes = []  # list类型
    for i in range(len(name)):
        box_temp = [name[i], xmin[i], ymin[i], xmax[i], ymax[i]]
        boxes.append(box_temp)
    for box_num in range(len(boxes)):
        box = boxes[box_num]
        namebox = box[0]
        xminbox = box[1]
        yminbox = box[2]
        xmaxbox = box[3]
        ymaxbox = box[4]
        cx.append((xminbox + xmaxbox) / 2 / img_width)
        cy.append((yminbox + ymaxbox) / 2 / img_height)
        w.append((xmaxbox - xminbox) / img_width)
        h.append((ymaxbox - yminbox) / img_height)
        if namebox == "rightmask":
            flag = 1
        elif namebox == "nomask":
            flag = 0
        else:
            flag = 2
            wrong.append(image)
        flags.append(flag)
    return flags, cx, cy, w, h, wrong


if __name__ == '__main__':
    image_mask = "H:/part1/image"
    # image_nomask = "H:/dataset with label/image_nomask"
    label_mask = "H:/part1/label"
    # label_nomask = "H:/dataset with label/label_nomask"
    # images_mask = split(image_mask)
    # images_nomask = split(image_nomask)
    # labels_mask = split(label_mask)
    # labels_nomask = split(label_nomask)
    image_list = split(image_mask)
    label_list = split(label_mask)
    # print(label_list[514])
    # print(label_list[515])
    wrongs = []
    for i in tqdm(range(len(image_list))):
        name = str(i)
        while len(name) < 4:
            name = "0" + name
        image = image_mask + "/" + image_list[i]
        label = label_mask + "/" + label_list[i]
        flags, cx, cy, w, h, wrong = get_box(image, label)
        save_path = image_mask + "/" + name
        # else:
        #     name = str(i - 514)
        #     while len(name) < 4:
        #         name = "0" + name
        #     image = image_nomask + "/" + image_list[i]
        #     label = label_nomask + "/" + label_list[i]
        #     flags, cx, cy, w, h, wrong = get_box(image, label)
        #     save_path = image_nomask + "/" + name
        write_txt(save_path, flags, cx, cy, w, h)
        for j in range(len(wrong)):
            wrongs.append(wrong[j])
        write_txt1("H:/part1", "wrong", wrongs)
    print("done")

