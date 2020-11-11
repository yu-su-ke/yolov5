import glob
import json
import os
import random
import shutil
import sys

from tqdm import tqdm

from class_list import LabelList


class MakeDataset:
    def __init__(self, label_name, task_name, task):
        self.label_name = label_name
        self.task_name = task_name
        self.task = task

        self.original_image_path = '../../{}/images'.format(self.task_name)
        self.original_label_path = '../../{}/labels'.format(self.task_name)
        self.count = 1

        # ラベルカウントの準備
        self.base_path = '../../annotation_data/{}_annotation/'.format(self.task_name)
        self.label_image_dictionary, self.label_count_dictionary = self.prepare_image_label()
        self.label_count = {}

    def main(self):
        image_path_list = glob.glob(os.path.join(self.original_image_path, '*.jpg'))
        test = glob.glob(os.path.join(self.original_image_path, '*.JPG'))
        image_path_list += test
        random.seed(1)
        random.shuffle(image_path_list)

        print(self.label_image_dictionary, self.label_count_dictionary)
        # 媒体用
        # self.split_learning_data(image_path_list)
        # 企業名、商品名用
        # self.split_advertiser_product_data(image_path_list)

    def split_learning_data(self, image_path_list):
        file_count = len(image_path_list)
        for image_path in image_path_list:
            image_name = os.path.basename(image_path)
            text_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
            label_path = '{}/{}/{}'.format(self.original_label_path, self.label_name, text_name)

            if self.count <= file_count * 0.6:
                self.save_file(image_path, 'train', image_name, label_path, text_name)
                self.count += 1
            elif file_count * 0.6 < self.count <= file_count * 0.8:
                self.save_file(image_path, 'val', image_name, label_path, text_name)
                self.count += 1
            elif self.count > file_count * 0.8:
                self.save_file(image_path, 'test', image_name, label_path, text_name)
                self.count += 1

    def split_advertiser_product_data(self, image_path_list):
        for image_path in image_path_list:
            image_name = os.path.basename(image_path)
            text_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
            label_path = '{}/{}/{}'.format(self.original_label_path, self.label_name, text_name)

            target_label = self.label_image_dictionary[image_name]
            if target_label not in self.label_count.keys():
                self.label_count[target_label] = 1
            else:
                self.label_count[target_label] += 1

            if self.label_count[target_label] <= self.label_count_dictionary[target_label] * 0.6:
                self.save_file(image_path, 'train', image_name, label_path, text_name)
            elif self.label_count_dictionary[target_label] * 0.6 < self.label_count[target_label] <= self.label_count_dictionary[target_label] * 0.8:
                self.save_file(image_path, 'val', image_name, label_path, text_name)
            elif self.label_count[target_label] > self.label_count_dictionary[target_label] * 0.8:
                self.save_file(image_path, 'test', image_name, label_path, text_name)

    def save_file(self, image_path, data_type, image_name, label_path, text_name):
        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(self.task_name, self.task, data_type)
        try:
            with open(save_history_path, 'a', encoding='utf-8') as text_file:
                shutil.move(image_path, '{}/{}/{}'.format(self.original_image_path, data_type, image_name))
                shutil.copy(label_path, '{}/{}/{}'.format(self.original_label_path, data_type, text_name))
                text_file.write('{}/{}/{}\n'.format(self.original_image_path, data_type, image_name))
        except FileNotFoundError:
            pass

    def prepare_image_label(self):
        label_image_dictionary, label_count_dictionary = {}, {}
        directory_path_list = glob.glob(os.path.join(self.base_path, '*'))
        for directory_path in directory_path_list:
            file_path_list = glob.glob(os.path.join(directory_path, '*.json'))
            for file_path in file_path_list:
                json_file = open(file_path)
                asset = json.load(json_file)
                image_path = asset['asset']['name']
                label = asset['regions'][0]['tags'][0]
                label_image_dictionary[image_path] = label
                if label not in label_count_dictionary.keys():
                    label_count_dictionary[label] = 1
                else:
                    label_count_dictionary[label] += 1
        return label_image_dictionary, label_count_dictionary


if __name__ == '__main__':
    _, label_name = LabelList.Subway_Media.value
    task_name = 'subway_media'
    task = 'random_directory'   # historyデータ保存用のパス

    for data_type in ['train', 'val', 'test']:
        os.system('mv ../../{}/images/{}/* ../../{}/images/'.format(task_name, data_type, task_name))
        os.system('rm ../../{}/labels/{}/*'.format(task_name, data_type))

        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(task_name, task, data_type)
        if os.path.exists(save_history_path):
            print('historyに既に存在します')
            sys.exit()
        else:
            os.makedirs('../../{}/images/{}/'.format(task_name, data_type), exist_ok=True)
            os.makedirs('../../{}/labels/{}/'.format(task_name, data_type), exist_ok=True)
            os.makedirs('../../{}/history/{}/'.format(task_name, task), exist_ok=True)

    make_dataset = MakeDataset(label_name, task_name, task)
    make_dataset.main()
