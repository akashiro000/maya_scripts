# encoding: utf-8
"""現在利用しているモジュール一覧と、それを利用しているモジュールの一覧を生成する。"""

import sys
import types

import collections


def doit(_globals):
    result = collections.OrderedDict()
    _modules = sorted(sys.modules.keys())

    for module_name in _modules:
        module = sys.modules[module_name]
        if module is None:
            continue
        elif '(built-in)' in repr(module):
            continue

        if hasattr(module, '__path__') and module.__path__:
            path = module.__path__[0]
        elif hasattr(module, '__file__'):
            path = module.__file__

        result[module] = {
            "file": path,
            "name": module.__name__,
            "use": []
        }

    # 利用しているモジュールを再帰検索してuseに列挙する。
    _append_use_in_module(_globals, result)

    return result


def _append_use_in_module(modules, _dict, path="globals"):
    for _, module in modules.items():
        if not isinstance(module, types.ModuleType):
            continue
        elif '(built-in)' in repr(module):
            continue
        elif module not in _dict.keys():
            continue
        elif path in _dict[module]["use"]:
            continue
        elif module is None:
            continue

        _dict[module]["use"].append(path)

        next_modules = {k: getattr(module, k) for k in sorted(dir(module))}
        next_path = module.__name__

        _append_use_in_module(next_modules, _dict, path=next_path)


if __name__ == "__main__":
    for _, v in  doit(globals()).items():
        print v["name"]
        print v["use"]