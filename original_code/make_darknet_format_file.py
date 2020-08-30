import os
import random

from tqdm import tqdm
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from class_list import LabelList
class_list, label_name = LabelList.ALL.value


def main():
    with open('../../billboard/model_data/billboard_' + label_name + '.txt', 'r', encoding='utf-8') as billboard:
        image_path_list = billboard.readlines()
        format_image_path_list = delete_zero_data(image_path_list)
        print('pytorch_yolov3用のテキストファイルを作成する')
        for image_path in tqdm(format_image_path_list):
            # image_list ['image_path', 'x1, y1, x2, y2, label', ...]
            element_list = image_path.split(' ')
            element_list.pop(-1)
            image_name = os.path.splitext(os.path.basename(element_list[0]))[0]
            save_path = '../../billboard/labels/{}/{}.txt'.format(label_name, image_name)
            save_text(save_path, element_list)


# ../billboard/labels/に保存
def save_text(save_path, element_list):
    # 該当ファイルが既に存在する場合は削除する
    if os.path.exists(save_path):
        os.system('rm ' + save_path)
    with open(save_path, 'w', encoding='utf-8') as save_file:
        for i in range(1, len(element_list)):
            x1, y1, x2, y2, label = element_list[i].split(',')
            x_center, y_center, width, height = resize_point(element_list[0], int(x1), int(y1), int(x2), int(y2))
            # label = class_list.index(label)
            save_file.write('{} {} {} {} {}\n'.format(label, x_center, y_center, width, height))


def resize_point(image_path, x1, y1, x2, y2):
    img = Image.open(image_path)
    img_width, img_height = img.size
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    x_center = x1 / img_width + width / 2
    y_center = y1 / img_height + height / 2

    return x_center, y_center, width, height


# ラベルの無い行を削除する
def delete_zero_data(image_path_list):
    print('ラベルの無い行を削除する')
    format_image_path_list = []
    for image_path in tqdm(image_path_list):
        list_element_num = image_path.split(' ')
        if len(list_element_num) >= 2:
            format_image_path_list.append(image_path)
        else:
            pass

    return format_image_path_list


if __name__ in '__main__':
    save_path = '../../billboard/labels/{}/'.format(label_name)

    os.system('rm {}'.format(os.path.join(save_path, '*')))

    main()

