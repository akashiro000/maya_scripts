# -*- coding: utf-8 -*-

class Node(object):
    createNode_optionlabel = {
        "-n": "name",
        "-name": "name",
        "-p": "parent",
        "-parent": "parent",
        "-s": "shared",
        "-shared": "shared",
        "-ss": "skipSelect",
        "-skipSelect": "skipSelect"
    }

    def __init__(self, maincommand, subcommands=[]):
        self.nodetype = maincommand.split(" ")[1].replace('"', "")



