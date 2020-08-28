import os
import shutil

import glob
from tqdm import tqdm


def main(image_directory, save_directory):
    image_dir_list = glob.glob(image_directory + '/**/')
    pattern = '*.jpg'
    print('フォルダリストを取得します')
    for directory in image_dir_list:
        image_files = glob.glob(directory + pattern)
        directory_name, _ = os.path.split(image_files[0])
        print(directory_name + '内の画像を変換中')
        for image_path in tqdm(image_files):
            shutil.copy(image_path, save_directory)


if __name__ in '__main__':
    image_directory = '../../annotation_data/'
    save_directory = '../../billboard/images/'

    os.system('rm ../../billboard/images/*')

    main(image_directory, save_directory)
