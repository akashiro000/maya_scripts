# -*- coding: utf-8 -*-
try:
    import _usersetup

    # Githubで公開しないセットアップ処理
    _usersetup.doit()
except ImportError:
    pass