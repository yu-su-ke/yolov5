import argparse
import glob
import itertools
import json
import os
import random
import shutil
import sys

from tqdm import tqdm

from utils import count_label_num


class MakeDataset:
    def __init__(self, task_name, history_task):
        self.task_name = task_name
        self.history_task = history_task

        self.original_image_path = '../../{}/images'.format(self.task_name)
        self.original_label_path = '../../{}/labels'.format(self.task_name)
        self.count = 1

        # ラベルカウントの準備
        self.base_path = '../../annotation_data/{}_annotation/'.format(self.task_name)
        # 画像に対応したラベルを格納した辞書、ラベルごとの数を格納した辞書
        self.label_image_dictionary, self.label_count_dictionary = count_label_num.prepare_image_label(self.base_path)

    def main(self):
        pattern = ['*.jpg', '*.JPG', '*.png', '*.PNG']
        image_path_list = [glob.glob(os.path.join(self.original_image_path, i)) for i in pattern]
        image_path_list = list(itertools.chain.from_iterable(image_path_list))
        random.seed(1)
        random.shuffle(image_path_list)

        # 媒体用
        # self.split_learning_data(image_path_list)
        # 企業名、商品名用
        self.split_per_directory_data(image_path_list)

    def split_learning_data(self, image_path_list):
        """ラベル毎などを考慮せず、純粋なファイル数だけでデータセットを作る

        主にmedia, subway_media用

        Args:
            image_path_list (str): 画像パスリスト

        """
        file_count = len(image_path_list)
        for image_path in image_path_list:
            image_name = os.path.basename(image_path)
            text_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
            label_path = '{}/{}/{}'.format(self.original_label_path, self.task_name, text_name)

            if self.count <= file_count * 0.6:
                self.save_file('train', image_path, image_name, label_path, text_name)
                self.count += 1
            elif file_count * 0.6 < self.count <= file_count * 0.8:
                self.save_file('val', image_path, image_name, label_path, text_name)
                self.count += 1
            elif self.count > file_count * 0.8:
                self.save_file('test', image_path, image_name, label_path, text_name)
                self.count += 1

    def split_per_directory_data(self, image_path_list):
        """ディレクトリ毎にtrain, val, test比率で分配したデータセットを作る

        主にadvertiser, product用

        Args:
            image_path_list (str): 画像パスリスト

        """
        label_count = {}
        for image_path in image_path_list:
            image_name = os.path.basename(image_path)
            text_name = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
            label_path = '{}/{}/{}'.format(self.original_label_path, self.task_name, text_name)

            target_label = self.label_image_dictionary[image_name]
            if target_label not in label_count.keys():
                label_count[target_label] = 1
            else:
                label_count[target_label] += 1

            if label_count[target_label] <= self.label_count_dictionary[target_label] * 0.6:
                self.save_file('train', image_path, image_name, label_path, text_name)
            elif self.label_count_dictionary[target_label] * 0.6 < label_count[target_label] <= self.label_count_dictionary[target_label] * 0.8:
                self.save_file('val', image_path, image_name, label_path, text_name)
            elif label_count[target_label] > self.label_count_dictionary[target_label] * 0.8:
                self.save_file('test', image_path, image_name, label_path, text_name)

    def save_file(self, data_type, image_path, image_name, label_path, text_name):
        """

        Args:
            data_type (str): train or val or test
            image_path (str): 画像パス
            image_name (str): 画像パスの画像名部分(拡張子含む)
            label_path (str): ラベルパス
            text_name (str): ラベル名(拡張子含む)

        """
        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(self.task_name, self.history_task, data_type)
        try:
            with open(save_history_path, 'a', encoding='utf-8') as text_file:
                shutil.move(image_path, '{}/{}/{}'.format(self.original_image_path, data_type, image_name))
                shutil.copy(label_path, '{}/{}/{}'.format(self.original_label_path, data_type, text_name))
                text_file.write('{}/{}/{}\n'.format(self.original_image_path, data_type, image_name))
        except FileNotFoundError:
            print('ファイルパスが存在しません')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertisr, media, product, ...')
    parser.add_argument('--history-task', required=True, type=str, help='ex. andom_directory, ...')

    opt = parser.parse_args()
    task_name, history_task = opt.task_name, opt.history_task

    for data_type in ['train', 'val', 'test']:
        # train, val, testに既に格納されている画像をimagesに戻す
        os.system('mv ../../{}/images/{}/* ../../{}/images/'.format(task_name, data_type, task_name))
        # train, val, testに既に格納されているテキストファイルを削除する
        os.system('rm ../../{}/labels/{}/*'.format(task_name, data_type))

        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(task_name, history_task, data_type)
        if os.path.exists(save_history_path):
            print('historyに既に存在します')
            sys.exit()
        else:
            os.makedirs('../../{}/images/{}/'.format(task_name, data_type), exist_ok=True)
            os.makedirs('../../{}/labels/{}/'.format(task_name, data_type), exist_ok=True)
            os.makedirs('../../{}/history/{}/'.format(task_name, history_task), exist_ok=True)

    make_dataset = MakeDataset(task_name, history_task)
    make_dataset.main()
