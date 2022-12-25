import os
import time
import datetime
import codecs
from lxml import etree
from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
'''
遇到python不懂的问题，可以加Python学习交流群：1004391443一起学习交流，群文件还有零基础入门的学习资料
'''
#控制编码，全英文网页，用不着
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#C:\Users\chuan\AppData\Local\Google\Chrome\Application>chrome.exe --remote-debugging-port=9222
# # date格式转为string格式
today = datetime.date.today()
today_string = today.strftime('%Y-%m-%d')

#通过浏览器得到网页页面--反反爬虫
def html_getter(site,file_name):
    #driver = webdriver.Firefox()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")#C:\Users\chuan\AppData\Local\Google\Chrome\Application>chrome.exe --remote-debugging-port=9222
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.set_window_size(800, 800)
    driver.set_window_position(0, 0)
    driver.get(site)
    driver.maximize_window() # 将浏览器最大化显示
    # 控制间隔时间，等待浏览器反映


    driver.implicitly_wait(10)

    f = codecs.open(file_name, 'w+', 'utf8')
    source_code = driver.page_source
    f.write(source_code)
    f.close()

#打开保存在本地的html文件
def file_html(file_name):
    f = open(file_name,'r',encoding="utf-8")
    html = f.read()
    f.close()
    return html

#写入csv，也可以有其他写入方式，这个地方就csv啦
def csv_writer(ll):
    headers = ['drug','inter','snp_rs_id','Allele_name','Defining_change','Adverse_Reaction','ref','href','original_title']
    with open('drugbank.csv','a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(ll)

#用xpath解析网页，得到表格数据，我就是这么爱xpath，不喜欢正则表达式
def data_get(html):
    selector = etree.HTML(html)
    tbody=selector.xpath('/html/body/main/table/tbody/tr')
    for each in tbody:
        # #1.'drug'
        drug_name=each.xpath('td[1]/strong/text()')[0]
        drug_sn=each.xpath('td[1]/a/text()')[0]
        drug=drug_name+'   '+drug_sn
        # #print(drug)
        # #2.'Interacting Gene/Enzyme'
        int=each.xpath('td[2]')[0]
        inter=int.xpath('string(.)')
        # print(inter)
        # #3.'SNP RS ID'
        snp=each.xpath('td[3]/a/text()')
        if snp:
            snp_rs_id=snp[0]
        else:
            snp_rs_id='Not Available   '
        #print snp_rs_id
        #4.Allele name
        Allele=each.xpath('td[4]/text()')
        if Allele:
            Allele_name=Allele[0]
        else:
            Allele_name='Not Available '
        # #print Allele_name
        # #5.'Defining change'
        Defining=each.xpath('td[5]/text()')
        if Defining:
            Defining_change=Defining[0]
        else:
            Defining_change='Not Available '
        # print Defining_change
        # 6.'Adverse Reaction'
        Adverse=each.xpath('td[6]/text()')
        if Adverse:
            Adverse_Reaction=Adverse[0]
        else:
            Adverse_Reaction='Not Available    '
        # print Adverse_Reaction
        #7.'Reference(s)'
        ref=each.xpath('td[7]/span/a/text()')[0]
        href=each.xpath('td[7]/span/a/@href')[0]
        original_title=each.xpath('td[7]/span/a/@data-original-title')[0]
        # print ref
        # print(href)
        # print(original_title)

        tt=(drug,inter,snp_rs_id,Allele_name,Defining_change,Adverse_Reaction,ref,href,original_title)
        ll.append(tt)

#print ll



if __name__ == '__main__':
    ll=[]
    for i in range(1,3):
        page_num=i
        site='https://go.drugbank.com/reactions?page='+str(page_num)
        #get the html through webdriver
        file_name=today_string+'drugbank_'+str(page_num)+u'.html'
        html_getter(site,file_name)
        html=file_html(file_name)
        data_get(html)
    csv_writer(ll)