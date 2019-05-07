# -*- coding: utf-8 -*-
"""mayaAsciiのパーサー"""

import re
import _scene_config_parser
import node_parser

REG_HEAD_TAB = re.compile(r"^\t*")

class Scene(object):
    def __init__(self, filepath):
        first_parse = self._first_parser(filepath)

        # scene情報をセット
        for main, _sub in first_parse:
            maincommand = main.split(" ")[0]
            if "parse_%s" % maincommand in dir(_scene_config_parser):
                setattr(self, *eval('_scene_config_parser.parse_%s' % maincommand)(main))


    def _first_parser(self, filepath):
        """メインコマンドごとに分離"""
        with open(filepath) as f:
            lines = f.read().split("\n")

        result = []
        for line in lines:
            # fileheader, footerは無視。
            if line.startswith("//"):
                continue

            # 先頭行が\tで始まらないものはメインコマンドとして扱う
            if not line.startswith("\t"):
                result.append([line, []])
            else:
                sub = REG_HEAD_TAB.sub("", line)
                sub_list = result[-1][1]

                # subコマンドが存在しない、もしくは終端行がセミコロンで終了している場合は
                # サブコマンドを追加。
                if not sub_list or sub_list[-1].endswith(";"):
                    sub_list.append(sub)
                else:
                    sub_list[-1] += sub
                result[-1][1] = sub_list

        return result
