import os
import shutil

with open('../not_detect_image.txt', 'r', encoding='utf-8') as text_file:
    text_lines = text_file.readlines()

shutil.rmtree('./not_detect_test/')
if not os.path.isdir('./not_detect_test/'):
    os.makedirs('./not_detect_test/')

for text_line in text_lines:
    text_line = text_line.replace('\n', '')
    shutil.copy(text_line, './not_detect_test/')
