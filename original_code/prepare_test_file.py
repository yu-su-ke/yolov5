import glob
import os
import shutil


task = 'advertiser'

test_image_path = glob.glob('/home/mokky/Program/advertisement/attribute_classification/{}_dataset/test/*/*'.format(task))
for test_image in test_image_path:
    shutil.copy(test_image, '/home/mokky/Program/{}/images/split_test'.format(task))
