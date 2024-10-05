import json
import logging

from requests import Response

from libs.feishu.errors import FeishuError


def feishu_response_load(res:Response)->dict:
    if res.status_code != 200:
        raise FeishuError()
    data = json.loads(res.text)
    if data["code"] !=0:
        raise FeishuError()
    return data
