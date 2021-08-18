#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :start.py
# @Time      :2021/8/16 18:53
# @Author    :sunyyer
import csv
import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    "cookie": "__gads=ID=26a71fb437d8c873-2210b098ceca0021:T=1629110991:RT=1629110991:S=ALNI_MYh4tk6C_kVR4ayNlvdpL_CmvYuag; _ga=GA1.2.823467924.1629110991; _gid=GA1.2.2135990507.1629110992; ASP.NET_SessionId=k0a01mikxiipvywnkhwnpx5m",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}


def judge_exists(path, title):
    if os.path.exists(path):
        return
    # title = []
    with open(path, 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写入单行
        writer.writerow(title)


def save_to_csv(data, filename: str, title: list):
    path = r'./data/{}.csv'.format(filename)
    judge_exists(path, title)
    with open(path, 'a+', encoding='utf-8', newline='') as f:
        # 创建一个写的对象
        writer = csv.writer(f)
        # 写入单行
        writer.writerow(data)


class Rank:
    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe',
                                       options=self.chrome_options)  # executable执行webdriver驱动的文件
        self.basic_url = 'https://rank.twincn.com'

    def start(self):
        url = "https://rank.twincn.com/c.aspx"
        soup = BeautifulSoup(self.get_html(url), 'lxml')
        # print(soup)
        content_list = soup.find('table', class_='table table-striped').find_all('tr')
        for item in content_list:
            item_soup = BeautifulSoup(str(item), 'lxml')
            name = item_soup.find('a').string
            url_path = item_soup.find('a').get('href')
            self.handle_details(name, url_path)

    def get_html(self, url):
        res = requests.get(url, headers=headers)
        html = res.text
        return html

    def request_data(self, url):
        try:
            self.driver.get(url)
        except:
            pass
        sleep(2)
        html = self.driver.page_source
        return html

    def handle_details(self, name, url_path):
        html = self.get_html(self.basic_url + url_path)
        soup = BeautifulSoup(html, 'lxml')
        content_list = soup.find('table', class_='table table-striped').find_all('tr')
        for item in content_list:
            item_soup = BeautifulSoup(str(item), 'lxml')
            try:
                company_name = item_soup.find_all('a')[0].string
                company_name_url = item_soup.find_all('a')[1].get('href')
                self.handle_company_name(name, company_name, company_name_url)
            except:
                pass

    def handle_company_name(self, name, company_name, company_name_url):
        title = ["統一編號（統編）", "公司名稱", "英文名稱", "代表人姓名", "公司所在地", "英文地址", "電話", "傳真", "公司狀況", "股權狀況", "資本總額(元)",
                 "實收資本額(元)", "登記機關", "每股金額(元)", "已發行股份總數(股)", "核准設立日期", "最後核准變更日期", "複數表決權特別股", "對於特定事項具否決權特別股",
                 "特別股股東被選為董事、監察人之禁止或限制或當選一定名額之權利", "類型", "類型", "所營事業資料", "聲明"]
        html = self.request_data(company_name_url)
        soup = BeautifulSoup(str(html), 'lxml')
        content_list = soup.find_all('div', class_='table-responsive')[0].find('table',
                                                                               class_='table table-striped').find_all(
            'tr')
        data = [company_name]
        for item in content_list:
            try:
                item_soup = BeautifulSoup(str(item), 'lxml')
                value = item_soup.find_all('td')[-1].string.replace('\n', '').replace(' ','')
                data.append(value)
            except:
                pass
        new_data = tuple(data)
        save_to_csv(new_data, "{}".format(name), title)
        print(new_data)


if __name__ == "__main__":
    rank = Rank()
    rank.start()
