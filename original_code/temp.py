import os 
import glob

from tqdm import tqdm


original_path = '/home/mokky/Program/subway_media/labels'
for task in ['train', 'val', 'test']:
    file_list = glob.glob(os.path.join(original_path, task, '*'))
    for i in tqdm(file_list):
        file_name = os.path.basename(i)
        with open(i, 'r') as text_file:
            text_lines = text_file.readlines()
        save_text = ''
        for text_line in text_lines:
            element_list = text_line.split(' ')
            if int(element_list[0]) == 4:
                element_list[0] = '7'
            elif int(element_list[0]) == 5:
                element_list[0] = '10'
            elif int(element_list[0]) == 6:
                element_list[0] = '11'
            # if int(element_list[0]) == 0:
            #     element_list[0] = '2'
            # elif int(element_list[0]) == 1:
            #     element_list[0] = '4'
            # elif int(element_list[0]) == 2:
            #     element_list[0] = '5'
            # elif int(element_list[0]) == 3:
            #     element_list[0] = '6'
            # elif int(element_list[0]) == 4:
            #     element_list[0] = '7'
            # elif int(element_list[0]) == 5:
            #     element_list[0] = '8'
            # elif int(element_list[0]) == 6:
            #     element_list[0] = '9'
            # elif int(element_list[0]) == 7:
            #     element_list[0] = '12'
            # elif int(element_list[0]) == 8:
            #     element_list[0] = '13'
            # elif int(element_list[0]) == 9:
            #     element_list[0] = '14'
            save_text += '{}'.format(' '.join(element_list))
        with open('/home/mokky/Program/all_media/labels/{}/{}'.format(task, file_name), 'w', encoding='utf-8') as save_file:
            save_file.write(save_text)
