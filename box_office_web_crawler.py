#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: python 2.7.13
# @author: baorunchen(runchen0518@gmail.com)
# @date: 2018/5/3
import os
import re
import time
import urllib2
from PIL import Image
from pytesseract import pytesseract

box_office_website_homepage_url = 'http://58921.com'
box_office_website_url = 'http://58921.com/alltime'
test_url = 'test_url'
offline_html_dir_name = 'html'


# 打日志专用，封装print，防止python3用户执行前需要大量修改py文件里面的print
def run_log(log):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '-', log


# 请求页面内容
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


# 爬取网页内容并处理
def process(url, offline_path):
    run_log('get data from page...')
    page_data = get_page_data_from_url(url)

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


# 处理离线网页
def process_offline(path):
    html_dir_path = os.getcwd() + '/' + path
    run_log('now get offline html from path: %s' % html_dir_path)

    html_list = os.listdir(html_dir_path)
    html_name_list = []
    for html in html_list:
        html_name = html.strip('.html')
        html_name_list.append(int(html_name))

    html_name_list.sort()
    # run_log(html_name_list)

    for html in html_name_list:
        html_path = html_dir_path + '/%d.html' % html
        run_log('process %s.html...' % html)
        if not os.path.exists(html_path):
            continue

        with open(html_path, 'r') as f:
            html_data = f.read()
            # run_log(html_data)

            pattern = re.compile('<div class="table-responsive.*?>(.*?)</div>', re.S)
            result = re.search(pattern, html_data)
            if result:
                process_data(result.group(1).strip())
            else:
                run_log('offline html data matching failed...')
                exit(-7)

    run_log('success!')


# 提取页面内容
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


# 将电影名称和电影网址写入本地文件
def write_data(film, url):
    with open('data.txt', 'a+') as f:
        f.write('%s\t%s\n' % (film, url))


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


# 识别图片里面的数字
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
    # url_list = [box_office_website_url]

    # for i in range(1, 10):
    #     url_list.append(box_office_website_url + '?page=%d' % i)
    #
    # for url in url_list:
    #     process(url, offline_page_dir_path)

    process_offline(offline_html_dir_name)


if __name__ == '__main__':
    main()
