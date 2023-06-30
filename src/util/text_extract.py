import re
import json
import pandas as pd
from ecloud import CMSSEcloudOcrClient
from py_pdf_parser.loaders import load_file

'''[elements, points, group]'''
'''[[bounding, center, text], [center, text], []]'''

point_density = 6
# pdf config

# img config
access_key = 'c89dccb76c114611a16f17c519f962d4'
secret_key = '092a0f411cc5478696c5dd351c93fff0'
url = 'https://api-wuxi-1.cmecloud.cn:8443'


def pdf_extract(filename):
    elements = pd.DataFrame()
    points = pd.DataFrame()
    counter = 0
    index = 0

    pdf = load_file(filename)

    raw_elements = pdf.elements
    for item in raw_elements:
        if re.search(pattern=r'[\w\u4e00-\u9fa5.@]', string=item.text()) is None:
            continue
        element = pd.DataFrame({
            'index': [index],
            'text': [re.sub(pattern='[\n ]', repl='', string=item.text())],
            'point': [counter],
            'width': [item.bounding_box.width],
            'height': [item.bounding_box.height],
            'x_0': [item.bounding_box.x0],
            'y_0': [item.bounding_box.y0],
            'x_1': [item.bounding_box.x1],
            'y_1': [item.bounding_box.y1],
            'x_c': [(item.bounding_box.x0 + item.bounding_box.x1) / 2],
            'y_c': [(item.bounding_box.y0 + item.bounding_box.y1) / 2],
        })
        elements = pd.concat([elements, element], ignore_index=True)

        for x in range(int(item.bounding_box.x0), int(item.bounding_box.x1), point_density):
            for y in range(int(item.bounding_box.y0), int(item.bounding_box.y1), point_density):
                point = pd.DataFrame({
                    'index': [counter],
                    'element': [index],
                    'x': [x],
                    'y': [y]
                })
                points = pd.concat([points, point], ignore_index=True)
                counter += 1
        index += 1
    return elements, points
    # elements = []
    # points = []
    # group_idx = []
    # counter = 0
    # index = 0
    #
    # pdf = load_file(filename)
    #
    # raw_elements = pdf.elements
    # for item in raw_elements:
    #     group_idx.append(counter)
    #
    #     elements.append({
    #         'bounding': item.bounding_box,
    #         'center': [(item.bounding_box.x0 + item.bounding_box.x1) / 2,
    #                    (item.bounding_box.y0 + item.bounding_box.y1) / 2],
    #         'text': re.sub(pattern='[\n ]', repl='', string=item.text()),
    #         'index': index
    #     })
    #     index += 1
    #
    #     for width in range(int(item.bounding_box.x0), int(item.bounding_box.x1), point_density):
    #         for height in range(int(item.bounding_box.y0), int(item.bounding_box.y1), point_density):
    #             points.append([width, height])
    #             counter += 1
    # return elements, points, group_idx

def img_extract(filename):
    elements = pd.DataFrame()
    points = pd.DataFrame()
    counter = 0
    index = 0

    request_url = '/api/ocr/v1/webimage'
    options = {
        'box_layout': True,
        'enable_table': True
    }

    try:
        ocr_client = CMSSEcloudOcrClient(access_key, secret_key, url)
        response = ocr_client.request_ocr_service_file(requestpath=request_url, imagepath=filename, options=options)
        for item in json.JSONDecoder().decode(response.text)['body']['content']['prism_wordsInfo']:
            # 避免只有装饰性字符体积过小的元素 无法产生 points
            if re.search(pattern=r'[\w\u4e00-\u9fa5.@]', string=item['word']) is None:
                continue
            element = pd.DataFrame({
                'index': [index],
                'text': [re.sub(pattern='[\n ]', repl='', string=item['word'])],
                'point': [counter],
                'width': [item['position'][2]['x'] - item['position'][0]['x']],
                'height': [item['position'][2]['y'] - item['position'][0]['y']],
                'x_0': [item['position'][2]['x']],
                'y_0': [-item['position'][2]['y']],
                'x_1': [item['position'][0]['x']],
                'y_1': [-item['position'][0]['y']],
                'x_c': [(item['position'][2]['x'] + item['position'][0]['x']) / 2],
                'y_c': [-(item['position'][2]['y'] + item['position'][0]['y']) / 2],
            })
            elements = pd.concat([elements, element], ignore_index=True)

            bounding = [list(item['position'][2].values()), list(item['position'][0].values())]
            for x in range(int(bounding[0][0]), int(bounding[1][0]), point_density):
                for y in range(int(bounding[0][1]), int(bounding[1][1]), point_density):
                    point = pd.DataFrame({
                        'index': [counter],
                        'element': [index],
                        'x': [x],
                        'y': [-y]
                    })
                    points = pd.concat([points, point], ignore_index=True)
                    counter += 1
            index += 1
        return elements, points
    except ValueError as e:
        print(e)

        # elements = []
        # points = []
        # counter = 0
        # index = 0
        #
        # request_url = '/api/ocr/v1/webimage'
        # options = {
        #     'box_layout': True,
        #     'enable_table': True
        # }
        #
        # try:
        #     ocr_client = CMSSEcloudOcrClient(access_key, secret_key, url)
        #     response = ocr_client.request_ocr_service_file(requestpath=request_url, imagepath=filename, options=options)
        #     for item in json.JSONDecoder().decode(response.text)['body']['content']['prism_wordsInfo']:
        #         group_idx.append(counter)
        #
        #         bounding = [list(item['position'][2].values()), list(item['position'][0].values())]
        #         x_center = (item['position'][2]['x'] + item['position'][0]['x']) / 2
        #         y_center = (item['position'][2]['y'] + item['position'][0]['y']) / 2
        #         center = [x_center, y_center]
        #         text = item['word']
        #         elements.append({
        #             'bounding': bounding,
        #             'center': center,
        #             'text': text,
        #             'index': index
        #         })
        #         index += 1
        #
        #         for width in range(int(bounding[0][0]), int(bounding[1][0]), point_density):
        #             for height in range(int(bounding[0][1]), int(bounding[1][1]), point_density):
        #                 points.append([width, -height])
        #                 counter += 1
        #     return elements, points, group_idx
        # except ValueError as e:
        #     print(e)

