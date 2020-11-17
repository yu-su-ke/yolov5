import json
import os
import shutil

from class_list import LabelList
class_list, label_name = LabelList.Subway_Media.value


file_path = '../runs/test/billboard_subway_media_random_image_5x/detections_val2017_best_results.json'
detection_result_path = './input/billboard_{}/detection-results'.format(label_name)
shutil.rmtree(detection_result_path)
os.makedirs(detection_result_path)

json_file = open(file_path)
asset_list = json.load(json_file)

save_result_lines = []
for asset in asset_list:
    with open('{}/{}.txt'.format(detection_result_path, asset['image_id']), 'a', encoding='utf-8') as text_file:
        label = class_list[asset['category_id'] - 1]
        bbox = [str(int(i)) for i in asset['bbox']]
        text_file.write('{} {} {}\n'.format(label, asset['score'], ' '.join(bbox)))
