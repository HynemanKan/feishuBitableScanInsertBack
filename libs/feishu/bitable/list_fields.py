import requests

from libs.feishu import feishu_response_load


def list_fields(access_token:str,app_token:str,table_id:str):
    response = requests.get(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
        headers={"Authorization": f"Bearer {access_token}"})
    data = feishu_response_load(response)
    return data["data"]