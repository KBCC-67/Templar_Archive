'''
'https://tieba.baidu.com/f?kw=stellaris&ie=utf-8&pn=450'
'https://tieba.baidu.com/f?kw=stellaris&ie=utf-8&pn=0'
#50pn一页，在一页之内搜索'/p/'就能找到所有贴吧链接，因为每个帖子的格式都像这样：
'https://tieba.baidu.com/p/7826942366'
'''
#本文件基本都是网上的代码，只有一个用：把目录爬下来（而且还没有对准）
from urllib import request,parse
import time
import random
import os
#from ua_info import ua_list #使用自定义的ua池#这个似乎不能用了
from fake_useragent import UserAgent
#定义一个爬虫类
class TiebaSpider(object):
    #初始化url属性
    def __init__(self):
        self.url='http://tieba.baidu.com/f?{}'
    # 1.请求函数，得到页面，传统三步
    def get_html(self,url):
        #req=request.Request(url=url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
                                             #'Accept-Language':'zh-CN,zh;q=0.9'})#可能只好用自己的身份了
        req=request.Request(url=url,headers={'User-Agent':str(UserAgent().random),'Accept-Language':'zh-CN,zh;q=0.9'})#克制反爬机制：设置headers
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
        name='stellaris'#input('输入贴吧名：')
        begin=171#int(input('输入起始页：'))
        stop=201#int(input('输入终止页：'))
        # +1 操作保证能够取到整数
        for page in range(begin,stop+1):
            pn=(page-1)*50
            params={
                'kw':name,
                'pn':str(pn)
            }
            #拼接URL地址   
            params=parse.urlencode(params)
            url=self.url.format(params)#这是自动在self.url之后追加？
            print(url)
            #assert False
            #发请求
            html=self.get_html(url)
            #定义路径
            filename='content_ref/0516{}-{}页.html'.format(name,page)
            self.save_html(filename,html)
            #提示
            print('第%d页抓取成功'%page)
            if (os.path.getsize(filename)/1024)<=3:
                print('爬取似乎触发了安全检测')
            else:
                print('百度还没有发现我是机器人')
            #每爬取一个页面随机休眠1-2秒钟的时间
            time.sleep(random.randint(180,240))
#以脚本的形式启动爬虫
if __name__=='__main__': 
    start=time.time()
    spider=TiebaSpider() #实例化一个对象spider
    spider.run() #调用入口函数
    end=time.time()
    #查看程序执行时间
    print('执行时间:%.2f'%(end-start))  #爬虫执行时间