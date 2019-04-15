# -*- encoding:utf8 -*-
import json
import random
import requests


class GetIP(object):
    ProxyPool = []

    # 初始化，每次初始化对象时查看ProxyPool中是否有IP
    def __init__(self):
        if self.ProxyPool:
            print("可用IP列表：", self.ProxyPool)
        else:
            self.crawl_ips()

    # 从代理商获取IP代理
    def crawl_ips(self, count=6):
        print("从代理商获取IP代理"+"--"*30+"\n")
        url = "http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=" \
              "ee7d6ae09bfa4cd8b9cb5f566256f490&count={}&expiryDate=0&format=1&newLine=2".format(count)
        body = json.loads(requests.get(url).text)
        for ip_info in body["msg"]:
            self.ProxyPool.append("https://"+ip_info["ip"]+":"+ip_info["port"])

    # 删除不可用IP
    def delete_ip(self, ip):
        self.ProxyPool.remove(ip)
        # 如果代理池中的ip过少,则再爬取一定数量的IP到代理池中
        if len(self.ProxyPool) <= 2:
            self.crawl_ips(4)

    # 判断IP是否可用
    def judge_ip(self, ip):
        url = "https://www.baidu.com"
        proxy = {"https": ip}
        try:
            response = requests.get(url, proxies=proxy, timeout=2)
        except:
            print(ip+"不可用")
            self.delete_ip(ip)
            return False
        # 如果能正常访问百度网页则进入下面判断
        else:
            code = response.status_code
            if (code >= 200) and (code < 300):
                return True
            else:
                print(ip+"不可用")
                self.delete_ip(ip)
                return False

    # 从列表中获取IP代理
    def get_random_ip(self):
        if self.ProxyPool:
            # 从列表中随机获取一个IP
            ip = random.choice(self.ProxyPool)

            # 验证IP是否可用
            flag = self.judge_ip(ip)
            if flag:
                return ip
            else:
                return self.get_random_ip()
        # else:
        #     self.crawl_ips()


