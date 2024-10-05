import requests

from libs.feishu import feishu_response_load

ORDER_BY_CREATE = "CreatedTime"
ORDER_BY_UPDATE = "EditedTime"
ORDER_BY_ASC = "ASC"
ORDER_BY_DESC = "DESC"


def list_file(
    access_token:str,
    page_size:int=50,
    order_by:str=ORDER_BY_UPDATE,
    direction:str=ORDER_BY_DESC,
    page_token:str="",
    folder_token:str=""
)->dict:
    params = {}
    if len(page_token)!=0:
        params['page_token'] = page_token
    if len(folder_token)!=0:
        params['folder_token'] = folder_token
    params['page_size'] = page_size
    params['order_by'] = order_by
    params['direction'] = direction
    res = requests.get("https://open.feishu.cn/open-apis/drive/v1/files",params=params,headers={
        "Authorization": f"Bearer {access_token}",
    })
    data = feishu_response_load(res)
    return data["data"]