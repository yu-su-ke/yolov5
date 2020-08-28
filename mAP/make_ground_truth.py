import glob
import os
import random

from tqdm import tqdm
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from scripts.extra.intersect_gt_and_dr import adjust_ground_and_detect
from class_list import LabelList


def main(label_list, learn_label_type):
    image_size = 608
    text_file_list = glob.glob('../../billboard/labels/*.txt')
    for text_file in tqdm(text_file_list):
        with open(text_file, 'r', encoding='utf-8') as text:
            save_path = './input/billboard_' + learn_label_type + '/ground-truth/' + \
                        os.path.splitext(os.path.basename(text_file))[0] + \
                        '.txt'  # 保存するパス
            with open(save_path, 'w', encoding='utf-8') as ground_truth:
                image_point_list = text.readlines()
                for image_point in image_point_list:
                    list_element = image_point.split(' ')
                    # print(list_element)
                    label = label_list[int(list_element[0])]
                    # 608 * 608に修正
                    left, top, right, bottom = \
                        convert_yolo_coordinates_to_voc(float(list_element[1]), float(list_element[2]),
                                                        float(list_element[3]), float(list_element[4]),
                                                        image_size, image_size)
                    ground_truth.write('{} {} {} {} {}'.format(label, left, top, right, bottom))
                    ground_truth.write('\n')


def convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height):
    # remove normalization given the size of the image
    x_c = float(x_c_n) * img_width
    y_c = float(y_c_n) * img_height
    width = float(width_n) * img_width
    height = float(height_n) * img_height
    # compute half width and half height
    half_width = width / 2
    half_height = height / 2
    # compute left, top, right, bottom
    # in the official VOC challenge the top-left pixel in the image has coordinates (1;1)
    left = int(x_c - half_width) + 1
    top = int(y_c - half_height) + 1
    right = int(x_c + half_width) + 1
    bottom = int(y_c + half_height) + 1
    return left, top, right, bottom


if __name__ in '__main__':
    label_list, label_name = LabelList.ALL.value
    os.system('rm -rf ./input/billboard_' + label_name + '/ground-truth/*')
    main(label_list, label_name)

    # ground_truthとdetect両方に存在しないファイルを削除する. これを回すとground-truthがnullになるので最初だけ回す
    adjust_ground_and_detect(label_name)
