#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:41:57
# @Author  : Reynard (rey@pku.edu.cn)
# @Link    : link
# @Version : 1.0.0

import re
from google_trans_new import google_translator
from termcolor import cprint
from time import sleep


def clean_text(text):
    # TODO: 文本清洗
    # print(text)
    text = re.sub('(\[转发自.*\])\n', '', text)
    text = text.replace('\n', '/////')
    text = text.replace('#', ' ')
    text = filter_emoji(text)
    return (text)


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        res = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        res = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return res.sub(restr, desstr)


def big5(text):
    try:
        text.encode('big5hkscs')
        cprint('繁体', 'white', 'on_grey')
        result = True
    except Exception as e:
        cprint('简体' + e, 'white', 'on_grey')
        result = False
    return result


def trans(text, lang='zh-CN', detect=1):
    text = clean_text(text)
    tr = google_translator()
    if lang == 'en':
        result = get_trans(text, lang_tgt='en')
    elif lang == 'zh':
        result = get_trans(text, lang_tgt='zh-CN')
    elif lang == 'ru':
        result = get_trans(text, lang_tgt='ru')
    elif lang == 'ja':
        result = get_trans(text, lang_tgt='ja')
    elif lang == 'vi':
        result = get_trans(text, lang_tgt='vi')
    elif lang == 'pt':
        result = get_trans(text, lang_tgt='pt')
    else:
        if get_lang(text)[0] == 'zh-CN':
            result = get_trans(text, lang_tgt='zh-CN') + '\n' \
                + get_trans(text, lang_tgt='en')
        else:
            result = get_trans(text, lang_tgt='zh-CN') + '\n' \
                + text
    return result


def trans_auto(text):
    text = clean_text(text)
    tr = google_translator()
    lang = get_lang(text)[0]
    if lang == '语言检测失败':
        return '语言检测失败'
    else:
        if  lang== 'zh-CN':
            result = get_trans(text, lang_tgt='en')
        elif lang == 'en':
            result = get_trans(text, lang_tgt='zh-CN')
        else:
            result = get_trans(text, lang_tgt='zh-CN') + '\n\n' + get_trans(
                text, lang_tgt='en')
        return result


def get_lang(text):
    detector = google_translator()
    try:
        lang = detector.detect(text)
        print(lang)
    except Exception as e:
        lang = ['语言检测失败']
        sleep(0.5)
    return lang


# result = get_lang('hello')


def get_trans(text, **kwargs):
    translator = google_translator()
    result = None
    while result == None:
        try:
            result = translator.translate(text, **kwargs)
        except Exception as e:
            cprint('API Error' + str(e), 'white', 'on_yellow')
            translator = google_translator()
            sleep(0.5)
            pass
    return result


# result = get_trans('hello',lang_tgt='ja')

if __name__ == "__main__":
    # print('Please run main.py instead of me!')
    print(trans_auto('测试'))
    pass
