# -*- coding: utf-8 -*-
def parse_requires(line):
    return [element.replace('"', '') for element in line[:-1].split(' ')][1:]

def parse_fileInfo(line):
    return [element.replace('"', '') for element in line[:-1].split(' "')][1:]