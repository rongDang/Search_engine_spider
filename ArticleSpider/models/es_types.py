# -*- encoding:utf8 -*-
from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])  # 连接es
my_analyzer = analyzer("ik_max_word")


class DouBan(Document):
    # Completion的analyzer可以直接设置字符串，也可以按照现在的方式设置
    suggest = Completion(analyzer=my_analyzer)
    # 电影名,导演,电影别名,评分
    title = Text(analyzer="ik_max_word")
    director = Keyword()
    alias = Text(analyzer="ik_max_word")
    grade = Integer()

    class Meta:
        # 设置类型名称,默认是doc
        doc_type = "test"

    class Index:
        """
            https://github.com/elastic/elasticsearch-dsl-py
            这里设置副本数量为0，因为是在单机上运行，设置多个副本会降低插入数据速度
        """
        name = "douban2"

        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }


if __name__ == "__main__":
    # 根据我们定义的类 ,在elasticsearch中生成mappings
    DouBan.init()
    # print(DouBan.index)


