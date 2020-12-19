import argparse
import itertools
import os
import shutil

import glob
from tqdm import tqdm
from urllib.parse import quote

from utils import get_label_list


def main(image_directory, save_directory):
    image_dir_list = glob.glob(image_directory + '/**/')
    pattern = ['*.jpg', '*.JPG', '*.png', '*.PNG']
    print('フォルダリストを取得します')
    for directory in image_dir_list:
        image_files = [glob.glob(directory + i) for i in pattern]
        image_files = list(itertools.chain.from_iterable(image_files))
        directory_name, _ = os.path.split(image_files[0])
        print(directory_name + '内の画像を変換中')
        for image_path in tqdm(image_files):
            # subway_mediaのときだけ使う
            # image_name = quote(os.path.basename(image_path))
            # shutil.copy(image_path, save_directory+image_name)

            shutil.copy(image_path, save_directory)


if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertisr, media, product, ...')

    opt = parser.parse_args()
    task_name = opt.task_name

    image_directory = '../../annotation_data/{}_annotation/'.format(task_name)
    save_directory = '../../{}/images/'.format(task_name)
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    os.system('rm ../../{}/images/*'.format(task_name))

    main(image_directory, save_directory)

    # labelのリストを取得
    get_label_list.main(task_name, image_directory)
