#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: python 2.7.13
# @author: baorunchen(runchen0518@gmail.com)
# @date: 2018/5/4
import os

import time
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

pic_path = '/Users/baorunchen/Desktop/test.png'


def run_log(log):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '-', log


def image_recognition(path):
    if not os.path.exists(path):
        run_log('pic not exists!')
        return ''
    im = Image.open(path)
    data = pytesseract.image_to_string(im)
    run_log(data)
    return data


def main():
    if not os.path.exists(pic_path):
        run_log('pic not exists!')
        exit(-1)

    image_recognition(pic_path)


if __name__ == '__main__':
    main()
