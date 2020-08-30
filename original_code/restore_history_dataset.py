import os
import shutil

from class_list import LabelList
_, label_name = LabelList.ALL.value

original_image_path = '../../billboard/images'
original_label_path = '../../billboard/labels'

for data_type in ['train', 'val', 'test']:
    os.system('mv ../../billboard/images/{}/* ../../billboard/images/'.format(data_type))
    os.system('rm ../../billboard/labels/{}/*'.format(data_type))
    with open('../../billboard/history/random_directory/billboard_{}.txt'.format(data_type), 'r',
              encoding='utf-8') as text_file:
        image_file_path_list = text_file.readlines()
        for image_file_path in image_file_path_list:
            image_file_path = image_file_path.replace('\n', '')
            image_name = os.path.basename(image_file_path)
            text_name = os.path.splitext(os.path.basename(image_file_path))[0] + '.txt'
            text_file_path = '{}/{}/{}'.format(original_label_path, data_type, text_name)

            shutil.move('{}/{}'.format(original_image_path, image_name), image_file_path)
            shutil.copy('{}/{}/{}'.format(original_label_path, label_name, text_name), text_file_path)
