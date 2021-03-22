import argparse
import os
import shutil

from tqdm import tqdm


def main(task_name, history_task):
    original_image_path = '../../{}/images'.format(task_name)
    original_label_path = '../../{}/labels'.format(task_name)

    for data_type in tqdm(['train', 'val', 'test']):
        os.system('mv ../../{}/images/{}/* ../../{}/images/'.format(task_name, data_type, task_name))
        os.system('rm ../../{}/labels/{}/*'.format(task_name, data_type))

    for data_type in tqdm(['train', 'val', 'test']):
        with open('../../{}/history/{}/billboard_{}.txt'.format(task_name, history_task, data_type), 'r',
                encoding='utf-8') as text_file:
            image_file_path_list = text_file.readlines()
            for image_file_path in image_file_path_list:
                image_file_directory = os.path.dirname(image_file_path)
                text_file_directory = '{}/{}'.format(original_label_path, data_type)
                if not os.path.exists(image_file_directory) or not os.path.exists(text_file_directory):
                    os.makedirs(image_file_directory, exist_ok=True)
                    os.makedirs(text_file_directory, exist_ok=True)
                image_file_path = image_file_path.replace('\n', '')
                image_name = os.path.basename(image_file_path)
                text_name = os.path.splitext(os.path.basename(image_file_path))[0] + '.txt'
                text_file_path = '{}/{}'.format(text_file_directory, text_name)

                try:
                    shutil.move('{}/{}'.format(original_image_path, image_name), image_file_path)
                    shutil.copy('{}/{}/{}'.format(original_label_path, task_name, text_name), text_file_path)
                except FileNotFoundError:
                    print(data_type)
                    print(image_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertiser, media, product, ...')
    parser.add_argument('--history-task', required=True, type=str, help='ex. random_directory, ...')

    opt = parser.parse_args()
    task_name, history_task = opt.task_name, opt.history_task
    main(task_name, history_task)