# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/7/30 15:36
# @Author : Gengwu
# @FileName: implicitly_wait.py
# @Software: PyCharm
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException #导入一个没有这个元素的类，定位到没有这个元素会抛出一个异常
from time import ctime #ctime导入后作为一个时间戳判断一下
from time import  sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
from selenium import webdriver
# from fake_useragent import UserAgent

import codecs
from lxml import etree
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery");
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")#C:\Users\chuan\AppData\Local\Google\Chrome\Application>chrome.exe --remote-debugging-port=9222

driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.delete_all_cookies()
# driver.set_window_size(800,800)
# driver.set_window_position(0,0)
#driver = webdriver.Firefox()
reaction_path ="reaction.json"
f_reaction = codecs.open(reaction_path, 'w', 'utf8')
for page_num in range(78,118):#118
    url="https://go.drugbank.com/reactions?page="+str(page_num)
    print(url)
    #url="PyCharm Project\drugbank_2.html"
    page_sourse = driver.get(url)
    file_name ='drugbank_' + str(page_num) + u'.html'

    source_code = driver.page_source

    # 保存文件
    f = codecs.open("all/"+file_name, 'w+', 'utf8')
    f.write(source_code)
    f.close()
    driver.implicitly_wait(10)
    time.sleep(5)

    selector = etree.HTML(source_code)
    tbody = selector.xpath("//*[@id='reactions-table']/tbody/tr")
    try:
        for each in tbody:
            # #1.'reactant'
            reactant_name = each.xpath('td[1]/a/text()')[0]
            reactant_href = each.xpath('td[1]/a/@href')[0]
            #https://go.drugbank.com/structures/metabolites/DBMET00223.smiles
            reactant_smiles_url = "https://go.drugbank.com/structures"+str(reactant_href)
            driver.implicitly_wait(10)

            driver.get(reactant_smiles_url)
            source_code = driver.page_source
            # 保存文件
            f = codecs.open("reactant/" + reactant_name.replace("/","_"), 'w+', 'utf8')
            f.write(source_code)
            f.close()
           # reactant_smile = etree.HTML(source_code).xpath('/html/body/main/div/div/div[2]/div[2]/dl[5]/dd[6]//string(.)')
            driver.implicitly_wait(10)
            time.sleep(3)


            # #2.'Interacting Gene/Enzyme'
            Enzyme_name = each.xpath('td[3]')[0].xpath('string(.)')
            #Enzyme_href = each.xpath('td[3]/span/span/a/@href')[0]

            # #3.'product'#
            product_name = each.xpath('td[4]/span/span/a/text()')[0]
            product_href = each.xpath('td[4]/span/span/a/@href')[0]
            # https://go.drugbank.com/structures/metabolites/DBMET00223.smiles
            product_smiles_url = "https://go.drugbank.com/structures" + str(product_href)

            driver.get(product_smiles_url)
            source_code = driver.page_source
            # 保存文件
            f = codecs.open("product/" + product_name.replace("/","_"), 'w+', 'utf8')
            f.write(source_code)
            f.close()
           # product_smile = etree.HTML(source_code).xpath(
              #  '/html/body/main/div/div/div[2]/div[2]/dl[5]/dd[6]/div/string(.)')

            driver.implicitly_wait(10)
            time.sleep(3)


            line = reactant_name+"|"+Enzyme_name+"|"+product_name+"\n"
            print(line)
            f_reaction.write(line)
    except:
        continue


f_reaction.close()







