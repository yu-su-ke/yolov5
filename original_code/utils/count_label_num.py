import glob
import json
import os


def prepare_image_label(base_path):
    """annotation_data/[task_name]_annotation 内のラベルをカウントする`

    Args:
        base_path (str): annotation_data/[task_name]_annotation

    Returns:
        dict: 画像に対応したラベルを格納した辞書
        dict: ラベルごとの数を格納した辞

    """
    label_image_dictionary, label_count_dictionary = {}, {}
    directory_path_list = glob.glob(os.path.join(base_path, '*'))
    for directory_path in directory_path_list:
        file_path_list = glob.glob(os.path.join(directory_path, '*.json'))
        for file_path in file_path_list:
            json_file = open(file_path)
            asset = json.load(json_file)
            image_path = asset['asset']['name']
            label = asset['regions'][0]['tags'][0]
            label_image_dictionary[image_path] = label
            if label not in label_count_dictionary.keys():
                label_count_dictionary[label] = 1
            else:
                label_count_dictionary[label] += 1
    return label_image_dictionary, label_count_dictionary


if __name__ == "__main__":
    base_path = '../../../annotation_data/advertiser_annotation'
    label_image_dictionary, label_count_dictionary = prepare_image_label(base_path)
    print(sorted(label_count_dictionary.items(), key=lambda x: x[1], reverse=True))
    