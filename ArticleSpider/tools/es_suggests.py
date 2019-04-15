# -*- encoding:utf8 -*-


# 生成suggest， 需要改正，used_words存在无意义
def generate_suggests(es_index, info_tuple):
    es = es_index
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            words = es.indices.analyze(body={"analyzer": "ik_smart", "text": "{}".format(text)})
            # 循环words，set对循环结果去重
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            # 过滤已经存在的单词,????
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests
