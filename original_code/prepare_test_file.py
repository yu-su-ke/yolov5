import glob
import json
import os
import shutil

import cv2
from tqdm import tqdm


task = 'advertiser'

save_directory = '/home/mokky/Program/{}/images/split_test'.format(task)
if os.path.exists(save_directory):
    shutil.rmtree(save_directory)
os.makedirs(save_directory)

test_image_path = glob.glob('/home/mokky/Program/advertisement/attribute_classification/{}_dataset/test/*/*'.format(task))
for test_image in test_image_path:
    shutil.copy(test_image, '/home/mokky/Program/{}/images/split_test'.format(task))


# test_image_path = glob.glob('/home/mokky/Program/{}/images/test/*'.format(task))
# annotation_image_path = glob.glob('/home/mokky/Program/annotation_data/{}_annotation/**/*.jpg'.format(task))
# for test_image in tqdm(test_image_path):
#     count = 0
#     test_image_name = os.path.basename(test_image)
#     for annotation_image in annotation_image_path:
#         if test_image_name in annotation_image:
#             annotation_dir_name = os.path.dirname(annotation_image)

#     vott_json_export_path = glob.glob(os.path.join(
#         annotation_dir_name, 'vott-json-export', '*.json'))[0]
#     json_open = open(vott_json_export_path, 'r')
#     json_load = json.load(json_open)

#     for annotation_id in json_load['assets']:
#         asset_image_name = json_load['assets'][annotation_id]['asset']['name']
#         if asset_image_name == test_image_name:
#             img = cv2.imread(test_image)
#             regions = json_load['assets'][annotation_id]['regions']
#             for region in regions:
#                 if 'main' in region['tags']:
#                     height, width, left, top = region['boundingBox']['height'], region['boundingBox']['width'], region['boundingBox']['left'], region['boundingBox']['top']
#                     main_img = img[int(top) : int(top + height), int(left) : int(left + width)]
#                     image_name = os.path.splitext(os.path.basename(test_image))[0]
#                     cv2.imwrite('{}/{}_{}.jpg'.format(save_directory, image_name, count), main_img)
#                     count += 1
