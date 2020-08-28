import os

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def make_detection_results(point, image, label, conf, cfg):
    save_name = os.path.splitext(os.path.basename(cfg))[0]
    left, top, right, bottom = int(point[0]), int(point[1]), int(point[2]), int(point[3])
    save_path = './mAP/input/' + save_name + '/detection-results/' + \
                os.path.splitext(os.path.basename(image))[0] + \
                '.txt'    # 保存するパス

    # print(save_path)
    with open(save_path, 'a+', encoding='utf-8') as detection_results:
        detection_results.write('{} {} {} {} {} {}'.format(label, conf, left, top, right, bottom))
        detection_results.write('\n')
