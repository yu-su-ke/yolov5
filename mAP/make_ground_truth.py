import glob
import json
import os

from tqdm import tqdm

from scripts.extra.intersect_gt_and_dr import adjust_ground_and_detect
from class_list import LabelList


class MakeGroundTruth:
    def __init__(self, label_list, label_name):
        self.base_path = '../../annotation_data/media_annotation/'
        self.label_dictionary = {}

        self.label_list = label_list
        self.label_name = label_name

    def main(self):
        directory_path_list = glob.glob(os.path.join(self.base_path, '*'))
        for directory_path in tqdm(directory_path_list):
            file_path_list = glob.glob(os.path.join(directory_path, '*.json'))
            for file_path in file_path_list:
                json_file = open(file_path)
                asset = json.load(json_file)
                self.write_annotation_path_label(asset)

    def write_annotation_path_label(self, asset):
        file_name = os.path.splitext(asset['asset']['name'])[0]
        with open('./input/billboard_{}/ground-truth/{}.txt'.format(self.label_name, file_name), 'w',
                  encoding='utf-8') as text_file:
            for region in asset['regions']:
                label = region['tags'][0]
                if label == 'main':
                    label = region['tags'][1]
                x1 = int(region['points'][0]['x'])
                y1 = int(region['points'][0]['y'])
                x2 = int(region['points'][2]['x'])
                y2 = int(region['points'][2]['y'])
                text_file.write('{} {} {} {} {}\n'.format(label, x1, y1, x2, y2))


if __name__ in '__main__':
    label_list, label_name = LabelList.ALL.value

    os.system('rm -rf ./input/billboard_' + label_name + '/ground-truth/*')

    make_ground_truth = MakeGroundTruth(label_list, label_name)
    make_ground_truth.main()

    # ground_truthとdetect両方に存在しないファイルを削除する. これを回すとground-truthがnullになるので最初だけ回す
    adjust_ground_and_detect(label_name)