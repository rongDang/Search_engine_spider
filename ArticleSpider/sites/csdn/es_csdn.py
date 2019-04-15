# -*- encoding:utf8 -*-
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])  # 连接es
my_analyzer = analyzer("ik_max_word")


class CsdnBlogIndex(Document):
    suggest = Completion(analyzer=my_analyzer)
    blog_id = Keyword()
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_smart")
    nick_name = Text(analyzer="ik_smart")
    user_url = Keyword()
    blog_url = Keyword()
    date = Date()

    class Index:
        name = "csdn"

        # 设置分片数量，副本数量，
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 0
        }


if __name__ == "__main__":
    # 执行init()在elastic search 中创建索引
    CsdnBlogIndex.init()
