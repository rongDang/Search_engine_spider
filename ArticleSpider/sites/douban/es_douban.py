# -*- encoding:utf8 -*-
from elasticsearch_dsl import Document, Keyword, Text, Completion, Float
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])  # 连接es
my_analyzer = analyzer("ik_smart")      # 创建suggest的分析器的详细程度


class DouBanIndex(Document):
    """
        :param: 电影id，电影名，别名，简介，链接，导演，演员，类型，上映时间
    """
    suggest = Completion(analyzer=my_analyzer)
    movie_id = Keyword()
    name = Text(analyzer="ik_max_word")
    alias = Text(analyzer="ik_smart")
    introduce = Text(analyzer="ik_smart")
    url = Keyword()
    directors = Keyword()
    rate = Float()
    casts = Keyword()
    type = Keyword()
    date = Keyword()

    class Index:
        name = "movie"

        # 设置分片数量，副本数量，
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 0
        }


if __name__ == "__main__":
    DouBanIndex.init()


