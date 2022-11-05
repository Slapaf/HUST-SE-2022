# -*- coding: utf-8 -*-
# @Time    : 2022/11/4 下午7:08
# @Author  : Nobody
# @File    : worddiff.py
# @Software: PyCharm
# @Description: 文本查重相关

import math
import re  # 正则包
import html  # html 包
import time
import jieba  # nlp 包
import jieba.analyse
import Levenshtein  # 编辑距离包
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # ml 包
from datasketch import MinHash  # 数据集处理包


class TextSimilarity(object):
    """
    文本相似度计算
    1. 余弦相似度
    2. Jaccard 相似度
    3. Levenshtein 相似度
    4. MinHash 相似度
    5. SimHash + 海明距离
    """

    def __init__(self, content_x1: str, content_x2: str):
        self.s1 = content_x1
        self.s2 = content_x2

    @staticmethod
    def get_bin_str(source: str):
        """
        字符串转二进制

        :param source:
        :return:
        """
        if source == "":
            return 0
        t = ord(source[0]) << 7
        m = 1000003
        mask = (1 << 128) - 1
        for c in source:
            t = ((t * m) ^ ord(c)) & mask
        t ^= len(source)
        if t == -1:
            t = -2
        t = bin(t).replace('0b', '').zfill(64)[-64:]
        return np.array(list(t)).astype(np.int64)

    @staticmethod
    def extract_keyword(content, with_weight=False):
        """
        提取关键词

        :param with_weight:
        :param content:
        :return: keywords(list): 关键词
        """
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != ' ']
        # 提取关键词
        keywords = jieba.analyse.extract_tags(
            "|".join(seg), topK=200, withWeight=with_weight)
        return keywords

    @staticmethod
    def one_hot(word_dict, keywords):
        """
        oneHot 编码

        :param word_dict:
        :param keywords:
        :return: cut_code
        """
        # ! 考虑使用 numpy 加速
        # cut_code = [0] * len(word_dict)
        cut_code = np.zeros(len(word_dict))
        for keyword in keywords:
            cut_code[word_dict[keyword]] += 1
        return list(cut_code)

    def run(self, keywords):
        """

        :param keywords:
        :return:
        """
        ret = np.empty(shape=[0, 64], dtype=int)
        for keyword, weight in keywords:
            bin_str = self.get_bin_str(keyword)
            bin_str[bin_str == 0] = -1  # 将 0 替换为 -1
            key_list = np.inner(bin_str, int(math.ceil(weight)))
            ret = np.append(ret, key_list.reshape(1, 64), axis=0)
        # 降维
        result = np.where(ret.sum(axis=0) > 0, 1, 0)
        return result

    def cosine_similarity_calc(self):
        """
        余弦相似度计算
        :return:
        """
        # 去除停用词
        jieba.analyse.set_stop_words('./baidu_stopwords.txt')
        # 提取关键词
        keyword_s1 = self.extract_keyword(self.s1)
        keyword_s2 = self.extract_keyword(self.s2)
        # 词的并集
        keyword_union = set(keyword_s1).union(set(keyword_s2))
        # 编码
        word_dict = {}
        for idx, word in enumerate(keyword_union):
            word_dict[word] = idx
        # oneHot 编码
        s1_cut_code = self.one_hot(word_dict, keyword_s1)
        s2_cut_code = self.one_hot(word_dict, keyword_s2)
        # 余弦相似度计算
        sample = [s1_cut_code, s2_cut_code]
        # 除零处理
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0

    def jaccard_similarity_calc(self):
        """
        Jaccard 相似度计算
        :return:
        """
        # 去除停用词
        jieba.analyse.set_stop_words('./baidu_stopwords.txt')
        # 分词与关键词提取
        keyword_s1 = self.extract_keyword(self.s1)
        keyword_s2 = self.extract_keyword(self.s2)
        # Jaccard 相似度计算
        intersection = len(list(set(keyword_s1).intersection(set(keyword_s2))))
        j_union = len(list(set(keyword_s1).union(set(keyword_s2))))
        # 除零处理
        sim = float(intersection) / j_union if j_union != 0 else 0
        return sim

    def levenshtein_similarity_calc(self):
        """
        编辑距离相似度计算
        :return:
        """
        # 去除停用词
        jieba.analyse.set_stop_words('./baidu_stopwords.txt')
        # 提取关键词
        keyword_s1 = '，'.join(self.extract_keyword(self.s1))
        keyword_s2 = '，'.join(self.extract_keyword(self.s2))
        # ratio 计算两个字符串的相似度，基于最小编辑距离
        distances = Levenshtein.ratio(keyword_s1, keyword_s2)
        return distances

    def minhash_similarity(self):
        """
        MinHash 相似度
        :return:
        """
        # 去除停用词
        jieba.analyse.set_stop_words('./baidu_stopwords.txt')
        # MinHash 计算
        m1, m2 = MinHash(), MinHash()
        # 提取关键词
        keyword_s1 = self.extract_keyword(self.s1)
        keyword_s2 = self.extract_keyword(self.s2)
        for keyword in keyword_s1:
            m1.update(keyword.encode('utf8'))
        for keyword in keyword_s2:
            m2.update(keyword.encode('utf8'))
        return m1.jaccard(m2)

    def simhash_similarity(self):
        """
        SimHash 相似度
        :return:
        """
        # 去除停用词
        jieba.analyse.set_stop_words('./baidu_stopwords.txt')
        # 提取关键词
        keyword_s1 = self.extract_keyword(self.s1, with_weight=True)
        keyword_s2 = self.extract_keyword(self.s2, with_weight=True)
        sim_hash1 = self.run(keyword_s1)
        sim_hash2 = self.run(keyword_s2)
        length = np.count_nonzero(sim_hash1 != sim_hash2)
        # 设定阈值
        threshold = sim_hash1.shape[0]
        return 1.0 - length / threshold

    def word_diff(self):
        """
        综合相似度，采用 5 种相似度算法的加权平均

        Returns:

        """
        # 去除停用词
        jieba.analyse.set_stop_words('./stopwords/baidu_stopwords.txt')
        # 分词与关键词提取
        keyword_s1 = self.extract_keyword(self.s1)
        keyword_s2 = self.extract_keyword(self.s2)
        # 关键词的并集
        keyword_union = set(keyword_s1).union(set(keyword_s2))
        # * 1. 余弦相似度
        # 编码
        word_dict = {}
        for idx, word in enumerate(keyword_union):
            word_dict[word] = idx
        # onehot 编码
        s1_cut_code = self.one_hot(word_dict, keyword_s1)
        s2_cut_code = self.one_hot(word_dict, keyword_s2)
        # 余弦相似度计算
        cosine_sim = cosine_similarity([s1_cut_code, s2_cut_code])[1][0]
        # * 2. Jaccard 相似度
        intersection = len(list(set(keyword_s1).intersection(set(keyword_s2))))
        j_union = len(list(keyword_union))
        jaccard_sim = float(intersection) / j_union if j_union != 0 else 0
        # * 3. Levenshtein 相似度
        levenshtein_sim = Levenshtein.ratio(','.join(keyword_s1), ','.join(keyword_s2))
        # * 4. MinHash 相似度
        # MinHash 计算
        m1, m2 = MinHash(), MinHash()
        for keyword in keyword_s1:
            m1.update(keyword.encode('utf8'))
        for keyword in keyword_s2:
            m2.update(keyword.encode('utf8'))
        minhash_sim = m1.jaccard(m2)
        # * 5. SimHash 相似度
        sim_hash1 = self.run(self.extract_keyword(self.s1, with_weight=True))
        sim_hash2 = self.run(self.extract_keyword(self.s2, with_weight=True))
        length = np.count_nonzero(sim_hash1 != sim_hash2)
        # 设定阈值
        threshold = sim_hash1.shape[0]
        simhash_sim = 1.0 - length / threshold
        # * 返回平均值
        return (cosine_sim + jaccard_sim + levenshtein_sim + minhash_sim + simhash_sim) / 5


def demo():
    """
    测试，最后删掉
    :return:
    """
    t1 = time.time()
    content_x = open('./testfile_a.txt', 'r').read()
    content_y = open('./testfile_a1.txt', 'r').read()
    for i in range(100):
        # similarity = TextSimilarity(content_x, content_y).cosine_similarity_calc()
        # print("余弦相似度: %.2f%%" % (similarity * 100))
        # similarity = TextSimilarity(content_x, content_y).jaccard_similarity_calc()
        # print("Jaccard 相似度: %.2f%%" % (similarity * 100))
        # similarity = TextSimilarity(content_x, content_y).levenshtein_similarity_calc()
        # print("Levenshtein 相似度: %.2f%%" % (similarity * 100))
        # similarity = TextSimilarity(content_x, content_y).minhash_similarity()
        # print("MinHash 相似度: %.2f%%" % (similarity * 100))
        similarity = TextSimilarity(content_x, content_y).simhash_similarity()
        # print("SimHash 相似度: %.2f%%" % (similarity * 100))
    t2 = time.time()
    print("总时间（毫秒）: %.2f ms" % ((t2 - t1) * 1000))
    print("总时间（秒）:   %.2f s" % (t2 - t1))
