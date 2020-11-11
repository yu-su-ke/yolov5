import os
import shutil

from tqdm import tqdm

from class_list import LabelList


_, label_name = LabelList.Subway_Media.value
# advertiser, media, product
task_name = 'subway_media'

original_image_path = '../../{}/images'.format(task_name)
original_label_path = '../../{}/labels'.format(task_name)

for data_type in tqdm(['train', 'val', 'test']):
    os.system('mv ../../{}/images/{}/* ../../{}/images/'.format(task_name, data_type, task_name))
    os.system('rm ../../{}/labels/{}/*'.format(task_name, data_type))

for data_type in tqdm(['train', 'val', 'test']):
    with open('../../{}/history/random_image/billboard_{}.txt'.format(task_name, data_type), 'r',
              encoding='utf-8') as text_file:
        image_file_path_list = text_file.readlines()
        for image_file_path in image_file_path_list:
            image_file_path = image_file_path.replace('\n', '')
            image_name = os.path.basename(image_file_path)
            text_name = os.path.splitext(os.path.basename(image_file_path))[0] + '.txt'
            text_file_path = '{}/{}/{}'.format(original_label_path, data_type, text_name)

            shutil.move('{}/{}'.format(original_image_path, image_name), image_file_path)
            shutil.copy('{}/{}/{}'.format(original_label_path, label_name, text_name), text_file_path)
