import os
import re
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from src.util.format_tools import cvt2pdf
from src.util.text_extract import pdf_extract, img_extract
from src.util.text_parser import dbscan

FILENAME = '100'
SUFFIX = 'pdf'
INPUT_FOLDER = 'D:/资源/ADriver/pdf/'
# INPUT_PATH = str(Path('../res/' + FILENAME + '.' + SUFFIX).resolve())
INPUT_PATH = str(Path('D:/资源/ADriver/pdf/' + FILENAME + '.' + SUFFIX).resolve())
OUTPUT_CSV = []
OUTPUT_SPLIT = ' '
# INPUT_PATH = str(Path('D:/资源/ADriver/输出/docx/' + FILENAME + '.' + SUFFIX).resolve())
FMT_DICT = {
    # doc
    'doc': 'doc',
    'docx':'doc',
    # img
    'bmp': 'img',
    'jpg': 'img',
    'jpeg':'img',
    'png': 'img',
    # pdf
    'pdf': 'pdf',
    # ppt
    'ppt': 'ppt',
    'pptx':'ppt'
}

PPT_APP = None
WORD_APP = None

EXPORT_TO_FILE = False
TEMP_PATH = str(Path('../res/' + SUFFIX + '_' + FILENAME + '.pdf').resolve())


def file_fmt(path):
    suffix = re.findall(pattern=r'^[a-zA-Z]+\.', string=path[::-1])
    # print('suffix:', suffix)
    # print('suffix[0][:-1:-1]:', suffix[0][::-1][1:])
    if len(suffix) == 0:
        return 'none'
    elif FMT_DICT.__contains__(suffix[0][-2::-1]):
        return FMT_DICT[suffix[0][-2::-1]]
    else:
        return 'none'


def analyse_main():
    global INPUT_PATH, OUTPUT_CSV

    print(f'# %15s:' % 'INPUT_FILE', INPUT_PATH,
          f'\n# %15s:' % 'TEMP_PATH', TEMP_PATH)

    if not os.path.isfile(INPUT_PATH):
        return '#FILE_NOT_EXIST'
    
    fmt = file_fmt(INPUT_PATH)
    elements = []
    points = []
    print(f'# %15s:' % 'FILE_TYPE', fmt, '\n')

    # convert doc/ppt to pdf
    if fmt == 'doc':
        INPUT_PATH = cvt2pdf(INPUT_PATH, 'doc', TEMP_PATH)
        fmt = 'pdf'
        print('# FMT: doc -> pdf', TEMP_PATH)
    elif fmt == 'ppt':
        INPUT_PATH = cvt2pdf(INPUT_PATH, 'ppt', TEMP_PATH)
        fmt = 'pdf'
        print('# FMT: ppt -> pdf', TEMP_PATH)
    else:
        print('# NO NEED TO CONVERT\n')

    # img/pdf text extract
    if os.path.exists(INPUT_PATH):
        if fmt == 'img':
            elements, points = img_extract(INPUT_PATH)
            print('# EXTRACT FROM img')
        elif fmt == 'pdf':
            elements, points = pdf_extract(INPUT_PATH)
            print('# EXTRACT FROM pdf')
        else:
            return '#INVALID_FORMAT'
    print(f'# %15s:' % 'ELEMENTS', len(elements),
          f'\n# %15s:' % 'POINTS', len(points))

    # split to chunk
    if len(elements) + len(points) == 0:
        return '#EMPTY_CONTENT'
    points['c_1'] = dbscan(points)
    elements['c_1'] = points.groupby(by='element')['c_1'].min().values
    print(f'# %15s:' % 'SPLIT TO BLOCK', elements['c_1'].max() + 1)

    # calculate rectangle
    rects = []
    g0 = elements.loc[:, ['c_1', 'x_0', 'y_0']].groupby(by='c_1').min()
    g1 = elements.loc[:, ['c_1', 'x_1', 'y_1']].groupby(by='c_1').max()
    for i in range(points['c_1'].max() + 1):
        x_0, y_0 = g0.iloc[i, :].values
        x_1, y_1 = g1.iloc[i, :].values
        width = x_1 - x_0
        height = y_1 - y_0
        rects.append({
            'xy': (x_0, y_0),
            'width': width,
            'height': height,
        })
    print(f'# %15s:' % 'RECT', len(rects))

    #
    fig = plt.figure(figsize=(6, 8))
    plt.axis('off')
    plt.autoscale(True)
    for rect in rects:
        plt.gca().add_patch(plt.Rectangle(rect['xy'], width=rect['width'], height=rect['height'], alpha=0.3))
    plt.show()

    # export
    _group = elements[['text', 'c_1']].groupby(by='c_1')
    if EXPORT_TO_FILE:
        # text
        with open('../output/' + SUFFIX + '_' + FILENAME + '.txt', 'w+', encoding='utf-8') as f:
            for name, group in _group:
                for item in group.values:
                    f.write(item[0] + OUTPUT_SPLIT)
                    # print(item[0])
                f.write(2*OUTPUT_SPLIT)
        print('# %15s:' % 'TEXT SAVE TO', '../output/' + SUFFIX + '_' + FILENAME + '.txt')
        # rect
        # TODO
        print('# %15s:' % 'RECT SAVE TO', '../output/' + SUFFIX + '_' + FILENAME + '.txt')
        return '#SUCCESS'
    else:
        # text
        str_text = '"'
        for name, group in _group:
            for item in group.values:
                str_text += item[0] + OUTPUT_SPLIT
                # print(item[0])
            str_text += 2*OUTPUT_SPLIT
        str_text += '"'
        OUTPUT_CSV.append([SUFFIX + '_' + FILENAME, str_text])
        # rect
        str_rect = ''
        # TODO
        return str_text, str_rect


