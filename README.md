# box office web crawler

## 爬取内容
[电影票房](http://58921.com)

## 执行命令

`python box_office_web_crawler.py`


## 环境配置

[解决Python图片处理模块pillow使用中出现的问题](http://www.cnblogs.com/runchen0518/p/8989968.html)

## 相关说明
* 由于第二页以后的排行榜数据需要登录才能查看，目前爬虫绕过登录比较麻烦（可行），所以直接写了一个函数，从离线网页中提取数据。
* 需要说明的是，需要在该python文件夹下面新建一个html文件夹，把网页按照顺序依次编号为1.html，2.html，...，13.html放到该文件夹中，python代码会依次提取html文件，进行匹配，拿到相应数据。
* 由于总票房是用图片来显示的，repo里面提供了一个图片识别的test。