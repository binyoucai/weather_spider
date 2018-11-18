

# 内容结构

1. **[功能描述]**：分布式或者单机爬取全国历史天气2011-未来历史天气
2. **[环境依赖]**：
```
scrapy_redis==0.6.8
demjson==2.2.4
redis==2.10.6
Scrapy==1.5.1
PyMySQL==0.7.11
pymongo==3.7.2
```
## **[项目结构简介]**：
```
tianqi
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
├── scrapy.cfg
└── tianqi
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        ├── tq.py
        └── tq_utills.py

```

## **[使用教程]**
###1、安装环境依赖
    `pip install -r requirements.txt`
###  2、项目配置数据库
    `tianqi/tianqi/settings.py`
### 3、创建mysql数据库和表
   `mysql -uroot -p > weather.sql`
###    4、启动爬虫
    `scrapy crawl tq`
###    5、redis推start_url
    `lpush tq:start_urls  http://tianqi.2345.com/js/citySelectData.js`

##后台运行
 `nohup python -u run.py > run.log 2>&1 &`
 
##docker运行
### 1、构建镜像
`docker build -t username/tianqi:latest .`
### 2、运行镜像
`docker run -d username/tianqi `
