# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import codecs



def selenium_fun():
    # 输入框内人获取
   #key_1 = entry_input.get()
    # 加载谷歌浏览器及输入登录的网址
    brower = webdriver.Chrome()
    brower.implicitly_wait(30)
    brower.get("https://www.yaozh.com/login/")
    # 窗口最大化
    brower.maximize_window()
    # ele=brower.find_element_by_id("kw")
    # entry=brower.find_element_by_class_name("s_ipt")
    Count = "13767448894"
    password = "110143nhy"
    # 账户输入
    entry = brower.find_element_by_xpath("//*[@id='username']")  # 调试失败input...sss的错误
    entry.clear()
    # print(entry.get_attribute("name"))
    entry.send_keys(Count)
    # 密码输入
    entry1 = brower.find_element_by_xpath("//*[@id='pwd']")  # 调试失败input...sss的错误
    entry1.clear()
    # print(entry.get_attribute("name"))
    entry1.send_keys(password)
    # 点击登录
    click = brower.find_element_by_xpath("//*[@id='button']")
    click.click()
      # 休息8秒，避免页面还没跳转
    # 点击药智数据
    click1 = brower.find_element_by_xpath("/html/body/div[1]/div/div[1]/a[2]")
    click1.click()

    currentWin = brower.current_window_handle
    handles = brower.window_handles
    # 浏览器会出现窗口跳转问题，得重新绑定，将brower与新的页面绑定起来
    for i in handles:
        if currentWin == i:
            continue
        else:

            brower.switch_to.window(i)
    # search_window=brower.current_window_handle
    # click_X=brower.switch_to_alert()
    # click_X.dismiss()
    # 关广告//*[@id="ad-dialog"]/div/img
    brower.find_element_by_xpath("//*[@id='ad-dialog']/div/img").click()
    # 移动鼠标到市场信息
    click2 = brower.find_element_by_xpath("/html/body/div[2]/ul/li[4]/a")
    ActionChains(brower).move_to_element(click2).perform()
    # 点击
    click3 = brower.find_element_by_link_text("国产药品数据库")
    click3.click()

    # 输入要搜索的关键字
    #read txt files
    ulist = []

    # data name

    while True:
        try:

           data_source = f.readline()
           data1=data_source.strip('\n')
           data=data1.strip('﻿国药准字')
        #data="国药准字Z10930008"
           if not data_source:


              break
          # data list
           name_entry = brower.find_element_by_xpath("/html/body/div[5]/div[1]/div[2]/div[1]/div/form[1]/div[4]/div/input")
           name_entry.clear()
           name_entry.send_keys(data)

        # 点击搜索
           find_button = brower.find_element_by_xpath("/html/body/div[5]/div[1]/div[2]/div[1]/div/form[1]/div[16]/div/button")
           find_button.click()                       #/html/body/div[5]/div[1]/div[2]/div[1]/div/form[1]/div[16]/div/button
        #brower.execute_script("var q=document.querySelector('body > div.main > div.ui-tab.search-tab > div.ui-tab-panels > div.ui-tab-panel.active > div > form:nth-child(1) > div.form-group.clear > div > button'); q.click();")                                          #/html/body/div[5]/div[1]/div[2]/div[1]/div/form[1]/div[16]/div/button
                                       #/html/body/div[5]/div[1]/div[2]/div[1]/div/form[1]/div[16]/div/button
        # 将brower与新的页面绑定起来
           for i in handles:
              if currentWin == i:
                  continue
              else:

                  brower.switch_to.window(i)
        # 解析页面


           name=brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[1]/a")
           type=brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[2]")
           acompany=brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[3]")
           number=brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[4]")

           from_number=brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[5]")
           date = brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[6]")
           medicine_type = brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[7]")
              # detail = brower.find_element_by_xpath("/html/body/div[5]/div[4]/div/div[2]/table/tbody/tr/td[8]/a")

              # ulist.append([name.text,type.text,acompany.text,number.text,from_number.text,date.text,medicine_type.text])
           file.write(str(name.text+'|||'+ type.text+'|||'+ acompany.text+'|||'+ number.text+'|||'+ from_number.text+'|||'+ date.text+'|||'+ medicine_type.text)+'-end-'+'\n')

        except Exception as erro:
            print(erro)
            no_result_file.write(str( data1 +  '\n'))#存没找到标准字的文件
            #ActionChains(brower).key_down(Keys.CONTROL).send_keys(Keys.F5).perform(

        #else:

        finally:
    # 刷新避免502错误
                ActionChains(brower).key_down(Keys.CONTROL).send_keys(Keys.F5).perform()

    f.close()
    file.close()
    no_result_file.close()
    #print(ulist)
f = open("data1.txt", "r", encoding="utf8")
file = open("result.txt", "a", encoding="utf8")#存结果的文件
no_result_file= open("no_result_file.txt", "a", encoding="utf8")#存没找到标准字的文件
selenium_fun()

# # 图形窗口
# root = Tk()
# # 窗口标题
# root.title("搜集数据")
# # 长宽为650*400，200，100为距离原点的距离
# root.geometry("650x400+200+100")
# # 标签
# label = Label(root, text="药品名称:", font=("华文行楷", 20)).grid()
# # 输入框
# entry_input = Entry(root, font=("微软雅黑", 20))
# entry_input.grid(row=0, column=1)
# # 列表，本程序没用到
# text = Listbox(root, font=("微软雅黑", 20), width=40, height=10).grid(row=1, columnspan=3)
# # 搜索按钮
# button = Button(root, text="搜索", font=("微软雅黑", 12), command=selenium_fun).grid(row=0, column=2, sticky=E)
# # 显示及消息循环
# root.mainloop()
#
