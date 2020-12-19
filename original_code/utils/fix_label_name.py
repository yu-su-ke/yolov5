import glob
import os

test = glob.glob(os.path.join('/home/mokky/Program/annotation_data/advertiser_annotation/22_C_Apple_Japan', '*.json'))

for t in test:
    with open(t, 'r', encoding='utf-8') as f:
        data_lines = f.read()
    data_lines = data_lines.replace('チョーヤ梅酒株式会社,', 'チョーヤ梅酒株式会社')
    with open(t, mode="w", encoding="utf-8") as f:
        f.write(data_lines)