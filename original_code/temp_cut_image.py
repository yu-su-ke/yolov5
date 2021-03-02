import os

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import cv2


def cut_image(detection_image_point_list, source, image_name):
    """検出された看板広告を切り出す

    Args:
        detection_image_point_list (list): 画像中から検出した座標リスト
        source (str): ターゲット画像ディレクトリ
        image_name (str): ターゲット画像れい

    Returns: None

    """
    # x1, y1, x2, y2 = calculate_max_area(detection_image_point_list)
    count = 0
    for detection_image_point in detection_image_point_list:
        x1, y1, x2, y2 = detection_image_point
        im0 = cv2.imread(os.path.join(source, image_name + '.jpg'))
        img1 = im0[y1: y2, x1: x2]
        save_directory = './inference/trimming_image/' + os.path.basename(source)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        cv2.imwrite('{}/{}_{}.jpg'.format(save_directory, image_name, count), img1)
        count += 1


def calculate_max_area(detection_image_point_list):
    """複数の検出範囲の中から最も面積の大きいものを代表とする

    Args:
        detection_image_point_list (list): 検出座標リスト

    Returns:
        list: 最も面積の広い検出範囲

    """
    max_detection_area = 0
    max_detection_point_list = []
    for detection_image_point in detection_image_point_list:
        x1, y1, x2, y2 = detection_image_point
        temp_detection_area = (x2 - x1) * (y2 - y1)
        if temp_detection_area > max_detection_area:
            max_detection_area = temp_detection_area
            max_detection_point_list = [x1, y1, x2, y2]

    return max_detection_point_list
