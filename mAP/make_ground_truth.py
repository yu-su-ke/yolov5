import argparse
import glob
import json
import os
import shutil

import cv2
from tqdm import tqdm
import yaml

from scripts.extra.intersect_gt_and_dr import adjust_ground_and_detect
from class_list import LabelList


class MakeGroundTruth:
    """
    model_data/ 内のファイルからground-truthを作る
    """
    def __init__(self, label_list, label_name):
        self.base_path = '../../{}/model_data/billboard_{}.txt'.format(label_name, label_name)
        self.label_dictionary = {}

        self.label_list = label_list
        self.label_name = label_name

    def main(self):
        with open(self.base_path, 'r', encoding='utf-8') as text_file:
            text_lines = text_file.readlines()
        for text_line in text_lines:
            text_line = text_line.replace('\n', '')
            element_list = text_line.split(' ')
            image_path = element_list[0]
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            with open('./input/{}/ground-truth/{}.txt'.format(self.label_name, image_name), 'w',
                      encoding='utf-8') as ground_truth_file:
                point_label_list = element_list[1:-1]
                for point_label in point_label_list:
                    point_label_split = point_label.split(',')
                    point = point_label_split[:4]
                    label = int(point_label_split[4])
                    if task_name in ['advertiser', 'product']:
                        ground_truth_file.write('{} {}\n'.format(label, ' '.join(point)))
                    else:
                        ground_truth_file.write('{} {}\n'.format(self.label_list[label], ' '.join(point)))


if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertiser, media, product, ...')

    opt = parser.parse_args()
    task_name = opt.task_name

    ground_truth_path = './input/{}/ground-truth'.format(task_name)
    shutil.rmtree(ground_truth_path)
    os.makedirs(ground_truth_path)

    # label_listの読み込み
    with open('../data/{}.yaml'.format(task_name)) as f:
        label_list = yaml.safe_load(f)['names']

    make_ground_truth = MakeGroundTruth(label_list, task_name)
    make_ground_truth.main()

    # ground_truthとdetect両方に存在しないファイルを削除する. これを回すとground-truthがnullになるので最初だけ回す
    adjust_ground_and_detect(task_name)
