#本文件把content_ref中出现的网址一个一个打开都爬下来
#每个帖子大概长这个样子：'https://tieba.baidu.com/p/7826942366'
from urllib import request,parse
import time
import random
#from ua_info import ua_list #使用自定义的ua池#这个似乎不能用了
from fake_useragent import UserAgent
import os
import re
from bs4 import BeautifulSoup
#定义一个爬虫类
class TiebaSpider(object):
    #初始化url属性
    def __init__(self):
        self.root='content_ref'
        self.file_names=os.listdir(self.root)
        self.outs='Templars/'
    
    def getTemplarsInfo(self):
        tiezi_names=list()
        tiezi_urls=list()
        tiezi_zuozhe=list()
        tiezi_huifuliang=list()
        tiezi_fabushijian=list()
        tiezi_current_id=-1#现在正在写入的id
        for name in self.file_names:
            print(self.root+'/'+name)
            html_doc=open(self.root+'/'+name,'r',encoding='utf-8',errors='replace')
            html_lines=html_doc.readlines()
            for line_index in range(len(html_lines)):
                line=html_lines[line_index]
                if re.search('threadlist_lz clearfix',line):
                    tiezi_current_id+=1#后面添加信息一定要和这个对齐
                if re.search('href="/p/',line):
                    #print('title',line_index)
                    items=line.split("\"")
                    name=items[5]
                    crt_url=items[3]
                    #print(name,crt_url)
                    if len(tiezi_names)==tiezi_current_id:
                        tiezi_names.append(name)
                        tiezi_urls.append(crt_url)
                    elif len(tiezi_names)>=tiezi_current_id:
                        pass
                    elif len(tiezi_names)<=tiezi_current_id:
                        tiezi_names.append('None')
                        tiezi_urls.append('None')
                        tiezi_names.append(name)
                        tiezi_urls.append(crt_url)
                if re.search('reply_num',line):
                    #print('reply',line_index)
                    start_index=line.rfind('reply_num&quot;:')
                    rest_line=line[start_index+16:]#去掉前缀所以+16
                    end_index=rest_line.rfind(',&quot;is_bak')
                    rest_line=rest_line[:end_index]
                    
                    if len(tiezi_huifuliang)==tiezi_current_id:
                        tiezi_huifuliang.append(eval(rest_line))
                    elif len(tiezi_huifuliang)>=tiezi_current_id:
                        pass
                    elif len(tiezi_huifuliang)<=tiezi_current_id:
                        tiezi_huifuliang.append(0)
                        tiezi_huifuliang.append(eval(rest_line))
                if re.search('tb_icon_author ',line):
                    #print('reply',line_index)
                    target_line=html_lines[line_index+2]
                    target_items=target_line.split("\"")
                    target_item=target_items[1]
                    
                    if len(tiezi_zuozhe)==tiezi_current_id:
                        tiezi_zuozhe.append(target_item[5:])#跳过开头主题作者
                    elif len(tiezi_zuozhe)>=tiezi_current_id:
                        pass
                    elif len(tiezi_zuozhe)<=tiezi_current_id:
                        tiezi_zuozhe.append('None')
                        tiezi_zuozhe.append(target_item[5:])
                if re.search('创建时间',line):
                    #print('reply',line_index)
                    start_index=line.rfind('title="创建时间">')
                    rest_line=line[start_index+13:]#去掉前缀所以+13
                    end_index=rest_line.rfind('</span>')
                    rest_line=rest_line[:end_index]
                    
                    if not re.search('-',rest_line):
                        rest_line='5-14'#说明是今天的，不关心具体几点
                    
                    if len(tiezi_fabushijian)==tiezi_current_id:
                        tiezi_fabushijian.append(rest_line)
                    elif len(tiezi_fabushijian)>=tiezi_current_id:
                        pass
                    elif len(tiezi_fabushijian)<=tiezi_current_id:
                        tiezi_fabushijian.append('None')
                        tiezi_fabushijian.append(rest_line)
            html_doc.close()
        print(tiezi_current_id)
        print(len(tiezi_names))
        print(len(tiezi_urls))
        print(len(tiezi_huifuliang))
        print(len(tiezi_zuozhe))
        print(len(tiezi_fabushijian))
        i=0
        print(tiezi_names[i])
        print(tiezi_urls[i])
        print(tiezi_huifuliang[i])
        print(tiezi_zuozhe[i])
        print(tiezi_fabushijian[i])
        #写入数据
        for i in range(tiezi_current_id):
            print(i)
            file=open(self.outs+tiezi_fabushijian[i]+'.txt','a',encoding='utf-8')
            file.write(tiezi_names[i]+'\n')
            file.write(tiezi_urls[i]+'\n')
            file.write(str(tiezi_huifuliang[i])+'\n')
            file.write(tiezi_zuozhe[i]+'\n')
            file.write(tiezi_fabushijian[i]+'\nend-------------------\n')
            file.close()
            
    def getFullContentList(self,soup):#可以完全确定，beautifulsoup就是不能处理div标签，里面各种东西经常就找不见，应该是百度故意不让找这样故意不规范地写的，<div>和</div>括号不匹配，整个文件就是崩溃的，但是html还能显示
        self.rogue = soup.select('.threadlist_lz clearfix')
        print(self.rogue)
        rogue_list = list()
        for item in self.rogue:
            #print(type(item))
            #print(str(item))
            item=str(item)
            #print(item.find_all('div',attr={'class':'plugin-guide-icon'}),'search result')
            
            if re.search('t_con cleafix',item):
                rogue_list.append(item)
        return rogue_list
        #下面三个属性如果对应同一个帖子的话，它们的标签就在同一个div标签class="threadlist_lz clearfix"下
        #帖子的名字是div标签threadlist_title pull_left j_th_tit 刚好50个，其中也包括了链接
        #帖子的发布人是span标签 class="tb_icon_author "（非全名，后面可能跟着no_icon_author），但是如果后面有_rely j_replyer那个是可能有可能无的最后回复人，需要删掉，作者名字是其中的title属性
        #帖子的回复数量是reply_num后面隔了一个双引号一个冒号的数字，刚好50个
        

#以脚本的形式启动爬虫
if __name__=='__main__': 
    
    #headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'}
    #print(headers)
    
    start=time.time()
    spider=TiebaSpider() #实例化一个对象spider
    spider.getTemplarsInfo() #调用入口函数
    end=time.time()
    #查看程序执行时间
    print('执行时间:%.2f'%(end-start))  #爬虫执行时间
    
    