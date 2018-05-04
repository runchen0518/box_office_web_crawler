#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: python 2.7.13
# @author: baorunchen(runchen0518@gmail.com)
# @date: 2018/5/3
import re
import time

import urllib2

import os

from PIL import Image
from pytesseract import pytesseract

box_office_website_homepage_url = 'http://58921.com'
box_office_website_url = 'http://58921.com/alltime'
test_url = 'test_url'


def run_log(log):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '-', log


def get_page_data_from_url(url):
    run_log('now get page date from url: %s' % url)

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e1:
        run_log('HTTPError! get page failed, reason: %s' % e1.message)
        exit(-2)
    except urllib2.URLError, e2:
        if hasattr(e2, 'code'):
            run_log('URLError! get page failed, reason: %s' % e2.code)
        if hasattr(e2, 'reason'):
            run_log('URLError! get page failed, reason: %s' % e2.reason)
        exit(-3)
    except ValueError, e3:
        run_log('ValueError! get page failed, reason: %s' % e3.message)
        exit(-4)

    data = response.read()

    if not data.strip():
        run_log('page is null!')
        exit(-5)

    run_log('get page success!')
    return data


def process(page_data, offline_path):
    run_log('get data from page...')

    offline_html_path = offline_path + '/' + 'page' + '.html'
    with open(offline_html_path, 'wb') as f:
        f.write(page_data)
    run_log('write page to path: %s' % offline_html_path)

    pattern = re.compile('<div class="table-responsive.*?>(.*?)</div>', re.S)
    result = re.search(pattern, page_data)
    if result:
        process_data(result.group(1).strip())
    else:
        run_log('data matching failed...')
        exit(-6)


def process_data(raw_data):
    # run_log(raw_data)
    # pattern = re.compile('<a href=.*?>(.*?)</a>', re.S)
    pattern = re.compile('<a href=(.*?) title=(.*?)>(.*?)</a>', re.S)
    # result = re.search(pattern, raw_data)
    # if result:
    #     film_name = result.group(2).strip('\"')
    #     film_url = box_office_website_homepage_url + result.group(1).strip('\"')
    #     write_data(film_name, film_url)
    # else:
    #     run_log('raw data matching failed...')
    #     exit(-7)
    items = re.findall(pattern, raw_data)
    for item in items:
        film_name = item[1].strip('\"')
        if film_name == '数据纠错':
            continue

        film_url = box_office_website_homepage_url + item[0].strip('\"')
        write_data(film_name, film_url)


def write_data(film, url):
    # run_log(film + '\t' + url)
    with open('data.txt', 'a+') as f:
        f.write(film + '\t' + url + '\n')


def process_title(page_data):
    run_log('process with title...')

    pattern = re.compile('<table class=".*?>(.*?)</table>', re.S)
    result = re.search(pattern, page_data)
    if result:
        write_title(result.group(1).strip())
    else:
        run_log('title matching failed...')
        exit(-8)


def write_title(raw_data):
    pattern = re.compile('<th>.*?</th>', re.S)
    items = re.findall(pattern, raw_data)
    for item in items:
        title = item.strip('<th>').strip('</th>')
        with open('data.txt', 'a+') as f:
            f.write(title + '\t')

    with open('data.txt', 'a+') as f:
        f.write('\n')


def image_recognition(path):
    if not os.path.exists(path):
        run_log('pic not exists!')
        return ''
    im = Image.open(path)
    data = pytesseract.image_to_string(im)
    run_log(data)
    return data


def main():
    # create offline html directory
    local_page_path = 'offline_web_page'
    offline_page_dir_path = os.getcwd() + '/' + local_page_path
    if not os.path.isdir(offline_page_dir_path):
        os.makedirs(offline_page_dir_path)
        run_log('make directory, path: %s' % offline_page_dir_path)

    # process_title(get_page_data_from_url(url))
    url_list = [box_office_website_url]

    for i in range(1, 10):
        url_list.append(box_office_website_url + '?page=%d' % i)

    for url in url_list:
        page_data = get_page_data_from_url(url)
        process(page_data, offline_page_dir_path)


if __name__ == '__main__':
    main()
