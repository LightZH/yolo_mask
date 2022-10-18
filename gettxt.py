import os
import random


def split(src):
    file = []  # 存储所有图片的路径
    for f in os.listdir(src):
        file.append(f)
    return file


def write_txt(path, flod, data_list):
    f = open(os.path.join(path, (flod + ".txt")), 'w')
    for fp in data_list:
        f.write(str(fp))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    image_mask = "./data/images"
    # label_mask = "./data/labels"
    image_list = split(image_mask)
    random.shuffle(image_list)
    train_list = []
    test_list = []
    val_list = []
    train_rate = 0.9
    test_rate = 0.09
    # label_list = split(label_mask)
    for i in range(len(image_list)):
        if i < int(len(image_list) * train_rate):
            train_list.append("data/images/" + image_list[i])
        elif i < int(len(image_list) * (train_rate + test_rate)):
            test_list.append("data/images/" + image_list[i])
        else:
            val_list.append("data/images/" + image_list[i])
    write_txt("./data", "train", train_list)
    write_txt("./data", "test", test_list)
    write_txt("./data", "val", val_list)

    print(len(image_list))
