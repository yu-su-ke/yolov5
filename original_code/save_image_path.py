import argparse
import glob
import json
import os

import yaml

from utils import count_label_num


class ConfirmAnnotation:
    def __init__(self, task_name, label_list):
        self.task_name = task_name
        self.label_list = label_list

        self.base_path = '../../annotation_data/{}_annotation/'.format(self.task_name)

    def main(self):
        directory_path_list = glob.glob(os.path.join(self.base_path, '*'))
        with open('../../{}/model_data/billboard_{}.txt'.format(self.task_name, self.task_name), 'w', encoding='utf-8') as text_file:
            for directory_path in directory_path_list:
                # パスの半角スペースを_に変換
                new_directory_path = directory_path.replace(' ', '_')
                os.rename(directory_path, new_directory_path)
                file_path_list = glob.glob(os.path.join(new_directory_path, '*.json'))
                for file_path in file_path_list:
                    json_file = open(file_path)
                    asset = json.load(json_file)
                    image_path = os.path.join(new_directory_path, asset['asset']['name'])
                    self.write_annotation_path_label(asset, image_path, text_file)
        _, label_count_dictionary = count_label_num.prepare_image_label(self.base_path)
        print(sorted(label_count_dictionary.items(), key=lambda x: x[1], reverse=True))
        

    def write_annotation_path_label(self, asset, image_path, text_file):
        """trainデータのためのファイルパスの記録

        Args:
            asset (dict):
            image_path (str):
            text_file (file):

        Returns: None

        """
        text_file.write(image_path + ' ')
        for region in asset['regions']:
            label = self.convert_label(region['tags'])
            if label is None:
                continue
            x1 = int(region['points'][0]['x'])
            y1 = int(region['points'][0]['y'])
            x2 = int(region['points'][2]['x'])
            y2 = int(region['points'][2]['y'])
            text_file.write('{},{},{},{},{} '.format(x1, y1, x2, y2, label))
        text_file.write('\n')

    def convert_label(self, tags):
        """ラベルを数字にコンバー数

        Args:
            tags (list): アノテーションにつけられたラベル

        Returns:
            int: ラベルをインデックスに変換

        """
        label = tags[0] if tags[0] != 'main' else tags[1]
        if label in self.label_list:
            return self.label_list.index(label)
        else:
            print('未知のラベルが検出されました : {}'.format(label))


if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertisr, media, product, ...')
    opt = parser.parse_args()
    task_name = opt.task_name

    with open('./label_name/{}.yaml'.format(task_name)) as f:
        label_list = yaml.safe_load(f)[task_name]

    ca = ConfirmAnnotation(task_name, label_list)
    ca.main()
