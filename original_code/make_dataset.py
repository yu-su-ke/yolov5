import glob
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

    def main(self):
        image_path_list = glob.glob(os.path.join(self.original_image_path, '*.jpg'))
        random.seed(1)
        random.shuffle(image_path_list)

        self.split_learning_data(image_path_list)

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

    def save_file(self, image_path, data_type, image_name, label_path, text_name):
        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(self.task_name, self.task, data_type)
        with open(save_history_path, 'a', encoding='utf-8') as text_file:
            shutil.move(image_path, '{}/{}/{}'.format(self.original_image_path, data_type, image_name))
            shutil.copy(label_path, '{}/{}/{}'.format(self.original_label_path, data_type, text_name))
            text_file.write('{}/{}/{}\n'.format(self.original_image_path, data_type, image_name))


if __name__ == '__main__':
    _, label_name = LabelList.ALL.value
    task_name = 'media'
    task = 'random_image'   # historyデータ保存用のパス

    for data_type in ['train', 'val', 'test']:
        os.system('mv ../../{}/images/{}/* ../../{}/images/'.format(task_name, data_type, task_name))
        os.system('rm ../../{}/labels/{}/*'.format(task_name, data_type))

        save_history_path = '../../{}/history/{}/billboard_{}.txt'.format(task_name, task, data_type)
        if os.path.exists(save_history_path):
            print('historyに既に存在します')
            sys.exit()

    make_dataset = MakeDataset(label_name, task_name, task)
    make_dataset.main()