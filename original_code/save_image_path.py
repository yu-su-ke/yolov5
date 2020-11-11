import glob
import json
import os

from class_list import LabelList


class ConfirmAnnotation:
    def __init__(self, label_list, label_name, task_name):
        self.label_list = label_list
        self.label_name = label_name
        self.task_name = task_name

        self.base_path = '../../annotation_data/{}_annotation/'.format(self.task_name)
        self.label_dictionary = {}

        self.label_count_dictionary = {}

    def main(self):
        directory_path_list = glob.glob(os.path.join(self.base_path, '*'))
        with open('../../{}/model_data/billboard_{}.txt'.format(self.task_name, self.label_name), 'w', encoding='utf-8') as text_file:
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
                    self.count_label(asset, image_path)
        print(sorted(self.label_dictionary.items(), key=lambda x: x[1], reverse=True))
        # class_list.py用のクラスの確認
        print(sorted(self.label_dictionary.keys()))

    def write_annotation_path_label(self, asset, image_path, text_file):
        """trainデータのためのファイルパスの記録

        Args:
            asset (dict):
            image_path (str):
            text_file (file):

        Returns: None

        """
        # print(image_path)

        # label = asset['regions'][0]['tags'][0]
        # if label not in self.label_count_dictionary.keys():
        #     self.label_count_dictionary[label] = 1
        # else:
        #     print(label, self.label_count_dictionary[label])
        #     self.label_count_dictionary[label] += 1
        # if self.label_count_dictionary[label] > 30:
        #    return

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

    # ラベルを数字にコンバート
    def convert_label(self, tags):
        """media用の関数

        Args:
            tags (list): アノテーションにつけられたラベル

        Returns:
            int: ラベルをインデックスに変換

        """
        label = tags[0]
        if label in self.label_list:
            return self.label_list.index(label)
        elif label == 'main':
            if label in self.label_list:
                return self.label_list.index(tags[1])
            else:
                pass
        elif self.label_list[0] == 'billboard':
            return 0
        else:
            pass

    # def convert_label(self, tags):
    #     """advertiser, product用の仮関数
    #
    #     Args:
    #         tags (list): アノテーションにつけられたラベル
    #
    #     Returns:
    #         int: ラベルをインデックスに変換
    #
    #     """
    #     if 'main' in tags:
    #         return None
    #     else:
    #         label = tags[0]
    #         if label in self.label_list:
    #             return self.label_list.index(label)
    #         elif label == 'main':
    #             if label in self.label_list:
    #                 return self.label_list.index(tags[1])
    #         else:
    #             pass

    def count_label(self, asset, image_path):
        """アノテーションデータの各ラベルの総数を確認

        Args:
            asset (dict):
            image_path (str):

        Returns:

        """
        for region in asset['regions']:
            label = region['tags'][0]
            if label == 'main':
                try:
                    label = region['tags'][1]
                except IndexError:
                    print('エラーが起きたファイルがあります' + image_path)
                    pass
            if label not in self.label_dictionary:
                self.label_dictionary[label] = 1
            else:
                self.label_dictionary[label] += 1


if __name__ in '__main__':
    label_list, label_name = LabelList.Subway_Media.value
    task_name = 'subway_media'

    print(label_list, label_name)
    ca = ConfirmAnnotation(label_list, label_name, task_name)
    ca.main()
