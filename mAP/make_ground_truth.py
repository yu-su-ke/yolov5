import glob
import json
import os

import cv2
from tqdm import tqdm

from scripts.extra.intersect_gt_and_dr import adjust_ground_and_detect
from class_list import LabelList


class MakeGroundTruth:
    def __init__(self, class_list, label_name, task_name):
        self.class_list = class_list
        self.label_name = label_name
        self.task_name = task_name

        self.text_base_path = '../../annotation_data/{}_annotation/'.format(self.task_name)
        self.label_base_path = '../../{}/labels/test/'.format(self.task_name)
        self.label_dictionary = {}

    def main(self):
        # 基本こっち
        directory_path_list = glob.glob(os.path.join(self.label_base_path, '*'))
        for directory_path in tqdm(directory_path_list):
            self.write_annotation_path_image(directory_path)

        # directory_path_list = glob.glob(os.path.join(self.text_base_path, '*'))
        # for directory_path in tqdm(directory_path_list):
        #     file_path_list = glob.glob(os.path.join(directory_path, '*.json'))
        #     for file_path in file_path_list:
        #         json_file = open(file_path)
        #         asset = json.load(json_file)
        #         self.write_annotation_path_label(asset)

    # ../../annotation_data 内のjsonファイルから座標を記録する
    def write_annotation_path_text(self, asset):
        file_name = os.path.splitext(asset['asset']['name'])[0]
        with open('./input/billboard_{}/ground-truth/{}.txt'.format(self.label_name, file_name), 'w',
                  encoding='utf-8') as text_file:
            for region in asset['regions']:
                label = region['tags'][0]
                if label == 'main':
                    label = region['tags'][1]
                x1 = int(region['points'][0]['x'])
                y1 = int(region['points'][0]['y'])
                x2 = int(region['points'][2]['x'])
                y2 = int(region['points'][2]['y'])
                text_file.write('{} {} {} {} {}\n'.format(label, x1, y1, x2, y2))

    # ../../billboard/labels/test 内のテキストファイルから画像を開き、座標を記録する
    def write_annotation_path_image(self, file_path):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        image_path = '../../{}/images/test/{}.jpg'.format(self.task_name, file_name)
        if not os.path.exists(image_path):
            image_path = '../../{}/images/test/{}.JPG'.format(self.task_name, file_name)
        img = cv2.imread(image_path)
        height, width = img.shape[0], img.shape[1]
        with open('./input/billboard_{}/ground-truth/{}.txt'.format(self.label_name, file_name), 'w',
                  encoding='utf-8') as text_file:
            with open(file_path, 'r', encoding='utf-8') as answer_path:
                text_lines = answer_path.readlines()
                for text in text_lines:
                    label_index, x_center, y_center, w, h = text.split(' ')
                    label = self.class_list[int(label_index)]
                    left = int(float(x_center) * width - (float(w) * width) / 2)
                    top = int(float(y_center) * height - (float(h) * height) / 2)
                    right = int(float(x_center) * width + (float(w) * width) / 2)
                    bottom = int(float(y_center) * height + (float(h.replace('\n', '')) * height) / 2)
                    if self.label_name in ['advertiser', 'product']:
                        text_file.write('{} {} {} {} {}\n'.format(int(label_index), left, top, right, bottom))
                    else:
                        text_file.write('{} {} {} {} {}\n'.format(label, left, top, right, bottom))


if __name__ in '__main__':
    class_list, label_name = LabelList.Subway_Media.value
    # advertiser, media, product
    task_name = 'subway_media'

    os.system('rm -rf ./input/billboard_' + label_name + '/ground-truth/*')

    make_ground_truth = MakeGroundTruth(class_list, label_name, task_name)
    make_ground_truth.main()

    # ground_truthとdetect両方に存在しないファイルを削除する. これを回すとground-truthがnullになるので最初だけ回す
    adjust_ground_and_detect(label_name)
