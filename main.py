# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 10:04
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from apps.create_app import create_app


apps =create_app("dev")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:apps', host='127.0.0.1', port=6582, debug=False, reload=True, access_log=False, workers=1,
                use_colors=True)
    # uvicorn.run('main:apps', host='127.0.0.1', port=9080)











