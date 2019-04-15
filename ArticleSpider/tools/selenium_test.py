# -*- encoding:utf8 -*-
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://weibo.com/")

time.sleep(10)
browser.find_element_by_css_selector("#loginname").send_keys("18807395853")
browser.find_element_by_css_selector(".info_list.password .input_wrap .W_input").send_keys("lz1999")
browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
