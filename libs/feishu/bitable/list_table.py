import requests

from libs.feishu import feishu_response_load


def list_tables(
    access_token:str,
    app_token:str,
    page_size:int=50,
    page_token:str="",

)->dict:
    params = {}
    if len(page_token)!=0:
        params['page_token'] = page_token
    params['page_size'] = page_size
    res = requests.get(f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables",params=params,headers={
        "Authorization": f"Bearer {access_token}",
    })
    data = feishu_response_load(res)
    return data["data"]