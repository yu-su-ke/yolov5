import glob
import json
import os

from pytorch_yolov3 import class_list


class ConfirmAnnotation:
    def __init__(self, label_list, label_name):
        self.base_path = '../../annotation_data/'
        self.label_dictionary = {}

        self.learn_label_type = label_list
        self.file_name = label_name

    def main(self):
        directory_path_list = glob.glob(os.path.join(self.base_path, '*'))
        with open('./billboard/model_data/billboard_' + self.file_name + '.txt', 'w', encoding='utf-8') as text_file:
            for directory_path in directory_path_list:
                # パスの半角スペースを_に変換
                new_directory_path = directory_path.replace(' ', '_')
                os.rename(directory_path, new_directory_path)
                file_path_list = glob.glob(os.path.join(new_directory_path, '*.json'))
                for file_path in file_path_list:
                    json_file = open(file_path)
                    asset = json.load(json_file)
                    image_path = os.path.join(new_directory_path, asset['asset']['name'])

                    self.write_annotation_path_label(asset, image_path, text_file)
                    self.count_label(asset, image_path)
        print(sorted(self.label_dictionary.items(), key=lambda x: x[1], reverse=True))

    # trainデータのためのファイルパスの記録
    def write_annotation_path_label(self, asset, image_path, text_file):
        # print(image_path)
        text_file.write('.' + image_path + ' ')
        for region in asset['regions']:
            label = self.convert_label(region['tags'])
            if label is None:
                continue
            x1 = int(region['points'][0]['x'])
            y1 = int(region['points'][0]['y'])
            x2 = int(region['points'][2]['x'])
            y2 = int(region['points'][2]['y'])
            text_file.write('{},{},{},{},{} '.format(x1, y1, x2, y2, label))
        text_file.write('\n')

    # ラベルを数字にコンバート
    def convert_label(self, tags):
        label = tags[0]
        if label in self.learn_label_type:
            return self.learn_label_type.index(label)
        elif label == 'main':
            if label in self.learn_label_type:
                return self.learn_label_type.index(tags[1])
            else:
                pass
        elif self.learn_label_type[0] == 'billboard':
            return 0
        else:
            pass

    # アノテーションデータの各ラベルの総数を確認
    def count_label(self, asset, image_path):
        for region in asset['regions']:
            label = region['tags'][0]
            if label == 'main':
                try:
                    label = region['tags'][1]
                except IndexError:
                    print('エラーが起きたファイルがあります' + image_path)
                    pass
            if label not in self.label_dictionary:
                self.label_dictionary[label] = 1
            else:
                self.label_dictionary[label] += 1


if __name__ in '__main__':
    label_list, label_name = class_list.LabelList.ONE.value
    print(label_list, label_name)
    ca = ConfirmAnnotation(label_list, label_name)
    ca.main()