def run_single():
    analyse_main()

def run_batch():
    start_s = time.time()
    start_b = time.time()
    end_t = time.time()

    global INPUT_PATH, FILENAME, SUFFIX
    folder_list = [INPUT_FOLDER]
    file_list = []

    while len(folder_list) > 0:
        folder = folder_list.pop()
        for i in os.listdir(folder):
            filename, suffix = os.path.splitext(i)
            if len(suffix) > 0:
                file_list.append(folder + filename + suffix)
            else:
                folder_list.append(folder + filename + '/')
            # print(file_list)
            # print(folder_list)
            # print()

    start_b = time.time()
    for i in range(len(file_list)):
        start_t = time.time()
        file = file_list[i]
        INPUT_PATH = file
        FILENAME, SUFFIX = os.path.splitext(file)
        FILENAME = FILENAME.split('/')[-1]
        SUFFIX = SUFFIX[1:]
        # print(INPUT_PATH, FILENAME, SUFFIX)
        analyse_main()
        end_t = time.time()
        print(f'\033[5;34m# PROGRESS: %4.0f/%4.0f with %3.2fs total %5.2fs\033[0m'
              % (i+1, len(file_list),
                 end_t-start_s,
                 end_t-start_b))

    np.savetxt('../output/resume_text.csv', OUTPUT_CSV, fmt='%s', delimiter=',')

def rubbish_bin():
    pass
    # multi
    # chunk = dbscan_multi(points)
    # layer_1 = [[] for i in range(max(chunk[0]) + 2)]
    # layer_2 = [[] for i in range(max(chunk[1]) + 2)]
    # # layer_3 = [[] for i in range(max(chunk[2]) + 2)]
    # # #
    # for item, idx in zip(elements, groups):
    #     layer_1[chunk[0][idx]].append(item)
    # for items in layer_1:
    #     if len(items) == 0:
    #         continue
    #     index = chunk[1][items[0]['index']]
    #     index = len(layer_2) - 1 if index == -1 else index
    #     layer_2[index].append(items)
    # # for items in layer_2:
    # #     if len(items) == 0:
    # #         continue
    # #     index = chunk[2][items[0][0]['index']]
    # #     index = len(layer_3) - 1 if index == -1 else index
    # #     layer_3[index].append(items)
    # #
    # # for i in layer_3:
    # #     print('----')
    # #     for j in i:
    # #         print('    ----')
    # #         for k in j:
    # #             print('        ----')
    # #             for l in k:
    # #                 print('            ', l['text'])
    # # with open('../output/' + FILENAME.replace('.', '_') + '_multi.txt', 'w+', encoding='utf-8') as f:
    # #         print()
    # #         f.write('\n')


if __name__ == '__main__':
    # run_single()

    run_batch()






