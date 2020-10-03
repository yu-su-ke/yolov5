import os
import shutil

with open('../not_detect_image.txt', 'r', encoding='utf-8') as text_file:
    text_lines = text_file.readlines()

for text_line in text_lines:
    text_line = text_line.replace('\n', '')
    shutil.copy(text_line, './test')
