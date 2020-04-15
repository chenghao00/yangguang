# yangguang
阳光政务平台爬虫


#在items.py中
完成定义item 


#在spiders.py中
拼接url传递给scrapy.Resquest(url,callback,meta) 
使用meta传递参数item获取去对应的图片信息 
callback=self.parse_detail
翻页获取本页对应的下页url


#在pipelines.py中
def __init__(self, mongo_url, mongo_db):
def from_crawler(cls, crawler):
两个函数获取配置文件中的信息 

def open_spider(self, spider): 进行mongo初始化

def process_item(self, item, spider): 插入到数据库中， 并进行数据的处理 self.process_content
    item["content"] = self.process_content(item["content"])
    
def process_content(self, content):
    content = re.sub(r"\u3000|\r\n", "", content)
    #content = [i for i in content if len(i) > 0]  # 去除列表中的空字符串
    return content

def close_spider(self, spider): 关闭数据库
