# Search_engine_spider
对应的Search_engin仓库的爬虫端

爬虫端所依赖的包参考Search_engin仓库的requirements.txt，安装依赖包时，可能会有browsercookie包安装出错，关于该包安装出错的解决方法参考该连接:
[https://blog.csdn.net/rongDang/article/details/85938814](https://blog.csdn.net/rongDang/article/details/85938814)


爬虫代理IP方面使用的是蘑菇代理，如果你使用也是蘑菇代理，那么修改下获取IP接口的中间连接即可


可用功能
=============
1.豆瓣电影，CSDN博客的爬取，数据存入MySQL&Elasticsearch

2.对存入到Elasticsearch中的数据创建suggest

3.在redis中存入具体站点的数量，搜索的热词


拓展
=============
1.如果需要拓展你自己的爬虫，创建你的item，继承items中的抽象类，实现对应的方法








