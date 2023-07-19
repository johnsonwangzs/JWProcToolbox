# -*- coding: UTF-8 -*-
# @file: cn2en.py
# @author: johnsonwangzs
# @time: 2023/7/17 16:25
# @function: 将一个txt(markdown)文件中的中文标点转化为英文

FILEPATH_CN = './test_in.txt'
FILEPATH_EN = './test_out.txt'
PUNCTUATION_CN = ['。', '，', '；', '：', '“', '”', '’', '‘', '？', '！', '（', '）']
PUNCTUATION_EN = ['. ', ', ', '; ', ': ', '\"', '\"', '\'', '\'', '? ', '! ', '(', ')']


def trans_character_cn2en(filepath_in, filepath_out) -> None:
    """
    将一个txt文件中的中文标点转化为英文
    :param string filepath_in: 输入文件路径
    :param string filepath_out: 输出文件路径
    :return: 无

    例子
    ========
    输入::

        他说：“早（啊）。”
        她说，“吃了吗您内！？”

    转换后::

        他说: "早(啊). "
        她说, "吃了吗您内! ? "
    """
    after_trans = ''
    with open(filepath_in, 'r', encoding='utf-8') as f_in:
        while True:
            ch = f_in.read(1)
            if not ch:
                break
            if ch in PUNCTUATION_CN:
                after_trans += PUNCTUATION_EN[PUNCTUATION_CN.index(ch)]
            else:
                after_trans += ch
    with open(filepath_out, 'w', encoding='utf-8') as f_out:
        f_out.write(after_trans)


if __name__ == '__main__':
    trans_character_cn2en(filepath_in=FILEPATH_CN, filepath_out=FILEPATH_EN)
    print('Done.')
