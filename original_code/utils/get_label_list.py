import argparse
import glob
import json

import yaml


def main(task_name, annotation_directory):
    label_list = []
    dir_list = glob.glob(annotation_directory + '/**/')
    for directory in dir_list:
        json_files = glob.glob(directory + '*.json')
        for file_path in json_files:
            json_file = open(file_path)
            asset = json.load(json_file)
            region_list = asset['regions']
            for region in region_list:
                label = region['tags'][0] if region['tags'][0] != 'main' else region['tags'][1]
                if label not in label_list:
                    label_list.append(label)
    save_directory = {
        'train': '../{}/images/train'.format(task_name),
        'val': '../{}/images/val'.format(task_name),
        'test': '../{}/images/test'.format(task_name),
        'nc': len(label_list),
        'names': sorted(label_list)
        }

    with open('../data/{}.yaml'.format(task_name), 'w', encoding='utf-8') as f:
        yaml.dump(save_directory, f, encoding='utf-8', allow_unicode=True)

if __name__ in '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str,
                        help='ex. advertisr, media, product, ...')

    opt = parser.parse_args()
    task_name = opt.task_name

    annotation_directory = '../../../annotation_data/{}_annotation/'.format(task_name)
    main(task_name, annotation_directory)
