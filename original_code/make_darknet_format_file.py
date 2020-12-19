import argparse
import os
import random

from tqdm import tqdm
from PIL import Image, ImageFile
from urllib.parse import unquote
import yaml

ImageFile.LOAD_TRUNCATED_IMAGES = True

from class_list import LabelList


class MakeDarknetFile:
    def __init__(self, task_name, label_list):
        self.task_name = task_name
        self.label_list = label_list

    def main(self):
        with open('../../{}/model_data/billboard_{}.txt'.format(self.task_name, self.task_name), 'r',
                  encoding='utf-8') as billboard:
            bounding_box_list = billboard.readlines()
            format_image_path_list = self.delete_zero_data(bounding_box_list)
            print('pytorch_yolov3用のテキストファイルを作成する')
            for image_path in tqdm(format_image_path_list):
                # image_list ['image_path', 'x1, y1, x2, y2, label', ...]
                element_list = image_path.split(' ')
                image_name = os.path.splitext(os.path.basename(element_list[0]))[0]
                save_path = '../../{}/labels/{}/{}.txt'.format(self.task_name, self.task_name, image_name)
                self.save_text(save_path, element_list)

    def save_text(self, save_path, element_list):
        """../[task_name]/labels/に保存

        Args:
            save_path (str): テキストファイルの保存パス
            element_list (list): ラベルと座標が格納されたリスト

        """
        # 該当ファイルが既に存在する場合は削除する
        if os.path.exists(save_path):
            os.system('rm ' + save_path)
        with open(save_path, 'w', encoding='utf-8') as save_file:
            for i in range(1, len(element_list)):
                x1, y1, x2, y2, label = element_list[i].split(',')
                x_center, y_center, width, height = self.resize_point(element_list[0], int(x1), int(y1), int(x2),
                                                                      int(y2))
                save_file.write('{} {} {} {} {}\n'.format(label, x_center, y_center, width, height))

    def resize_point(self, image_path, x1, y1, x2, y2):
        """座標をyolo仕様に変更する

        Args:
            image_path (str): 画像パス
            x1 (int): 左上x座標
            y1 (int): 左上y座標
            x2 (int): 右下x座標
            y2 (int): 右下y座標

        Returns:
            list: boundig box の中心のx座標とy座標、幅と高さを格納したリスト

        """
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            img = Image.open(unquote(image_path))
        img_width, img_height = img.size
        width = (x2 - x1) / img_width
        height = (y2 - y1) / img_height
        x_center = x1 / img_width + width / 2
        y_center = y1 / img_height + height / 2

        return [x_center, y_center, width, height]

    # ラベルの無い行を削除する
    def delete_zero_data(self, bounding_box_list):
        """ラベルの無い行を削除する

        Args:
            bounding_box_list list: 画像パスとbounding boxを格納したリスト

        Returns:
            list: ラベルの無い行を削除した bounding_box_list

        """
        print('ラベルの無い行を削除する')
        format_image_path_list = []
        for bounding_box in tqdm(bounding_box_list):
            bounding_box = bounding_box.replace(' \n', '')
            list_element_num = bounding_box.split(' ')
            if len(list_element_num) >= 2:
                format_image_path_list.append(bounding_box)
            else:
                pass
        return format_image_path_list


if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertisr, media, product, ...')
    opt = parser.parse_args()
    task_name = opt.task_name

    with open('./label_name/{}.yaml'.format(task_name)) as f:
        label_list = yaml.safe_load(f)[task_name]

    save_path = '../../{}/labels/{}/'.format(task_name, task_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    os.system('rm {}'.format(os.path.join(save_path, '*')))

    make_darknet_file = MakeDarknetFile(task_name, label_list)
    make_darknet_file.main()
