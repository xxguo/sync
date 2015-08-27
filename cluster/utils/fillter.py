# -*- coding: utf-8 -*-

_filter_words = ["技术监督局", "政务动态", "红盾网", "地方视窗"]

def filter_data(data):
    for w in _filter_words:
        if w.find(data["title"]) != -1:
            return True

    return False
