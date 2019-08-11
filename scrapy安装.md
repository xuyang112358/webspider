pip install Twisted

pip install scrapy

创建工程

打开命令行，然后切换到需要的目录,d:

输入下面的命令创建工程

scrapy startproject weibo

其中weibo是你需要创建的工程的名字，前两个参数不动。

然后到达工程的目录，cd weibo

scrapy genspider weibocn www.weibo.cn

然后这时候进入工程的spider文件发现多了一个文件weibocn.py

weibocn 是爬虫的名字，具有唯一性，每个工程拥有一个唯一的爬虫名，m.weibo.cn是指定域范围，获取的内容只在指定的域。

