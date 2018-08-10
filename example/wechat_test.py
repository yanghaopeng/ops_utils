# coding = utf-8

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import sys
dcap = dict(DesiredCapabilities.PHANTOMJS)

dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")

js2 = 'window.scrollTo(0, document.body.scrollHeight)'


class crawl_wechat:

    def __init__(self, url):

        self.url = url

        self.old_scroll_height = 0

    def getList(self):

        driver = webdriver.PhantomJS(desired_capabilities=dcap)

        driver.get(self.url)

        for i in range(10):
            print(BeautifulSoup(driver.page_source, 'html5lib').find('div', class_="loadmore with_line"))
            if(BeautifulSoup(driver.page_source,'html5lib').find('div', class_="loadmore with_line").get("style")) == 'display:none':
                driver.execute_script(js2)

        resp = BeautifulSoup(driver.page_source, 'html5lib')
        msg_list = []
        msg_cover = resp.find_all("div", class_="msg_cover")

        for href in msg_cover:
            if href.get("hrefs") is not None:
                msg_list.append(href.get("hrefs"))
            else:
                msg_cover_redirect = resp.find_all(
                    "a", class_="cover_appmsg_link_box redirect")
                for tmp in msg_cover_redirect:
                    msg_list.append(tmp.get("hrefs"))

        sub_msg = resp.find_all("h4", class_="flex_msg_title msg_title")

        for sub_href in sub_msg:
            msg_list.append(sub_href.get("hrefs"))

        print(msg_list)


if __name__ == '__main__':

    key = '8e4e52b940835730adb624ab85478864b618714df8be65249a3268c9fcda0597363061b6d4fbdc78c9ff2c976ad9dbee5a4d7faf4d18e1b96d9417b760d7feea1558ff6eee682afc6d2c710383f70697'

    wechat_url = 'https://mp.weixin.qq.com/mp/getmasssendmsg__biz=MzI1NjE2MTUzNg==&uin=MTA1MzA1Nzk4Mw%3D%3D&key=&devicetype=Windows+7&version=62060426&lang=zh_CN&ascene=7&pass_ticket=LG2u0K7fzmx47cbBEsGg65xkocMaK1iCadtBI2f7fb6Ak6mKao8U9aKnMiAENlRJ'.format(
        key)

    wechat = crawl_wechat(wechat_url)

    wechat.getList()
