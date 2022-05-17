#本文件把content_ref中出现的网址一个一个打开都爬下来
#每个帖子大概长这个样子：'https://tieba.baidu.com/p/7826942366'
from urllib import request,parse
import time
import random
#from ua_info import ua_list #使用自定义的ua池#这个似乎不能用了
from fake_useragent import UserAgent
import os
import re
#定义一个爬虫类
class TiebaSpider(object):
    #初始化url属性
    def __init__(self):
        self.url='http://tieba.baidu.com{}'#这里不用写/p/!!!!后面自己就带上来。。
    # 1.请求函数，得到页面，传统三步
    def get_html(self,url):
        #req=request.Request(url=url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'})#可能只好用自己的身份了
        req=request.Request(url=url,headers={'User-Agent':str(UserAgent().random)})#克制反爬机制：设置headers
        #如果要频繁抓取一个网页，每次都设置一样的UA，这也会被网站怀疑，因为一个人可能不会短时间内访问千百次那个网站，
        #所以我们要做的是随机换UA，我们可以从网上搜集一个UA列表，每次从中随机提取即可，这里我们就是直接用ua_list随机选择了
        res=request.urlopen(req)
        #windows会存在乱码问题，需要使用 gbk解码，并使用ignore忽略不能处理的字节
        #linux不会存在上述问题，可以直接使用decode('utf-8')解码
        html=res.read().decode("gbk","ignore")
        return html
    # 2.解析函数，此处代码暂时省略，还没介绍解析模块
    def parse_html(self):
        pass
    # 3.保存文件函数
    def save_html(self,filename,html):
        with open(filename,'w') as f:
            f.write(html)
    # 4.入口函数
    def run(self):
        #首先从content_ref文件夹里把所有要爬的链接名字提取出来
        content_root='content_ref'
        content_refs=os.listdir(content_root)
        tiezi_names=list()
        tiezi_urls=list()
        for file_name in content_refs:
            path=content_root+'/'+file_name
            file=open(path,'r',encoding='utf-8',errors='ignore')#这样直接igonre表情就都消失了
            for line in file:
                if re.search('/p/',line):
                    items=line.split("\"")
                    name=items[5]
                    crt_url=items[3]
                    #print(name,crt_url)
                    tiezi_names.append(name)
                    tiezi_urls.append(crt_url)
            file.close()
        #之后开始正式爬虫
        for index in range(len(tiezi_names)):
            url=self.url.format(tiezi_urls[index])
            print(url)
            #assert False
            html=self.get_html(url)#发请求爬网页
            output='detailed_htmls/'+tiezi_urls[index][3:]+'.html'#为了避免标题里有问号或者书名号导致存不了
            self.save_html(output,html)
            #提示
            print('帖子：{}  爬取完毕'.format(tiezi_names[index]))
            if (os.path.getsize(output)/1024)<=3:
                print('爬取似乎触发了安全检测')
            else:
                print('百度还没有发现我是机器人')
            #每爬取一个页面随机休眠180-300秒钟的时间
            time.sleep(random.randint(180,300))
        return 0
'''     
        for page in range(begin,stop+1):
            pn=(page-1)*50
            params={
                'kw':name,
                'pn':str(pn)
            }
            #拼接URL地址   
            params=parse.urlencode(params)
            url=self.url.format(params)#这是自动在self.url之后追加？
            #发请求
            html=self.get_html(url)
            #定义路径
            filename='content_ref/{}-{}页.html'.format(name,page)
            self.save_html(filename,html)
            #提示
            print('第%d页抓取成功'%page)
            #每爬取一个页面随机休眠1-2秒钟的时间
            time.sleep(random.randint(1,2))'''
#以脚本的形式启动爬虫
if __name__=='__main__': 
    
    #headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'}
    #print(headers)
    
    start=time.time()
    spider=TiebaSpider() #实例化一个对象spider
    spider.run() #调用入口函数
    end=time.time()
    #查看程序执行时间
    print('执行时间:%.2f'%(end-start))  #爬虫执行时间
    
    