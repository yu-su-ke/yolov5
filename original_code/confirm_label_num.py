import os

from class_list import LabelList

classes, label_name = LabelList.Subway_Media.value

label_count_dictionary = {}
text_path = '/home/mokky/Program/subway_media/model_data/billboard_subway_media.txt'
with open(text_path, 'r', encoding='utf-8') as text_file:
    text_lines = text_file.readlines()
for text_line in text_lines:
    element_list = text_line.split(' ')
    point_list = element_list[1:-1]
    for point in point_list:
        point = point.split(',')
        label = classes[int(point[-1])]
        if label not in label_count_dictionary.keys():
            label_count_dictionary[label] = 1
        else:
            label_count_dictionary[label] += 1
print(label_count_dictionary)
