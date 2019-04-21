# -*- coding: utf-8 -*-
"""再帰的なreloadを行うためのスクリプト

USAGE:
    # モジュール単体を再帰的リロード
    import recursive_reload
    recursive_reload.doit(hoge)

    # インタプリタ内のすべてのモジュールを再帰的リロード
    import recursive_reload
    recursive_reload.globals_reload(globals())
"""
import inspect
import os

# reload済みのmoduleパス
temp_reloaded_module = []

# reloadを考慮していないのか、他に要因があるのか分からないが
# pymelのリロードでエラーがあるので、ProgramFiles以下に存在するモジュールは無視する
ignore_directory = [
    os.environ["PROGRAMFILES"]
]

def doit(module):
    """moduleを再帰的にreloadする

    Args:
        module(types.moduleType):
    """
    global temp_reloaded_module
    # reload済みのmoduleパスのリストをリセット
    temp_reloaded_module = []

    _recursive_reload(module)

def _recursive_reload(module):
    try:
        module_file = inspect.getfile(module)
        # 既に再読込されていれば無視。
        if module_file in temp_reloaded_module:
            return
        # 再読込を行わないディレクトリ以下のmoduleも無視
        if any([module_file.startswith(x) for x in ignore_directory]):
            return

    # built-in moduleは再読込する必要が無いので、無視
    # (built-in moduleはinspect.getfileでTypeErrorを吐く)
    except TypeError:
        return

    temp_reloaded_module.append(module_file)

    # module内で利用しているmoduleを検索し再帰的reloadを行う。
    module_objs = [getattr(module, attribute) for attribute in dir(module)]
    for obj in module_objs:
        if not inspect.ismodule(obj):
            continue

        _recursive_reload(obj)

    try:
        reload(module)
        print("Success: %s" % module.__str__())
    except ImportError:
        # ptvsd などで再読込でエラーが出ることもある
        print("Error:  %s" % module.__str__())


def globals_reload(globals_):
    """渡した辞書内のmoduleを検索し、再帰的なreloadを行う。

    Args:
        globals_(dict): 更新したい辞書を渡す。
    """
    global temp_reloaded_module
    # reload済みmoduleパスのリストをリセット
    temp_reloaded_module = []

    for obj in globals_.values():
        if not inspect.ismodule(obj):
            continue

        _recursive_reload(obj)