import argparse
import json
import os
import shutil

import yaml


def main(task_name, test_name):
    # label_listの読み込み
    with open('../data/{}.yaml'.format(task_name)) as f:
        label_list = yaml.safe_load(f)['names']

    file_path = '../runs/test/{}/detections_val2017_best_results.json'.format(test_name)
    detection_result_path = './input/{}/detection-results'.format(task_name)
    shutil.rmtree(detection_result_path)
    os.makedirs(detection_result_path)

    json_file = open(file_path)
    asset_list = json.load(json_file)
    for asset in asset_list:
        with open('{}/{}.txt'.format(detection_result_path, asset['image_id']), 'a', encoding='utf-8') as text_file:
            if task_name in ['advertiser', 'product']:
                label = asset['category_id']
            else:
                label = label_list[asset['category_id'] - 1]
            bbox = [str(int(i)) for i in asset['bbox']]
            text_file.write('{} {} {}\n'.format(label, asset['score'], ' '.join(bbox)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-name', required=True, type=str, help='ex. advertiser, media, product, ...')
    parser.add_argument('--test-name', required=True, type=str, help='ex. billboard_advertiser_random_label_5x')
    opt = parser.parse_args()
    task_name, test_name = opt.task_name, opt.test_name

    main(task_name, test_name)